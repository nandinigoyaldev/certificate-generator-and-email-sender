import os
import smtplib
import logging
import argparse
from email.message import EmailMessage
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# === LOGGING SETUP ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# === CONFIG ===
SMTP_PORT = 465

import tempfile
TEMPLATE_FILE = "template/sample_template.png"
OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "certificates")

def get_participants(file_path: str):
    """Load participants from a CSV or Excel file."""
    import pandas as pd
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine="openpyxl")
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error loading participants file {file_path}: {e}")
        return []

# === FUNCTIONS ===
def generate_certificate(name: str, template_file: str, font_file: str, font_size: int, y_pos: int, font_color: str = "black", x_pos: int = -1, align: str = "center") -> str:
    """Generates a certificate with the given name and returns the output filename."""
    if not os.path.exists(template_file):
        raise FileNotFoundError(f"Template file not found at {template_file}")
    if not os.path.exists(font_file):
        raise FileNotFoundError(f"Font file not found at {font_file}")

    template = Image.open(template_file).convert("RGB")
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(font_file, font_size)

    text_width = draw.textlength(name, font=font)
    image_width = template.width

    if align == "center":
        x = (image_width - text_width) // 2 if x_pos == -1 else x_pos - (text_width // 2)
    elif align == "right":
        x = image_width - text_width if x_pos == -1 else x_pos - text_width
    else: # left
        x = 0 if x_pos == -1 else x_pos

    position = (x, y_pos)

    draw.text(position, name, font=font, fill=font_color)

    safe_name = str(name).strip().replace("/", "-").replace("\\", "-")
    filename = os.path.join(OUTPUT_DIR, f"{safe_name}_certificate.pdf")
    template.save(filename, "PDF")
    return filename

def send_email(sender: str, password: str, recipient: str, subject: str, body: str, attachment: str, smtp_server: str = "smtp.gmail.com") -> None:
    """Sends an email with the certificate attached."""
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(attachment),
        )

    with smtplib.SMTP_SSL(smtp_server, SMTP_PORT) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
        logger.info(f"✅ Email sent to {recipient}")

# === MAIN ===
def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and email certificates")
    parser.add_argument("--demo", action="store_true", help="Generate certificates only (no email)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of recipients")
    parser.add_argument("--test-name", type=str, default=None, help="Generate a single test certificate for a specific name to check placement")
    parser.add_argument("--y-pos", type=int, default=400, help="Y-coordinate for the name text (default: 400)")
    parser.add_argument("--font-size", type=int, default=80, help="Font size for the name (default: 80)")
    parser.add_argument("--font-file", type=str, default="fonts/Roboto-Regular.ttf", help="Path to the TrueType font file")
    parser.add_argument("--data-file", type=str, default="data/sample_participants.csv", help="Path to the participants data file (.csv or .xlsx)")
    
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Test Name Mode
    if args.test_name:
        logger.info(f"Generating test certificate for: '{args.test_name}'")
        try:
            cert_path = generate_certificate(args.test_name, TEMPLATE_FILE, args.font_file, args.font_size, args.y_pos)
            logger.info(f"✅ Test certificate successfully generated at: {cert_path}")
        except Exception as e:
            logger.error(f"Failed to generate test certificate: {e}")
        return

    # 2. Bulk Processing Mode
    recipients = get_participants(args.data_file)
    
    if args.limit is not None:
        recipients = recipients[: int(args.limit)]

    if not recipients:
        logger.error(f"No valid recipients found in {args.data_file}")
        return

    if not args.demo and not ACCOUNTS:
        logger.error("No email accounts configured in environment variables. Set EMAIL_ACCOUNTS and EMAIL_PASSWORDS, or run with --demo.")
        return

    # Split into two batches if multiple accounts are used (based on original logic)
    num_accounts = len(ACCOUNTS) if ACCOUNTS else 1
    batch_size = max(1, len(recipients) // num_accounts) if len(recipients) > 1 and num_accounts > 1 else len(recipients)
    
    batches = [recipients[i:i + batch_size] for i in range(0, len(recipients), batch_size)]

    for i, batch in enumerate(batches):
        if not args.demo:
            account = ACCOUNTS[i % len(ACCOUNTS)]
            sender_email = account["email"]
            sender_pass = account["password"]
            logger.info(f"Using {sender_email} for batch {i+1}...")

        for r in batch:
            try:
                name = str(r.get("Name", "")).strip()
                email = str(r.get("Email", "")).strip()

                if not name:
                    continue

                safe_name = name.replace("/", "-").replace("\\", "-")
                cert_path = os.path.join(OUTPUT_DIR, f"{safe_name}_certificate.pdf")
                
                if os.path.exists(cert_path):
                    logger.info(f"⏭️ Skipping {name} ({email}) – certificate already exists")
                    continue

                cert = generate_certificate(name, TEMPLATE_FILE, args.font_file, args.font_size, args.y_pos)

                if not args.demo:
                    send_email(sender_email, sender_pass, email, SUBJECT, BODY, cert)
                    logger.info(f"Sent to {name} ({email})")
                else:
                    logger.info(f"Generated demo cert for {name} ({email})")

            except Exception as e:
                logger.error(f"Failed for {r.get('Name')} ({r.get('Email')}): {e}")

if __name__ == "__main__":
    main()
