# Audio-visual digit classification

Classify spoken-and-written digits from paired audio and image inputs, comparing late fusion, low-rank tensor fusion and bimodal interaction fusion on AVMNIST.

> **Note:** the narrated `plot_audio_visual_digit_classification.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/avmnist_multimodal`](https://github.com/pykale/pykale/tree/main/examples/avmnist_multimodal)
in the PyKale library.

## 2. Usage

* Task: multimodal classification
* Modality: image, audio
* Algorithms: Multimodal Neural Network, Late fusion, Low-rank tensor fusion, Bimodal interaction fusion
* Difficulty: intermediate
* Hardware: cpu — ~10 min on CPU
* Datasets:
  * [AVMNIST (subset, labels 0 and 1)](https://drive.google.com/file/d/1N5k-LvLwLbPBgn3GdVg6fXMBIR6pYrKb/view)

```bash
pip install -r requirements.txt
python main.py --cfg configs/late_fusion.yaml --output AVMNIST-LATE
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.image_cnn`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.embed.multimodal_fusion`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.avmnist_datasets`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.base_nn_trainer`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.decode`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://github.com/pliang279/MultiBench>
