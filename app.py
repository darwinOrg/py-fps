import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from mdoc import convert_file_format
from mimg import pdf_to_image, pdf_to_pngs, compress_image, pdf_image_count
from mpat import extract_archive
from mpdf import extract_pdf_text_speed
from result import Result

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=100)


class ConvertFileFormatReq(BaseModel):
    input_path: str
    output_path: str


class ExtractPdfTextReq(BaseModel):
    pdf_path: str
    output_dir: str
    word_count_min: int = 80
    max_page: int = 8
    parse_method: Optional[str] = 'auto'


class PdfToImageReq(BaseModel):
    pdf_path: str
    output_dir: str
    max_page: int
    target_size: int


class PdfToPngsReq(BaseModel):
    pdf_path: str
    output_dir: str


class CompressImageReq(BaseModel):
    input_path: str
    output_path: str
    target_size: int


class PdfImageCountReq(BaseModel):
    pdf_path: str


class ExtractArchiveReq(BaseModel):
    input_path: str
    output_dir: str


@app.post('/convert-file-format')
async def convert_file_format_api(req: ConvertFileFormatReq):
    await asyncio.get_event_loop().run_in_executor(
        executor,
        convert_file_format,
        req.input_path,
        req.output_path)
    return JSONResponse(Result.success().to_dict(), status_code=200)


@app.post('/extract-pdf-text-speed')
async def extract_pdf_text_speed_api(req: ExtractPdfTextReq):
    text_path = await asyncio.get_event_loop().run_in_executor(
        executor,
        extract_pdf_text_speed,
        req.pdf_path,
        req.output_dir,
        req.word_count_min,
        req.max_page
    )
    return JSONResponse(Result.success(text_path).to_dict(), status_code=200)


@app.post('/pdf-to-image')
async def pdf_to_image_api(req: PdfToImageReq):
    image_path = await asyncio.get_event_loop().run_in_executor(
        executor,
        pdf_to_image,
        req.pdf_path,
        req.output_dir,
        req.max_page,
        req.target_size
    )
    return JSONResponse(Result.success(image_path).to_dict(), status_code=200)


@app.post('/pdf-to-pngs')
async def pdf_to_pngs_api(req: PdfToPngsReq):
    pngs = await asyncio.get_event_loop().run_in_executor(
        executor,
        pdf_to_pngs,
        req.pdf_path,
        req.output_dir,
    )
    return JSONResponse(Result.success(pngs).to_dict(), status_code=200)


@app.post('/compress-image')
async def compress_image_api(req: CompressImageReq):
    await asyncio.get_event_loop().run_in_executor(
        executor,
        compress_image,
        req.input_path,
        req.output_path,
        req.target_size
    )
    return JSONResponse(Result.success().to_dict(), status_code=200)


@app.post('/pdf-image-count')
async def pdf_image_count_api(req: PdfImageCountReq):
    image_count = await asyncio.get_event_loop().run_in_executor(
        executor,
        pdf_image_count,
        req.pdf_path
    )
    return JSONResponse(Result.success(image_count).to_dict(), status_code=200)


@app.post('/extract-archive')
async def extract_archive_api(req: ExtractArchiveReq):
    await asyncio.get_event_loop().run_in_executor(
        executor,
        extract_archive,
        req.input_path,
        req.output_dir
    )
    return JSONResponse(Result.success().to_dict(), status_code=200)


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, e: Exception):
    logger.error(f"Unhandled exception occurred: {e}")
    return JSONResponse(Result.fail(str(e)).to_dict(), status_code=200)


if __name__ == '__main__':
    port = os.getenv('FPS_PORT', '9999')
    uvicorn.run(app, host='0.0.0.0', port=int(port))
