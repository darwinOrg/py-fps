import os.path
import pathlib
import subprocess

from pyppeteer import launch

use_uno = os.getenv("USE_UNO") == 'true'


def convert_file_format(input_path: str, output_path: str):
    if os.path.exists(output_path):
        return

    _, output_ext = os.path.splitext(output_path)

    if output_ext == '.md' or (input_path.endswith('.html') and output_ext == '.docx'):
        subprocess.run(['pandoc', input_path, '-o', output_path],
                       check=True, capture_output=True, text=True, timeout=60)
        return

    if input_path.endswith('.html') and output_ext == '.pdf':
        browser = launch(headless=True)
        page = browser.newPage()
        page.goto(f'file://{input_path}')
        page.pdf(path=output_path, format='A4', printBackground=True)
        browser.close()
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
