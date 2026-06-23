<div align="center">
  <img src="https://img.shields.io/badge/CredFlow-SaaS-3b82f6?style=for-the-badge" alt="CredFlow Logo">
  <h1>🏆 CredFlow</h1>
  <p><strong>A lightning-fast, hackathon-ready tool to generate personalized certificates in bulk and dispatch them automatically via email.</strong></p>

  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#deployment">Deployment</a> •
    <a href="#configuration">Configuration</a>
  </p>
</div>

---

Welcome to **CredFlow**! Whether you're organizing a 500-person hackathon, a local workshop, or an online webinar, this tool completely automates the tedious process of creating and sending out participant certificates.

It features an ultra-sleek, minimalist web dashboard inspired by modern SaaS products. Built with **FastAPI** and natively compatible with **Vercel Serverless**, you can host it in seconds and process hundreds of participants instantly.

## ✨ Key Features

- **"Credify Dark" Aesthetic:** A highly professional, distraction-free interface utilizing deep slates, neon blue accents, and sharp typography.
- **Dynamic Data Parsing:** Upload your CSV/XLSX and instantly view a clean data table of all participants directly in your browser.
- **Vercel Serverless Ready:** The backend is fully ephemeral and writes strictly to `/tmp`, allowing you to host the entire platform on Vercel's free tier.
- **Drag & Drop:** Upload custom templates and lists with seamless native drag-and-drop zones.
- **Zero-Setup Typographical Engine:** The app uses smart alignment and auto-centers the text on the certificate so you don't have to guess X/Y coordinates anymore.
- **Demo Mode (ZIP Downloads):** Don't want to spam emails just yet? Toggle "Demo Mode" and the system will instantly process your certificates and securely download a `.zip` file containing all PDFs!
- **Load Balanced Mailing:** The backend supports round-robin dispatch across multiple SMTP accounts to prevent rate-limiting during massive events.

---

## 🚀 Quick Start (Local)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/credflow.git
   cd credflow
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI Development Server:**
   ```bash
   uvicorn app:app --port 8000 --reload
   ```

5. **Access the Dashboard:**
   Open your browser and navigate to [http://localhost:8000](http://localhost:8000).

---

## ☁️ Deployment (Vercel)

CredFlow is pre-configured for instant serverless deployment on Vercel!

1. Push your code to a GitHub repository.
2. Sign in to [Vercel](https://vercel.com) and click **Add New Project**.
3. Import your GitHub repository.
4. Click **Deploy**! 

*Note: Vercel automatically detects the `vercel.json` file which instructs it to properly bundle the HTML templates, CSS, JS, and font files for the serverless function.*

---

## 📄 File Formatting

When uploading your participant list via the Dashboard, ensure it is an Excel (`.xlsx`) or `.csv` file containing exactly two columns:

| Name | Email |
| :--- | :--- |
| Jane Doe | jane.doe@example.com |
| John Smith | john.smith@example.com |

---

## 🛠 Built With

- **Backend:** Python, FastAPI, Starlette
- **Frontend:** Vanilla HTML5, CSS3, Javascript (No heavy frameworks!)
- **Certificate Engine:** Pillow (PIL)
- **Deployment:** Vercel Serverless

---

<div align="center">
  <p>Built for hackers, organizers, and communities.</p>
</div>
