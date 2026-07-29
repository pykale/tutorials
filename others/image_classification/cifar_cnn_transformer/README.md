# CIFAR-10 classification with a CNN-Transformer

Train an 8-layer CNN on CIFAR-10 as a baseline, then stack a Transformer encoder on the same backbone and compare validation accuracy across four Transformer sizes.

> **Note:** the narrated `tutorial.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/cifar_cnntransformer`](https://github.com/pykale/pykale/tree/main/examples/cifar_cnntransformer)
in the PyKale library.

## 2. Usage

* Task: image classification
* Modality: image
* Algorithms: SimpleCNN, CNNTransformer
* Difficulty: beginner
* Hardware: gpu optional — ~45 min on one GPU
* Datasets:
  * [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html)

```bash
pip install -r requirements.txt
python main.py --cfg configs/CF10-CNNTransformer.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.embed.image_cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.image_access`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.base_nn_trainer`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.class_domain_nets`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://arxiv.org/abs/1706.03762>
