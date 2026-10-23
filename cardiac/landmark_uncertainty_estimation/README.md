# Uncertainty estimation for landmark localisation

Quantile Binning sorts landmark predictions into bins of increasing uncertainty with estimated error bounds, so the least reliable predictions can be filtered out before they are acted on.

> **Note:** the narrated `plot_landmark_uncertainty_estimation.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/landmark_uncertainty`](https://github.com/pykale/pykale/tree/main/examples/landmark_uncertainty)
in the PyKale library.

## 2. Usage

* Task: uncertainty estimation
* Modality: tabular
* Algorithms: Quantile Binning, S-MHA, E-MHA, E-CPV
* Difficulty: intermediate
* Hardware: cpu — ~5 min on CPU
* Datasets:
  * [Short-axis CMR landmarks (303 images, 3 landmarks)](https://github.com/pykale/data/tree/main/tabular/cardiac_landmark_uncertainty)
  * [Four-chamber CMR landmarks (422 images, 3 landmarks)](https://github.com/pykale/data/tree/main/tabular/cardiac_landmark_uncertainty)
  * [Cephalometric radiographs (400 images, 19 landmarks)](https://github.com/pykale/data/tree/main/tabular/cardiac_landmark_uncertainty)

```bash
pip install -r requirements.txt
python main.py --cfg configs/SA_data.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.uncertainty_fitting`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.interpret.uncertainty_quantiles`](https://pykale.readthedocs.io/en/latest/kale.interpret.html)
- [`kale.utils.download`](https://pykale.readthedocs.io/en/latest/kale.utils.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://arxiv.org/abs/2203.02351>
2. <https://github.com/Schobs/Qbin>
