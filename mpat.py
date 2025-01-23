import os

import patoolib


def extract_archive(input_path: str, output_dir: str):
    # Ensure the destination directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract the archive using patoolib
    patoolib.extract_archive(input_path, outdir=output_dir)
    print(f"Successfully extracted {input_path} into {output_dir}")
