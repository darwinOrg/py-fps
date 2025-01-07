import os.path
import subprocess

from weasyprint import HTML


def convert_file_format(input_path: str, output_path: str):
    if os.path.exists(output_path):
        return

    _, output_ext = os.path.splitext(output_path)

    if input_path.endswith('.html') and output_ext == '.pdf':
        with open(input_path) as f:
            HTML(string=f.read()).write_pdf(output_path)
            return

    if output_ext == '.md':
        subprocess.run(['pandoc', '--toc', input_path, '-o', output_path],
                       check=True, capture_output=True, text=True, timeout=60)
        return

    output_format = output_ext[1:]
    subprocess.run(['unoconvert', '--convert-to', output_format, input_path, output_path],
                   check=True, capture_output=True, text=True, timeout=60)
