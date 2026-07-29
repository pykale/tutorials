# Cardiac MRI diagnosis with multilinear PCA

Diagnose pulmonary arterial hypertension from short-axis cardiac MRI. MPCA keeps the tensor structure of the image stack intact, and the learned weights map back onto the anatomy.

> **Note:** the narrated `tutorial.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/cmri_mpca`](https://github.com/pykale/pykale/tree/main/examples/cmri_mpca)
in the PyKale library.

## 2. Usage

* Task: diagnosis
* Modality: image
* Algorithms: MPCA, Linear SVM, Kernel SVM, Logistic regression
* Difficulty: intermediate
* Hardware: cpu — ~5 min on CPU
* Datasets:
  * [ShefPAH-179 v2.0 (short-axis cardiac MRI)](https://github.com/pykale/data/tree/main/images/ShefPAH-179)

```bash
pip install -r requirements.txt
python main.py --cfg configs/tutorial_svc.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.interpret.model_weights`](https://pykale.readthedocs.io/en/latest/kale.interpret.html)
- [`kale.interpret.visualize`](https://pykale.readthedocs.io/en/latest/kale.interpret.html)
- [`kale.loaddata.image_access`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.mpca_trainer`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.prepdata.image_transform`](https://pykale.readthedocs.io/en/latest/kale.prepdata.html)
- [`kale.utils.download`](https://pykale.readthedocs.io/en/latest/kale.utils.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://academic.oup.com/ehjcimaging/article/22/2/236/5717931>
