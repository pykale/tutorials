# Drug-target affinity prediction with DeepDTA

Predict binding affinity between compounds and protein targets by encoding SMILES strings and amino-acid sequences with parallel CNNs, on three BindingDB subsets (Kd, IC50, Ki).

> **Note:** the narrated `plot_drug_target_affinity_prediction.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/bindingdb_deepdta`](https://github.com/pykale/pykale/tree/main/examples/bindingdb_deepdta)
in the PyKale library.

## 2. Usage

* Task: affinity prediction
* Modality: sequence
* Algorithms: DeepDTA
* Difficulty: intermediate
* Hardware: gpu optional — ~1 h on one GPU
* Datasets:
  * [BindingDB Kd](https://tdcommons.ai/)
  * [BindingDB IC50](https://tdcommons.ai/)
  * [BindingDB Ki](https://tdcommons.ai/)

```bash
pip install -r requirements.txt
python main.py --cfg configs/Kd-DeepDTA.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.tdc_datasets`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.deepdta`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.decode`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://academic.oup.com/bioinformatics/article/34/17/i821/5093245>
