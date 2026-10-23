# Multi-site neuroimaging classification

Autism detection from resting-state fMRI pooled across four ABIDE acquisition sites, using CoIRLS to regularise away site-driven covariate shift.

> **Note:** the narrated `plot_multisite_neuroimaging_classification.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/multisite_neuroimg_adapt`](https://github.com/pykale/pykale/tree/main/examples/multisite_neuroimg_adapt)
in the PyKale library.

## 2. Usage

* Task: classification
* Modality: neuroimaging, tabular
* Algorithms: CoIRLS, Ridge classifier
* Difficulty: intermediate
* Hardware: cpu — ~5 min on CPU
* Datasets:
  * [ABIDE I (NYU, UM_1, UCLA_1, USM; CC200 atlas, cpac pipeline)](https://fcon_1000.projects.nitrc.org/indi/abide/)

```bash
pip install -r requirements.txt
python main.py --cfg configs/tutorial.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.evaluate.cross_validation`](https://pykale.readthedocs.io/en/latest/kale.evaluate.html)
- [`kale.pipeline.multi_domain_adapter`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://doi.org/10.3389/conf.fninf.2013.09.00041>
2. <https://doi.org/10.1609/aaai.v34i04.6179>
