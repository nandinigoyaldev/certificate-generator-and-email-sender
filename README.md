<h1 align="center">
  Certificate Generator & Email Sender 🎓
</h1>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
</p>

<p align="center">
  An open-source Python tool for generating beautifully customized certificates in bulk from Excel or CSV files, and emailing them automatically to participants.
</p>

## ✨ Features

- **Bulk Certificate Generation**: Read participant data from `.csv` or `.xlsx` files effortlessly.
- **Customizable Placement**: Easily test and configure name placement using `--test-name`, `--y-pos` and `--font-size` parameters directly from your terminal.
- **Automated Emailing**: Supports multiple SMTP sender accounts to bypass rate limits and distribute the load.
- **Cross-Platform Compatibility**: Bundled with standard open-source fonts (Roboto) for consistent rendering on macOS, Windows, and Linux.
- **Security First**: Uses `.env` files to prevent your email passwords from ever leaking to GitHub.

## 📦 Prerequisites

- **Python 3.8+** (use `python3` command if `python` is not found on your system)
- A Gmail Account with an "App Password" generated (if using Gmail).

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/certificate_project.git
   cd certificate_project
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   Copy `.env.example` to `.env` and fill in your email credentials.
   ```bash
   cp .env.example .env
   ```

## 🛠️ Usage

### 1. Test Name Placement (Demo Mode)

To ensure the name is placed perfectly on your certificate template *before* generating hundreds of them, use the `--test-name` argument:

```bash
python3 send_certificates.py --test-name "John Doe" --y-pos 400 --font-size 80
```
This generates a single `John Doe_certificate.pdf` inside the `certificates/` directory. Check it, and adjust `--y-pos` and `--font-size` until it looks just right!

### 2. Bulk Generation (No Emails Sent)

Want to see all generated certificates without sending emails yet?
```bash
python3 send_certificates.py --demo
```

### 3. Send Certificates

Once you are completely ready to send the emails:
```bash
python3 send_certificates.py
```

You can optionally limit the number of emails sent (great for testing a small batch):
```bash
python3 send_certificates.py --limit 10
```

## 🎨 Customizing

- **Template**: Replace `template/sample_template.png` with your own beautiful design.
- **Fonts**: Place your `.ttf` font in the `fonts/` directory and run the script with `--font-file fonts/YourFont.ttf`.
- **Data File**: The default data file expected is `data/sample_participants.csv`, but you can pass any CSV or Excel file using `--data-file path/to/your/file.xlsx`.

## 🤝 Contributing

Contributions, issues and feature requests are welcome!
Feel free to check out the [issues page](../../issues). Please read the [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## 📝 License

This project is [MIT](LICENSE) licensed.
