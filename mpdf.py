import os
import pathlib

import fitz
from loguru import logger
from pdfminer.high_level import extract_text

output_txt_filename = 'cv.txt'

special_char_map = {
    0xA728: "TZ",
    0xA729: "tz",
    0xA732: "AA",
    0xA733: "aa",
    0xA734: "AO",
    0xA735: "ao",
    0xA736: "AU",
    0xA737: "au",
    0xA738: "AV",
    0xA739: "av",
    0xA73A: "AV",
    0xA73B: "av",
    0xA73C: "AY",
    0xA73D: "ay",
    0xA74E: "OO",
    0xA74F: "oo",
    0xA760: "VY",
    0xA761: "vy",
    0xFB00: "ff",
    0xFB01: "fi",
    0xFB02: "fl",
    0xFB03: "ffi",
    0xFB04: "ffl",
    0xFB05: "ft",
    0xFB06: "st"
}


def extract_pdf_text_speed(pdf_path: str, output_dir: str, word_count_min: int, max_page: int) -> str:
    pdf_path = truncate_pdf_over_pages(pdf_path, output_dir, max_page)
    extracted_text = extract_text(pdf_path).strip()
    if len(extracted_text) < word_count_min:
        return ''
    processed_text = replace_spec_chars(extracted_text)
    text_path = os.path.join(output_dir, output_txt_filename)
    with open(text_path, 'w') as f:
        f.write(processed_text)
    logger.info(f'extract_pdf_text_simply({pdf_path} -> {text_path}) success')
    return text_path


def truncate_pdf_over_pages(input_pdf_path: str, output_dir: str, max_page: int) -> str:
    with fitz.open(input_pdf_path) as doc:
        total_pages = len(doc)
        if total_pages <= max_page:
            return input_pdf_path

        with fitz.open() as new_doc:
            for page_num in range(min(max_page, total_pages)):
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            output_pdf_path = str(
                pathlib.Path(output_dir).joinpath(pathlib.Path(input_pdf_path).stem + "_truncated.pdf"))
            new_doc.save(output_pdf_path)
            print(f"Truncated document to {max_page} pages and saved as {output_pdf_path}.")
            return output_pdf_path


def replace_spec_chars(raw) -> str:
    if not raw:
        return raw

    result = []

    for c in raw:
        r = special_char_map.get(ord(c))
        if r is None:
            result.append(c)
        else:
            result.append(r)

    return ''.join(result)
