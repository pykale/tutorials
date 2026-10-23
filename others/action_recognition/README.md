# Domain adaptation for action recognition

Transfer an action recogniser between egocentric video domains. Same adversarial adaptation pipeline as the digits tutorial, with a 3D-CNN feature extractor and video data loaders.

> **Note:** the narrated `plot_action_recognition.py` in this folder is still a stub. The example below
> is complete and runnable.

## 1. Description

See [`README.upstream.md`](./README.upstream.md) for the original example write-up, including
method background, architecture diagrams and reference results.

Migrated from [`examples/action_dann`](https://github.com/pykale/pykale/tree/main/examples/action_dann)
in the PyKale library.

## 2. Usage

* Task: action recognition
* Modality: video
* Algorithms: DANN, CDAN, DAN, I3D, R3D
* Difficulty: advanced
* Hardware: gpu required — several hours on one GPU
* Datasets:
  * [EPIC-Kitchens (D1, D2, D3)](https://epic-kitchens.github.io/)
  * ADL (P4, P6, P11)
  * GTEA
  * KITCHEN

```bash
pip install -r requirements.txt
python main.py --cfg configs/EPIC-D12D2-DANN.yaml --devices 1
```

See `configs/` for ready-made variants.

## 3. Related `kale` API

- [`kale.embed.video.feature_extractor`](https://pykale.readthedocs.io/en/latest/kale.embed.html)
- [`kale.loaddata.video_access`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.loaddata.video_multi_domain`](https://pykale.readthedocs.io/en/latest/kale.loaddata.html)
- [`kale.pipeline.domain_adapter`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.pipeline.video_domain_adapter`](https://pykale.readthedocs.io/en/latest/kale.pipeline.html)
- [`kale.predict.class_domain_nets`](https://pykale.readthedocs.io/en/latest/kale.predict.html)

## 4. Sample output

See [`README.upstream.md`](./README.upstream.md).

## References

1. <https://github.com/criteo-research/pytorch-ada>
