import os
import pathlib

import fitz
from loguru import logger


def pdf_to_image(pdf_path: str, output_dir: str, max_page: int, target_size: int) -> str:
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    png_output_path = os.path.join(output_dir, f"{base_name}.png")
    jpeg_output_path = os.path.join(output_dir, f"{base_name}.jpg")

    images = []
    total_height = 0
    max_width = 0

    document = fitz.open(pdf_path)
    page_len = min(len(document), max_page)

    for page_num in range(page_len):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        images.append(img)

        total_height += img.size[1]
        max_width = max(max_width, img.size[0])

    document.close()
    merged_image = Image.new('RGB', (max_width, total_height), color='white')
    current_height = 0

    for img in images:
        # 如果页面宽度小于最大宽度，则需要创建一个白色背景的图像来填充
        if img.size[0] < max_width:
            new_img = Image.new('RGB', (max_width, img.size[1]), color='white')
            new_img.paste(img, (0, 0))
            img = new_img

        merged_image.paste(img, (0, current_height))
        current_height += img.size[1]
        img.close()

    # 灰度化
    with merged_image.convert('L') as gray_img:
        merged_image.close()
        gray_img.save(png_output_path, "PNG")
        pic_size = os.path.getsize(png_output_path)
        if pic_size <= target_size:
            logger.info(f'pdf_to_image({pdf_path} -> {png_output_path}) success')
            return png_output_path

        for i in range(1, 19):
            quality = (10 - i) * 10 if i < 10 else 19 - i
            gray_img.save(png_output_path, "PNG", quality=quality)
            pic_size = os.path.getsize(png_output_path)
            if pic_size <= target_size:
                logger.info(f'pdf_to_image({pdf_path} -> {png_output_path}) success')
                return png_output_path

        os.remove(png_output_path)

        # 如果PNG失败，尝试保存为JPEG
        for i in range(1, 19):
            quality = (10 - i) * 10 if i < 10 else 19 - i
            gray_img.save(jpeg_output_path, "JPEG", quality=quality)
            pic_size = os.path.getsize(jpeg_output_path)
            if pic_size <= target_size:
                logger.info(f'pdf_to_image({pdf_path} -> {jpeg_output_path}) success')
                return jpeg_output_path

    return ''


def pdf_to_pngs(pdf_path: str, output_dir: str) -> list[str]:
    document = fitz.open(pdf_path)
    pp = pathlib.Path(pdf_path)
    pngs = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        output_image_path = f"{output_dir}/{pp.stem}_{page_num + 1}.png"
        pix.save(output_image_path)
        pngs.append(output_image_path)

    return pngs


def compress_image(input_path: str, output_path: str, target_size: int):
    with Image.open(input_path) as img:
        # 如果图像是 RGBA 模式，则转换为 RGB 模式
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGB')

        # 灰度化
        img = img.convert('L')

        for i in range(1, 19):
            quality = (10 - i) * 10 if i < 10 else 19 - i
            img.save(output_path, "JPEG", quality=quality)
            pic_size = os.path.getsize(output_path)
            if pic_size < target_size:
                break

    logger.info(f'compress_image({input_path} -> {output_path}) success')


def pdf_image_count(pdf_path: str) -> int:
    with fitz.open(pdf_path) as document:
        total_images = 0

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            images = page.get_images(full=True)

            if images:
                total_images += len(images)

        logger.info(f'pdf_image_count({pdf_path} -> {total_images}) success')
        return total_images


from PIL import Image


def merge_images_horizontally(img_paths: list[str], output_path: str):
    images = [Image.open(x) for x in img_paths]

    # 计算总宽度和最大高度
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    new_img = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.width

    new_img.save(output_path)


def merge_images_vertically(img_paths: list[str], output_path: str):
    images = [Image.open(x) for x in img_paths]

    # 计算总高度和最大宽度
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights)
    max_width = max(widths)

    new_img = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for img in images:
        new_img.paste(img, (0, y_offset))
        y_offset += img.height

    new_img.save(output_path)
