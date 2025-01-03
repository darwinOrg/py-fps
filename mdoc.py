import os.path
import subprocess

from weasyprint import HTML


def convert_file_format(input_path: str, output_path: str, output_format: str):
    if os.path.exists(output_path):
        return

    if output_format == 'md' or output_format == 'markdown':
        subprocess.run(['pandoc', '--toc', input_path, '-o', output_path],
                       check=True, capture_output=True, text=True, timeout=60)
        return

    if input_path.endswith('html') and output_format == 'pdf':
        with open(input_path) as f:
            HTML(string=f.read()).write_pdf(output_path)
            return

    subprocess.run(['unoconvert', '--convert-to', output_format, input_path, output_path],
                   check=True, capture_output=True, text=True, timeout=60)
