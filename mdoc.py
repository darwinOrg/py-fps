import os.path
import pathlib
import subprocess

from weasyprint import HTML

use_uno = os.getenv("USE_UNO") == 'true'


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

    if use_uno:
        subprocess.run(['unoconvert', '--convert-to', output_format, input_path, output_path],
                       check=True, capture_output=True, text=True, timeout=60)
    else:
        out_dir = os.path.dirname(output_path)
        subprocess.run(['soffice', '--headless', '--convert-to', output_format, input_path, '--outdir', out_dir],
                       check=True, capture_output=True, text=True, timeout=60)
        converted_path = os.path.join(out_dir, pathlib.Path(input_path).stem + output_ext)
        if converted_path != output_path:
            os.rename(converted_path, output_path)
