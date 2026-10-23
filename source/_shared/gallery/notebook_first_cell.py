"""The install cell prepended to every notebook sphinx-gallery generates.

Colab has no PyKale preinstalled and a stale pip; Binder builds from the repo and needs nothing. The
cell therefore detects Colab and no-ops elsewhere, so the same notebook works in both places and
locally.
"""

from __future__ import annotations

INSTALL_CELL = """\
# Run this cell first if you are on Google Colab. It is a no-op elsewhere.
import importlib.util
import sys

if "google.colab" in sys.modules and importlib.util.find_spec("kale") is None:
    !pip install --quiet git+https://github.com/pykale/pykale.git
    print("PyKale installed. If imports fail, restart the runtime and re-run this cell.")
"""


def notebook_header(extra_packages: tuple[str, ...] = ()) -> str:
    """Return the first-cell source, optionally installing tutorial-specific extras.

    ``extra_packages`` covers tutorials whose ``requirements.txt`` lists dependencies beyond the
    PyKale core -- rdkit and PyTDC being the usual offenders.
    """
    if not extra_packages:
        return INSTALL_CELL
    packages = " ".join(extra_packages)
    return INSTALL_CELL.replace(
        "    print(",
        f"    !pip install --quiet {packages}\n    print(",
    )
