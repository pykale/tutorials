# Efficient video data loading

Load, sample and augment video datasets with VideoFrameDataset. Sparse temporal sampling keeps memory flat regardless of clip length, and the loader plugs straight into torch DataLoader.

> **Note:** the narrated `plot_video_data_loading.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/video_loading`](https://github.com/pykale/pykale/tree/main/examples/video_loading)
in the PyKale library.

## 2. Usage

* Task: data loading
* Modality: video
* Algorithms: Sparse temporal sampling
* Difficulty: beginner
* Hardware: cpu — <1 min on CPU
* Datasets:
  * Demo frame dataset (dummy, two classes)

```bash
pip install -r requirements.txt
python main.py
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.loaddata.videos`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.prepdata.video_transform`](https://pykale.readthedocs.io/en/latest/kale.prepdata.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://arxiv.org/abs/1608.00859>
2. <https://github.com/yjxiong/tsn-pytorch>
