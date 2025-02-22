import os
import tempfile
import subprocess
import logging
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def health_check(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    logger.debug(f"[PdfConverter] healthcheck request from {client_host}:{client_port}")
    return Response(status_code=200)

@app.head("/")
async def health_check_head(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    logger.debug(f"[PdfConverter] healthcheck request from {client_host}:{client_port}")
    return Response(status_code=200)

@app.post("/convert")
async def convert_data(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    
    try:
        # Check for request body
        body = await request.body()
        if not body:
            logger.warning(f"[PdfConverter] no request body from {client_host}:{client_port}")
            return Response(
                status_code=400,
                content='{"message": "No request body found."}',
                media_type="application/json"
            )

        # Create a temporary file and write request body
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(body)
            logger.debug(f"[PdfConverter] conversion request from {client_host}:{client_port}: {len(body)} bytes using file: {temp_file_path}")

        try:
            # Construct output file path
            output_file_path = f"{temp_file_path}.pdf"
            
            # Execute LibreOffice conversion command
            result = subprocess.run(
                ['soffice', '--headless', 
                 '--convert-to', 'pdf:writer_pdf_Export:ExportFonts=1',
                 temp_file_path,
                 '--outdir', '/tmp/'],
                check=True,
                capture_output=True,
                text=True
            )

            # Check if output file exists
            if not os.path.exists(output_file_path):
                logger.warning(f"[PdfConverter] output file {output_file_path} not found for conversion request from {client_host}:{client_port}")
                return Response(
                    status_code=500,
                    content='{"message": "The input data could not be converted to PDF."}',
                    media_type="application/json"
                )

            # Read and return the PDF file
            logger.debug(f"[PdfConverter] retrieving output file {output_file_path} for conversion request from {client_host}:{client_port}")
            with open(output_file_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()

            return Response(
                content=pdf_content,
                media_type="application/octet-stream"
            )

        finally:
            # Clean up: Delete temporary files
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

    except Exception as e:
        logger.error(f"[PdfConverter] exception encountered from {client_host}:{client_port}: {str(e)}")
        return Response(
            status_code=500,
            content=f'{{"message": "An internal server error was encountered", "context": "{str(e)}"}}',
            media_type="application/json"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)