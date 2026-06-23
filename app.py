import os
import shutil
import zipfile
import json
from pathlib import Path
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import tempfile
from send_certificates import generate_certificate, get_participants, send_email, SUBJECT, BODY, ACCOUNTS

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Ensure required directories exist in temp
UPLOAD_DIR = Path(tempfile.gettempdir()) / "uploads"
OUTPUT_DIR = Path(tempfile.gettempdir()) / "certificates"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="index.html")
    except Exception as e:
        import traceback
        return f"<html><body><h1>Internal Server Error</h1><pre>{traceback.format_exc()}</pre></body></html>"

@app.post("/api/preview")
async def preview_certificate(
    request: Request,
    name: str = Form("John Doe"),
    x_pos: int = Form(-1),
    y_pos: int = Form(400),
    align: str = Form("center"),
    font_size: int = Form(80),
    font_color: str = Form("black"),
    template_file: UploadFile = File(None),
    font_file: UploadFile = File(None)
):
    """Generates a preview certificate and returns it."""
    try:
        # Default files if none provided
        temp_template_path = os.path.join(BASE_DIR, "template/sample_template.png")
        temp_font_path = os.path.join(BASE_DIR, "fonts/Roboto-Regular.ttf")

        if template_file and template_file.filename:
            temp_template_path = UPLOAD_DIR / template_file.filename
            with open(temp_template_path, "wb") as buffer:
                shutil.copyfileobj(template_file.file, buffer)
        
        if font_file and font_file.filename:
            temp_font_path = UPLOAD_DIR / font_file.filename
            with open(temp_font_path, "wb") as buffer:
                shutil.copyfileobj(font_file.file, buffer)

        if not os.path.exists(temp_template_path) or not os.path.exists(temp_font_path):
            return JSONResponse(status_code=400, content={"error": "Template or font file not found."})

        cert_path = generate_certificate(
            name=name,
            template_file=str(temp_template_path),
            font_file=str(temp_font_path),
            font_size=font_size,
            y_pos=y_pos,
            font_color=font_color,
            x_pos=x_pos,
            align=align
        )
        return FileResponse(cert_path, media_type="application/pdf", filename="preview.pdf")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/parse_csv")
async def parse_csv(request: Request, data_file: UploadFile = File(...)):
    try:
        temp_data_path = UPLOAD_DIR / data_file.filename
        with open(temp_data_path, "wb") as buffer:
            shutil.copyfileobj(data_file.file, buffer)
        recipients = get_participants(str(temp_data_path))
        return JSONResponse(content={"participants": recipients})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.post("/api/generate")
async def generate_bulk(
    request: Request,
    x_pos: int = Form(-1),
    y_pos: int = Form(400),
    align: str = Form("center"),
    font_size: int = Form(80),
    font_color: str = Form("black"),
    demo_mode: bool = Form(False),
    subject: str = Form(SUBJECT),
    body: str = Form(BODY),
    template_file: UploadFile = File(None),
    font_file: UploadFile = File(None),
    data_file: UploadFile = File(None)
):
    try:
        temp_template_path = os.path.join(BASE_DIR, "template/sample_template.png")
        temp_font_path = os.path.join(BASE_DIR, "fonts/Roboto-Regular.ttf")
        temp_data_path = os.path.join(BASE_DIR, "data/sample_participants.csv")

        if template_file and template_file.filename:
            temp_template_path = UPLOAD_DIR / template_file.filename
            with open(temp_template_path, "wb") as buffer:
                shutil.copyfileobj(template_file.file, buffer)
        
        if font_file and font_file.filename:
            temp_font_path = UPLOAD_DIR / font_file.filename
            with open(temp_font_path, "wb") as buffer:
                shutil.copyfileobj(font_file.file, buffer)

        if data_file and data_file.filename:
            temp_data_path = UPLOAD_DIR / data_file.filename
            with open(temp_data_path, "wb") as buffer:
                shutil.copyfileobj(data_file.file, buffer)

        recipients = get_participants(str(temp_data_path))
        if not recipients:
            return JSONResponse(status_code=400, content={"error": "No participants found in data file."})

        # Run synchronously for Vercel
        zip_path = process_bulk_certificates(
            recipients=recipients,
            template_path=str(temp_template_path),
            font_path=str(temp_font_path),
            y_pos=y_pos,
            x_pos=x_pos,
            align=align,
            font_size=font_size,
            font_color=font_color,
            demo_mode=demo_mode,
            subject=subject,
            body=body
        )
        if demo_mode:
            return FileResponse(zip_path, media_type="application/zip", filename="certificates.zip")
        return {"message": "Bulk generation and emailing completed.", "total": len(recipients)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def process_bulk_certificates(recipients, template_path, font_path, y_pos, x_pos, align, font_size, font_color, demo_mode, subject, body):
    import logging
    logger = logging.getLogger(__name__)
    
    num_accounts = len(ACCOUNTS) if ACCOUNTS else 1
    batch_size = max(1, len(recipients) // num_accounts) if len(recipients) > 1 and num_accounts > 1 else len(recipients)
    batches = [recipients[i:i + batch_size] for i in range(0, len(recipients), batch_size)]
    generated_files = []

    for i, batch in enumerate(batches):
        sender_email, sender_pass = None, None
        if not demo_mode and ACCOUNTS:
            account = ACCOUNTS[i % len(ACCOUNTS)]
            sender_email = account["email"]
            sender_pass = account["password"]

        for r in batch:
            try:
                name = str(r.get("Name", "")).strip()
                email = str(r.get("Email", "")).strip()
                if not name:
                    continue
                
                safe_name = name.replace("/", "-").replace("\\", "-")
                cert_path = os.path.join(str(OUTPUT_DIR), f"{safe_name}_certificate.pdf")
                
                if not os.path.exists(cert_path):
                    cert_path = generate_certificate(name, template_path, font_path, font_size, y_pos, font_color, x_pos, align)
                
                generated_files.append(cert_path)
                
                if not demo_mode and sender_email and sender_pass and email:
                    send_email(sender_email, sender_pass, email, subject, body, cert_path)
            except Exception as e:
                logger.error(f"Failed processing {r.get('Name')}: {e}")
                
    # Create ZIP archive
    zip_filename = os.path.join(str(OUTPUT_DIR), "certificates.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for f in generated_files:
            if os.path.exists(f):
                zipf.write(f, os.path.basename(f))
                
    return zip_filename
