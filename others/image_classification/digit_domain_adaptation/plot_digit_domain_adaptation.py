"""
Domain adaptation on digit images
=================================

A classifier trained on MNIST does poorly on USPS. Both are handwritten digits, both have ten
classes, and a human sees essentially the same task — but the pixel statistics differ enough that
accuracy drops sharply when the model is moved across. That gap is *domain shift*, and it is the
ordinary situation whenever a model trained on one hospital's scanner, one lab's assay or one
season's imagery meets data from another.

Unsupervised domain adaptation attacks the gap without any target labels. This tutorial trains a
**DANN** (Domain-Adversarial Neural Network) on labelled MNIST plus *unlabelled* USPS. The
mechanism is a second head: alongside the digit classifier sits a *domain discriminator* that tries
to tell source images from target images, and a **gradient reversal layer** sits between it and the
shared feature extractor. The discriminator descends its loss; the feature extractor, seeing a
sign-flipped gradient, *ascends* it. At equilibrium the features carry enough information to
classify digits but not enough to reveal which dataset they came from — and features that look the
same across domains are features the source classifier can reuse on the target.

This tutorial follows the same implementation as the ``digits_dann`` example in this folder: it
reuses the example's :mod:`config` and :mod:`model` modules and its ``configs/tutorial.yaml``, so
the code you read here is the code the full experiment runs — just with a short, three-epoch
configuration so it finishes in minutes on CPU.

.. note::
   For the real experiment (all methods, 120 epochs, several repeats), run the full script in this
   folder::

       python main.py --cfg configs/MN2UP-DANN.yaml --devices 1

   ``configs/`` also holds CDAN and DAN variants. See ``config.py`` for every option.
"""

# %%
# Setup
# -----
# We import the example's own ``config`` and ``model`` modules (the same files ``main.py`` uses)
# alongside PyTorch Lightning and the ``kale`` data loaders. On Colab, the first cell of the
# generated notebook installs PyKale; locally, install it once with ``pip install pykale``.

import matplotlib.pyplot as plt
import pytorch_lightning as pl
import torch
from config import get_cfg_defaults
from model import get_model
from pytorch_lightning.callbacks import ModelCheckpoint, TQDMProgressBar
from pytorch_lightning.loggers import CSVLogger

from kale.loaddata.image_access import DigitDataset
from kale.loaddata.multi_domain import MultiDomainAccess, MultiDomainDataset
from kale.utils.seed import set_seed

# %%
# Configuration
# -------------
# PyKale examples are configuration-driven: a set of typed defaults in ``config.py`` is overridden by
# a small ``.yaml`` for the specific run. Here ``configs/tutorial.yaml`` selects DANN, MNIST → USPS,
# and just three epochs. Reading the frozen config back is a good habit — it is the single record of
# exactly what you ran.

cfg = get_cfg_defaults()
cfg.merge_from_file("./configs/tutorial.yaml")
cfg.freeze()
print(cfg)

# %%
# Device
# ------
# A CUDA GPU accelerates training but is not required — three epochs on this subset run in a couple
# of minutes on CPU.

device = "cuda" if torch.cuda.is_available() else "cpu"
devices = 1 if device == "cuda" else 0
print(f"Using: {device}")

# %%
# Data
# ----
# MNIST is the *source* (labels used) and USPS the *target* (labels withheld during training, used
# only to score the result). ``MultiDomainAccess`` wraps both datasets into one object that yields a
# domain label alongside each image — the adversarial machinery needs to know where each sample came
# from, even though the classifier must not encode it. Both datasets download automatically.

data_src = DigitDataset(cfg.DATASET.SOURCE.upper())
data_tgt = DigitDataset(cfg.DATASET.TARGET.upper())
# USPS and MNIST are single-channel; taking the maximum keeps the code working when you swap in a
# 3-channel pair such as SVHN through the config.
num_channels = max(DigitDataset.get_channel_numbers(data_src), DigitDataset.get_channel_numbers(data_tgt))

data_access = MultiDomainAccess(
    {
        cfg.DATASET.SOURCE.upper(): DigitDataset.get_access(data_src, cfg.DATASET.ROOT)[0],
        cfg.DATASET.TARGET.upper(): DigitDataset.get_access(data_tgt, cfg.DATASET.ROOT)[0],
    },
    cfg.DATASET.NUM_CLASSES,
    return_domain_label=True,
)
dataset = MultiDomainDataset(data_access)
print(f"Source: {cfg.DATASET.SOURCE.upper()}, target: {cfg.DATASET.TARGET.upper()}, channels: {num_channels}")

