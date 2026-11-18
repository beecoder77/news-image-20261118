#!/usr/bin/env python3
"""Entry point for the news-image-20261118 bounty.

Copies this repository's entry.png into the output directory named by
the MAKEFUN_OUTPUT_DIR environment variable. Standard library only;
no network, no extra work, so both grader runs produce identical bytes.
"""

import os
import shutil
from pathlib import Path


def main():
    out_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    out_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "entry.png"
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
