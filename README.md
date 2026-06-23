<h1 align="center">
  Certificate Generator & Email Sender 🎓
</h1>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
</p>

<p align="center">
  An open-source, dual-interface (Web UI & CLI) tool for generating beautifully customized certificates in bulk from Excel or CSV files, and emailing them automatically to participants. 
</p>

---

## ✨ Features

- **Stunning Web Interface**: A modern, glassmorphic dashboard built with FastAPI to visualize, configure, and manage certificate generation and distribution natively in your browser.
- **Live Previews**: Adjust typography, font color, size, and Y-position in real-time before generating hundreds of certificates.
- **Bulk Generation**: Read participant data from `.csv` or `.xlsx` files effortlessly, processing everything asynchronously in the background.
- **Automated Emailing**: Supports multiple SMTP sender accounts to bypass rate limits and distribute the load.
- **Cross-Platform Compatibility**: Bundled with standard open-source fonts (Roboto) for consistent rendering on macOS, Windows, and Linux.
- **Security First**: Uses `.env` files to prevent your email passwords from ever leaking to GitHub.

---

## 📦 Prerequisites

- **Python 3.8+** (use `python3` command if `python` is not found on your system)
- A Gmail Account with an "App Password" generated (if using Gmail).

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/certificate_project.git
   cd certificate_project
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment variables:**
   Copy `.env.example` to `.env` and configure your SMTP credentials and email templates.
   ```bash
   cp .env.example .env
   ```

---

## 🌐 Usage: Web Dashboard (Recommended)

The interactive Web UI provides the most seamless experience for creating and distributing certificates. 

1. **Start the FastAPI Server:**
   ```bash
   uvicorn app:app --port 8000
   ```
2. **Access the Dashboard:**
   Open your browser and navigate to [http://localhost:8000](http://localhost:8000).
3. **Configure & Preview:**
   - Upload your custom template, fonts, and participant data.
   - Adjust the **Y Position**, **Font Size**, and **Font Color**.
   - Click **Update Preview** to verify the name placement.
4. **Distribute:**
   - Turn on **Demo Mode** to test the generation process without sending emails.
   - Click **Generate & Email All** to dispatch your certificates in the background!

---

## 💻 Usage: Command Line Interface

For power users or automated CI/CD environments, the original CLI script remains fully supported.

### 1. Test Name Placement
Test the name placement before processing your list:
```bash
python3 send_certificates.py --test-name "John Doe" --y-pos 400 --font-size 80
```
This generates a single `John Doe_certificate.pdf` inside the `certificates/` directory.

### 2. Bulk Generation (Demo Mode)
Want to see all generated certificates without sending emails yet?
```bash
python3 send_certificates.py --demo
```

### 3. Send Certificates
Once you are completely ready to send the emails:
```bash
python3 send_certificates.py
```
*(You can optionally limit the number of emails sent using the `--limit 10` flag).*

---

## 🎨 Customization

- **Template**: The Web UI allows custom template uploads. Alternatively, replace `template/sample_template.png`.
- **Fonts**: Upload your `.ttf` font directly via the dashboard or place it in the `fonts/` directory.
- **Data File**: CSV or Excel lists can be uploaded dynamically, or you can update `data/sample_participants.csv`.

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!
Feel free to check out the [issues page](../../issues). Please read the [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## 📝 License

This project is [MIT](LICENSE) licensed.