# %%
# Reproducibility
# ---------------
# ``set_seed`` covers Python, NumPy, torch and cuDNN in one call — worth using rather than seeding by
# hand, because an unseeded cuDNN backend is a common source of results that will not reproduce.

set_seed(cfg.SOLVER.SEED)

# %%
# Model
# -----
# ``get_model`` (from the example's ``model.py``) assembles three pieces from the config: a shared
# ``SmallCNNFeature`` extractor, a ``ClassNetSmallImage`` digit classifier, and — for adversarial
# methods like DANN — a ``DomainNetSmallImage`` critic, wired together with the gradient reversal
# already in place. Reusing ``get_model`` means this tutorial and the full ``main.py`` build *exactly*
# the same model; only the config differs.

model, train_params = get_model(cfg, dataset, num_channels)

# %%
# Training
# --------
# Lightning runs the loop. Watch the *validation* loss rather than the training loss: the adversarial
# term makes the training loss non-monotonic by design, and a rising discriminator loss is a sign the
# adaptation is working, not failing. We use a lightweight ``CSVLogger`` here; the example's
# ``main.py`` uses TensorBoard for richer curves.

logger = CSVLogger(cfg.OUTPUT.OUT_DIR, name=f"seed{cfg.SOLVER.SEED}")
checkpoint_callback = ModelCheckpoint(filename="{epoch}-{step}-{valid_loss:.4f}", monitor="valid_loss", mode="min")
progress_bar = TQDMProgressBar(cfg.OUTPUT.PB_FRESH)

trainer = pl.Trainer(
    min_epochs=cfg.SOLVER.MIN_EPOCHS,
    max_epochs=cfg.SOLVER.MAX_EPOCHS,
    callbacks=[checkpoint_callback, progress_bar],
    logger=logger,
    accelerator="gpu" if devices != 0 else "cpu",
)
trainer.fit(model)

# %%
# Results
# -------
# The number that matters is **target accuracy**. Testing reports several metrics; the key contrast
# is ``test_source_acc`` (how well the model does on data like it trained on) versus
# ``test_target_acc`` (how well it transfers to the unlabelled domain). Source accuracy staying high
# while target accuracy climbs is the healthy pattern.

results = trainer.test(ckpt_path="best")[0]

source_acc = results.get("test_source_acc", 0.0)
target_acc = results.get("test_target_acc", 0.0)
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(["Source (MNIST)", "Target (USPS)"], [source_acc, target_acc], color=["#2563eb", "#dc2626"])
ax.set_ylabel("Accuracy")
ax.set_ylim(0, 1)
ax.set_title(f"MNIST → USPS after {cfg.SOLVER.MAX_EPOCHS} epochs (reduced run)")
for bar, value in zip(bars, [source_acc, target_acc]):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.3f}", ha="center", fontsize=10)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %%
# Reading the metrics:
#
# * ``test_source_acc`` / ``test_target_acc`` — task accuracy on each domain.
# * ``test_domain_acc`` — how well the *discriminator* still tells the domains apart; near 0.5
#   (chance) means the features have become domain-invariant, which is the goal.
# * ``test_task_loss`` / ``test_domain_div_loss`` — the two competing objectives.
#
# With three epochs the gap is visible but not closed. The published MNIST → USPS result reaches
# roughly 95% target accuracy after 120 epochs, against roughly 80% for source-only training.

# %%
# Where to go next
# ----------------
# * Swap ``METHOD: "DANN"`` for ``CDAN`` in ``configs/tutorial.yaml`` to condition the discriminator
#   on the classifier output — usually a clear gain when classes are imbalanced across domains.
# * Change ``DATASET.TARGET`` to ``svhn`` for a much harder shift, where source-only training fails
#   badly enough to make the point on its own.
# * :doc:`Multi-source domain adaptation
#   <../office_multisource_adaptation/plot_office_multisource_adaptation>` extends this to several
#   labelled source domains at once.
#
# **Reference:** Ganin et al. (2016), `Domain-Adversarial Training of Neural Networks
# <https://arxiv.org/abs/1505.07818>`_, JMLR 17(59). Refactored from
# `pytorch-ada <https://github.com/criteo-research/pytorch-ada>`_.
