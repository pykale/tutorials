# Polypharmacy side effect prediction with GripNet

Link prediction on a protein-drug knowledge graph. GripNet propagates messages along a task-specific path over a supergraph to predict side effects caused by drug combinations.

> **Note:** the narrated `tutorial.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/polypharmacy_gripnet`](https://github.com/pykale/pykale/tree/main/examples/polypharmacy_gripnet)
in the PyKale library.

## 2. Usage

* Task: link prediction
* Modality: graph
* Algorithms: GripNet
* Difficulty: advanced
* Hardware: gpu optional — ~15 min on one GPU
* Datasets:
  * [PoSE (mini subset of the Decagon knowledge graph)](https://github.com/pykale/data/tree/main/graphs)

```bash
pip install -r requirements.txt
python main.py --cfg configs/PoSE_MINI-GripNet.yaml
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.loaddata.polypharmacy_datasets`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.predict.decode`](https://pykale.readthedocs.io/en/latest/kale.predict.html)
- [`kale.prepdata.supergraph_construct`](https://pykale.readthedocs.io/en/latest/kale.prepdata.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://doi.org/10.1016/j.patcog.2022.108973>
2. <https://academic.oup.com/bioinformatics/article/34/13/i457/5045770>
