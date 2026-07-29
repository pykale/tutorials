# Multi-source domain adaptation on Office

Adapt from three labelled source domains to one unlabelled target using moment matching (M3SDA) and multiple feature-space alignment (MFSAN), on Office-Caltech and digits.

> **Note:** the narrated `tutorial.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/office_multisource_adapt`](https://github.com/pykale/pykale/tree/main/examples/office_multisource_adapt)
in the PyKale library.

## 2. Usage

* Task: image classification
* Modality: image
* Algorithms: M3SDA, MFSAN
* Difficulty: intermediate
* Hardware: gpu optional — ~30 min on one GPU
* Datasets:
  * [Office-Caltech](https://github.com/pykale/data/tree/main/images/office)
  * [Office-31](https://github.com/pykale/data/tree/main/images/office)
  * [Digits (MNIST, MNIST-M, USPS, SVHN)](https://github.com/pykale/data)

```bash
pip install -r requirements.txt
python main.py --cfg configs/Office2A-M3SDA.yaml --devices 1
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.image_cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.image_access`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.loaddata.multi_domain`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.multi_domain_adapter`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.class_domain_nets`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://openaccess.thecvf.com/content_ICCV_2019/html/Peng_Moment_Matching_for_Multi-Source_Domain_Adaptation_ICCV_2019_paper.html>
2. <https://ojs.aaai.org/index.php/AAAI/article/view/4551>
