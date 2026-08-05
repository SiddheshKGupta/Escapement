#!/usr/bin/env python3
"""Deprecated compatibility wrapper for Escapement v6."""

from __future__ import annotations

import runpy
import warnings
from pathlib import Path

warnings.warn(
    "scripts/vlco_build.py is deprecated; use scripts/escapement.py.",
    DeprecationWarning,
    stacklevel=1,
)
runpy.run_path(
    str(Path(__file__).with_name("escapement.py")),
    run_name="__main__",
)
