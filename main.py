"""Entry point for makefun news-image-20261118 competition.

Copies the generated picture.png to <MAKEFUN_OUTPUT_DIR>/entry.png.
Standard library only, deterministic, no network, no clock reads.
"""

import os
import shutil
import sys


def main():
    # Determine output directory: MAKEFUN_OUTPUT_DIR env var or /output default
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    # Locate source picture.png in this script's directory
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "picture.png")
    dest_path = os.path.join(output_dir, "entry.png")

    if not os.path.exists(src_path):
        sys.stderr.write(f"Source image not found: {src_path}\n")
        sys.exit(1)

    # Copy picture.png to destination entry.png unchanged
    shutil.copyfile(src_path, dest_path)

    # Verification robustness check: verify destination exists and size matches source
    src_size = os.path.getsize(src_path)
    dest_size = os.path.getsize(dest_path)
    if src_size != dest_size:
        sys.stderr.write(f"Size mismatch: src={src_size} vs dest={dest_size}\n")
        sys.exit(1)

    print(f"Copied {src_path} ({src_size} bytes) -> {dest_path} successfully.")


if __name__ == "__main__":
    main()
