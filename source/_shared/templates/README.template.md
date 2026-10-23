# {{ TITLE }}

{{ One or two sentences. Same content as `summary:` in metadata.yml. }}

## 1. Description

{{ The problem, the method, and the reason they fit together. Cite the paper this refactors, if any. }}

## 2. Usage

* Datasets: {{ names, with links }}
* Algorithms: {{ methods }}
* Example: {{ the specific configuration the command below runs }}

```bash
{{ RUN_COMMAND }}
```

See [`config.py`](./config.py) for all configuration options, and [`configs/`](./configs) for
ready-made variants.

## 3. Related `kale` API

{{ One line per module, saying what it does *here* rather than restating its docstring. }}

`kale.module.name`: {{ what it does in this tutorial }}

## 4. Sample output

{{ A table or figure from a real run, with the hardware and epoch count stated. Omit the section
rather than inventing numbers. }}

## References

{{ [1] Author, A. (Year). Title. Venue. }}
