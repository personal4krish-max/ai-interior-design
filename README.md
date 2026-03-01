# 🏠 DecorAI – AI Interior Design Studio

A beautiful Streamlit web app that transforms rooms using AI — just like the popular "AI Home Design: Interior DecAI" mobile app. Upload a photo, pick a style, and watch AI redesign your space instantly.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🛋️ AI Interior Design | Upload room photo → choose style → generate AI redesign |
| 🏠 Exterior Design | Transform your home's facade with different architectural styles |
| 🌿 Landscape & Garden | Design backyards, patios, front yards with AI |
| 🎨 Wall Color Preview | See how any wall color looks before painting |
| 🪵 Flooring Visualizer | Preview hardwood, marble, tiles, vinyl and more |
| 🧹 Cleanup & Erase | Remove clutter and unwanted objects from photos |
| 💎 Pricing & UPI Payment | Beautiful plans page with UPI QR code payment |

---

## 🚀 COMPLETE SETUP & DEPLOYMENT GUIDE (from scratch)

### STEP 1 — Install Required Software

Make sure you have these installed on your computer:

1. **Python 3.9 or higher** → [Download here](https://python.org/downloads)
   - During install, ✅ check "Add Python to PATH"

2. **Git** → [Download here](https://git-scm.com/downloads)

3. **VS Code (optional but recommended)** → [Download here](https://code.visualstudio.com)

---

### STEP 2 — Set Up the Project

1. **Unzip** the downloaded `ai_interior_design.zip` file anywhere on your computer

2. **Open a terminal / command prompt** in the `ai_interior_design` folder:
   - On Windows: Right-click the folder → "Open in Terminal"
   - On Mac: Right-click → "New Terminal at Folder"

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test locally first:**
   ```bash
   streamlit run app.py
   ```
   Your browser will open at `http://localhost:8501` — you should see the full app! ✅

---

### STEP 3 — Get Your FREE Hugging Face API Token (for AI to work)

The AI image generation uses Hugging Face's free API.

1. Go to [huggingface.co](https://huggingface.co) → Sign up (free)
2. Click your profile icon → **Settings** → **Access Tokens**
3. Click **New Token** → Give it a name → Select **Read** permission → **Generate**
4. Copy the token (starts with `hf_...`)
5. In the app sidebar → ⚙️ AI Settings → paste your token

> 💡 The free tier gives you hundreds of image generations per day!

---

### STEP 4 — Add Your UPI ID

Open `app.py` in VS Code or any text editor.

Find this line near the top (around line 90):

```python
UPI_ID = "yourname@upi"          # ← REPLACE WITH YOUR UPI ID
```

Replace `yourname@upi` with your actual UPI ID, for example:

```python
UPI_ID = "john@paytm"
```

Save the file.

---

### STEP 5 — Publish to Streamlit Community Cloud (share.streamlit.io)

This is completely FREE forever! Follow these exact steps:

#### 5a. Create a GitHub Account
Go to [github.com](https://github.com) → Sign Up (free) if you don't have one.

#### 5b. Create a New GitHub Repository

1. Click the **+** icon (top right) → **New repository**
2. Repository name: `decorai-interior-design` (or anything you like)
3. Set to **Public**
4. Click **Create repository**

#### 5c. Upload Your Files to GitHub

In your terminal (inside the project folder):

```bash
git init
git add .
git commit -m "Initial commit - DecorAI app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/decorai-interior-design.git
git push -u origin main
```

> Replace `YOUR_USERNAME` with your actual GitHub username.

Alternatively, on the GitHub website:
- Click **"uploading an existing file"**
- Drag and drop ALL files from the unzipped folder
- Click **Commit changes**

#### 5d. Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **Sign in with GitHub**
3. Click **New app** (top right)
4. Select your repository: `decorai-interior-design`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **Deploy!**

⏳ Wait 2-5 minutes for the first deployment. Your app will be live at:
```
https://YOUR_USERNAME-decorai-interior-design-app-XXXXX.streamlit.app
```

🎉 **Done! Your app is live on the internet!**

---

### STEP 6 — Share Your App

Copy your Streamlit URL and share it on:
- WhatsApp / Telegram
- Instagram bio
- LinkedIn
- Anywhere!

---

## 📁 Project Structure

```
ai_interior_design/
│
├── app.py                    ← Main application (all pages)
├── requirements.txt          ← Python dependencies
├── README.md                 ← This guide
│
└── .streamlit/
    └── config.toml           ← Dark theme configuration
```

---

## 🔧 Customization Guide

### Change App Name
In `app.py`, find:
```python
APP_NAME = "DecorAI"
```
Change `"DecorAI"` to your preferred name.

### Add More Design Styles
In `app.py`, find the `STYLES` list and add more:
```python
STYLES = [
    "Modern", "Minimalist", ...
    "Your New Style"   # ← Add here
]
```

### Change Primary Color (from gold to another color)
In `.streamlit/config.toml`:
```toml
primaryColor = "#c9a84c"   # ← Change this hex color
```

---

## 💰 Payment Flow

When a user pays via UPI:
1. They scan the QR code or copy your UPI ID
2. They pay through any UPI app (GPay, PhonePe, Paytm, BHIM)
3. They email you the transaction screenshot at your support email
4. You manually activate their plan

> For automated payments, you can later integrate Razorpay or PayU which support UPI.

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| App not opening | Make sure you ran `streamlit run app.py` in the project folder |
| AI not generating | Add your HF token in ⚙️ AI Settings in the sidebar |
| Deployment fails | Check all files are uploaded to GitHub including `.streamlit/config.toml` |
| QR code not scanning | Try increasing screen brightness |

---

## 📞 Tech Stack

- **Frontend**: Streamlit + Custom CSS (Playfair Display font, Gold theme)
- **AI Engine**: Hugging Face Inference API (Stable Diffusion)
- **QR Code**: `qrcode` Python library
- **Images**: Pillow (PIL)
- **Hosting**: Streamlit Community Cloud (free)

---

*Built with ❤️ using Python & Streamlit*
