"""Print the tutorials that are safe to execute on a CPU-only runner.

The nightly CI job (see ``.github/workflows/docs.yml``) installs each runnable tutorial's
``requirements.txt`` before the executing build, so the reference narratives run with their real
dependencies. ``--requirements`` prints those paths; the default prints tutorial directories.

    python scripts/list_runnable.py                 # tutorial dirs, one per line
    python scripts/list_runnable.py --requirements  # their requirements.txt paths (skips missing)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from models import REPO_ROOT, Catalog, TutorialMetadata


def runnable_paths() -> list[str]:
    """List repo-relative paths of every tutorial whose narrative may be executed.

    Returns:
        list[str]: Directories of runnable tutorials, in catalog order.
    """
    paths: list[str] = []
    for path in Catalog.load().iter_relative_paths():
        metadata = TutorialMetadata.model_validate(
            yaml.safe_load((REPO_ROOT / path / "metadata.yml").read_text(encoding="utf-8"))
        )
        if metadata.is_runnable:
            paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--requirements",
        action="store_true",
        help="print each runnable tutorial's requirements.txt path instead of its directory",
    )
    args = parser.parse_args()

    for path in runnable_paths():
        if args.requirements:
            req = Path(path) / "requirements.txt"
            if (REPO_ROOT / req).exists():
                print(req.as_posix())
        else:
            print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
