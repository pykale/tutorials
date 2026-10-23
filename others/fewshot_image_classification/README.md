# Few-shot image classification with ProtoNet

Prototypical Networks under N-way K-shot settings. Learn an embedding where class prototypes are the mean of their support samples, then classify query samples by distance to those prototypes.

> **Note:** the narrated `plot_fewshot_image_classification.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/fewshot_protonet`](https://github.com/pykale/pykale/tree/main/examples/fewshot_protonet)
in the PyKale library.

## 2. Usage

* Task: few-shot classification
* Modality: image
* Algorithms: ProtoNet
* Difficulty: intermediate
* Hardware: gpu optional — ~30 min on one GPU
* Datasets:
  * [Omniglot](https://github.com/brendenlake/omniglot)
  * [mini-ImageNet](https://www.kaggle.com/datasets/arjunashok33/miniimagenet)
  * [tiered-ImageNet](https://www.kaggle.com/datasets/arjun2000ashok/tieredimagenet)

```bash
pip install -r requirements.txt
python main.py --cfg configs/demo.yaml --gpus 1
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.image_cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.few_shot`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.fewshot_trainer`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.prepdata.image_transform`](https://pykale.readthedocs.io/en/latest/kale.prepdata.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://arxiv.org/abs/1703.05175>
2. <https://github.com/jakesnell/prototypical-networks>
