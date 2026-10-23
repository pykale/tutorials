# Drug-target interaction prediction with DrugBAN

An interpretable bilinear attention network over drug molecular graphs and protein sequences, with optional domain adaptation for cross-domain generalisation on BindingDB and BioSNAP.

> **Note:** the narrated `plot_drug_target_interaction_prediction.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/bindingdb_drugban`](https://github.com/pykale/pykale/tree/main/examples/bindingdb_drugban)
in the PyKale library.

## 2. Usage

* Task: interaction prediction
* Modality: graph, sequence
* Algorithms: DrugBAN, Bilinear attention, CDAN
* Difficulty: advanced
* Hardware: gpu optional — ~2 h on one GPU
* Datasets:
  * [BindingDB (random and cluster splits)](https://github.com/pykale/data/blob/main/molecular/README.md)
  * [BioSNAP (random and cluster splits)](https://github.com/pykale/data/blob/main/molecular/README.md)

```bash
pip install -r requirements.txt
python main.py --cfg configs/non_DA_in_domain.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.model_lib.drugban`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.interpret.visualize`](https://pykale.readthedocs.io/en/latest/kale.interpret.html)
- [`kale.loaddata.molecular_datasets`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.loaddata.sampler`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.drugban_trainer`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.prepdata.tensor_reshape`](https://pykale.readthedocs.io/en/latest/kale.prepdata.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://www.nature.com/articles/s42256-022-00605-1>
2. <https://github.com/peizhenbai/DrugBAN>
