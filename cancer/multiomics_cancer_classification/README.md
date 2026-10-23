# Multiomics cancer classification with MOGONET

Integrate mRNA expression, DNA methylation and miRNA expression with per-omics graph convolutional networks, fusing their predictions through a view-correlation discovery network.

> **Note:** the narrated `plot_multiomics_cancer_classification.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/multiomics_mogonet`](https://github.com/pykale/pykale/tree/main/examples/multiomics_mogonet)
in the PyKale library.

## 2. Usage

* Task: classification
* Modality: omics, graph
* Algorithms: MOGONET, Graph convolutional network, VCDN
* Difficulty: advanced
* Hardware: gpu optional — ~10 min on one GPU
* Datasets:
  * [BRCA (breast cancer subtypes)](https://github.com/pykale/data/tree/main/multiomics)
  * [ROSMAP (Alzheimer's disease)](https://github.com/pykale/data/tree/main/multiomics)

```bash
pip install -r requirements.txt
python main.py --cfg configs/MOGONET_BRCA_quick_test.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.model_lib.mogonet`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.interpret.model_weights`](https://pykale.readthedocs.io/en/latest/kale.interpret.html)
- [`kale.loaddata.multiomics_datasets`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.multiomics_trainer`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.decode`](https://pykale.readthedocs.io/en/latest/kale.predict.html)
- [`kale.prepdata.tabular_transform`](https://pykale.readthedocs.io/en/latest/kale.prepdata.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://doi.org/10.1038/s41467-021-23774-w>
2. <https://github.com/txWang/MOGONET>
