import os

import patoolib

# 设置环境变量以支持GBK编码（适用于Linux和macOS）
os.environ['LANG'] = 'zh_CN.GBK'
os.environ['LC_ALL'] = 'zh_CN.GBK'


def extract_archive(input_path: str, output_dir: str):
    # Ensure the destination directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract the archive using patoolib
    patoolib.extract_archive(input_path, outdir=output_dir)
    print(f"Successfully extracted {input_path} into {output_dir}")
