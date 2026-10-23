# CIFAR classification with ISONet

Deep isometric learning on CIFAR-10/100. ISONet trains very deep networks without residual connections or batch normalisation by keeping the layer-wise transform close to an isometry.

> **Note:** the narrated `plot_cifar_isonet.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/cifar_isonet`](https://github.com/pykale/pykale/tree/main/examples/cifar_isonet)
in the PyKale library.

## 2. Usage

* Task: image classification
* Modality: image
* Algorithms: ISONet
* Difficulty: intermediate
* Hardware: gpu optional — ~2 h on one GPU
* Datasets:
  * [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html)
  * [CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html)

```bash
pip install -r requirements.txt
python main.py --cfg configs/CF10-ISO38.yaml --output CF10-ISO38
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.loaddata.image_access`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.predict.isonet`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <http://proceedings.mlr.press/v119/qi20a.html>
2. <https://github.com/HaozhiQi/ISONet>
