# Domain adaptation on digit images

Adapt a digit classifier from MNIST to USPS without target labels, comparing adversarial and discrepancy-based methods. The reference tutorial for domain adaptation in PyKale.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/digits_dann`](https://github.com/pykale/pykale/tree/main/examples/digits_dann)
in the PyKale library.

## 2. Usage

* Task: image classification
* Modality: image
* Algorithms: DANN, CDAN, DAN, JAN, WDGRL, MME
* Difficulty: beginner
* Hardware: gpu optional — ~20 min on one GPU
* Datasets:
  * [MNIST](https://yann.lecun.com/exdb/mnist/)
  * [USPS](https://git-disl.github.io/GTDLBench/datasets/usps_dataset/)
  * [MNIST-M](https://github.com/zumpchke/keras_mnistm)

```bash
pip install -r requirements.txt
python main.py --cfg configs/MN2UP-DANN.yaml --devices 1
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.image_cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.image_access`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.loaddata.multi_domain`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.domain_adapter`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.class_domain_nets`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://arxiv.org/abs/1505.07818>
2. <https://github.com/criteo-research/pytorch-ada>
