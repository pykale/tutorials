# Domain adaptation on synthetic data

The smallest possible domain adaptation example. Two blob-generated domains, two classes, and a CoIRLS classifier -- runs in seconds and makes the covariate-shift problem visible in one plot.

> **Note:** the narrated `plot_synthetic_domain_adaptation.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/toy_domain_adaptation`](https://github.com/pykale/pykale/tree/main/examples/toy_domain_adaptation)
in the PyKale library.

## 2. Usage

* Task: classification
* Modality: tabular
* Algorithms: CoIRLS
* Difficulty: beginner
* Hardware: cpu — <1 min on CPU
* Datasets:
  * Synthetic blobs (sklearn.datasets.make_blobs)

```bash
pip install -r requirements.txt
python main.py
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.interpret.visualize`](https://pykale.readthedocs.io/en/latest/kale.interpret.html)
- [`kale.pipeline.multi_domain_adapter`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://ojs.aaai.org//index.php/AAAI/article/view/6179>
