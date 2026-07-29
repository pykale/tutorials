"""Shared pytest fixtures and environment setup.

Force a headless matplotlib backend before anything imports pyplot. The reference tutorial (and the
gallery build) import matplotlib; on a machine with no display an interactive backend makes the suite
hang or raise ``_tkinter.TclError`` -- a documented pykale CI trap. Setting it here covers every test
regardless of import order.
"""

from __future__ import annotations

import os

os.environ.setdefault("MPLBACKEND", "Agg")
