---
title: MailAI Smart Email Composer
emoji: 🚀
colorFrom: teal
colorTo: blue
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
license: mit
---

# 🚀 MailAI — Smart Email Composer

> An AI-powered email composer built with **Streamlit** that drafts, personalizes, and sends emails using **200+ AI models** via OpenRouter — all from a beautiful, animated web UI.

---

## ✨ Features

- **AI Body Generation** — Enter a subject, pick a tone, and let any OpenRouter model write the full email body instantly
- **200+ AI Models** — Live model list fetched from OpenRouter (GPT-4o, Claude, Gemini, Llama, Mistral, and more)
- **5 Tone Styles** — Formal, Professional, Friendly, Casual, Persuasive
- **SMTP Email Sending** — Works with Gmail, Outlook, or any custom SMTP server
- **File Attachments** — Attach multiple files (PDF, DOCX, PNG, etc.)
- **CC Support** — Optional CC field
- **Two-Page Flow** — Dedicated config page + clean compose page, no clutter
- **Animated UI** — Ambient orbs, shimmer effects, breathing glow, card hover animations
- **Responsive Layout** — Clean full-width design, no sidebar

---

## 📸 UI Overview

### Page 1 — Configuration
Set up your AI engine and email credentials once. The app validates both before letting you proceed.

```
         🚀  MailAI
  Set up once — compose smarter forever

 ┌──────────────────────────────────────┐
 │  ① AI Engine                        │
 │  OpenRouter API Key  [⚡ Load Models]│
 │  Select Model ▼                      │
 └──────────────────────────────────────┘

 ┌──────────────────────────────────────┐
 │  ② Email Account                    │
 │  SMTP Host · Port                    │
 │  Your Email · App Password           │
 └──────────────────────────────────────┘

  ✅ AI Engine       Ready
  ✅ Email Account   Ready

      [ 🚀 Start Composing → ]
```

### Page 2 — Compose
Full-width email composer with AI generation and file attachment support.

```
 🚀 MailAI   Smart Composer          [⚙️ Settings]
 ● llama-3.3-70b-instruct

 ┌──────────── 👤 Recipients ─────────────────┐
 │  To *  [recipient@example.com]             │
 │  CC    [cc@example.com (optional)]         │
 └────────────────────────────────────────────┘

 ┌──────────── 📝 Subject & Tone ─────────────┐
 │  Subject * [What's this email about?]      │
 │  Tone      [Professional ▼]                │
 │  [✨ Generate Body]  ✨ Ready — 3 words   │
 └────────────────────────────────────────────┘

 ┌──────────── 📄 Email Body ──────────────────┐
 │  (AI-generated or manual text)             │
 │                               450/5000 ━━━ │
 └────────────────────────────────────────────┘

 ┌──────────── 📎 Attachments ────────────────┐
 │  Drop files here or click to browse        │
 └────────────────────────────────────────────┘

       [ 🚀 Send Email ]
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io) |
| **AI Generation** | [OpenRouter API](https://openrouter.ai) (OpenAI-compatible) |
| **Email Sending** | Python `smtplib` + `email` (stdlib) |
| **HTTP Client** | `requests` |
| **Config** | `python-dotenv` |
| **Font** | Plus Jakarta Sans (Google Fonts) |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mailai-composer.git
cd mailai-composer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
OPENROUTER_API_KEY=sk-or-v1-...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASS=xxxx xxxx xxxx xxxx
```

> **Note:** The `.env` file is optional. You can fill all credentials directly in the app's Configuration page.

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🔑 Getting Your API Keys

### OpenRouter API Key
1. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up for a free account
3. Click **Create Key**
4. Copy the key (starts with `sk-or-v1-`)

### Gmail App Password
Gmail requires an **App Password** — not your regular Gmail password.

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Navigate to **Security → 2-Step Verification** (must be enabled)
3. Scroll down to **App passwords**
4. Select **Mail** and your device → click **Generate**
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

> For **Outlook/Hotmail**, use `smtp-mail.outlook.com` on port `587` with your regular password or an app password.

---

## 🌐 Supported SMTP Providers

| Provider | SMTP Host | Port |
|---|---|---|
| Gmail | `smtp.gmail.com` | `587` |
| Outlook / Hotmail | `smtp-mail.outlook.com` | `587` |
| Yahoo Mail | `smtp.mail.yahoo.com` | `587` |
| iCloud Mail | `smtp.mail.me.com` | `587` |
| Custom / Self-hosted | your SMTP host | varies |

---

## 🤖 Popular AI Models on OpenRouter

| Model | Provider | Best For |
|---|---|---|
| `meta-llama/llama-3.3-70b-instruct` | Meta | General emails, free tier |
| `openai/gpt-4o` | OpenAI | High-quality, nuanced tone |
| `openai/gpt-4o-mini` | OpenAI | Fast + affordable |
| `anthropic/claude-3.5-sonnet` | Anthropic | Long, detailed emails |
| `google/gemini-pro-1.5` | Google | Structured, factual emails |
| `mistralai/mistral-7b-instruct` | Mistral | Lightweight, fast |

> The app fetches the **full live list** from OpenRouter when you click **Load Models** — so you always see every model available on your account.

---

## 📁 Project Structure

```
mailai-composer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your credentials (git-ignored)
└── README.md           # This file
```

---

## 🔧 Environment Variables Reference

| Variable | Required | Description | Example |
|---|---|---|---|
| `OPENROUTER_API_KEY` | Optional* | OpenRouter API key for AI generation | `sk-or-v1-abc123` |
| `SMTP_HOST` | Optional* | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | Optional* | SMTP server port | `587` |
| `SMTP_USER` | Optional* | Your sender email address | `you@gmail.com` |
| `SMTP_PASS` | Optional* | Your SMTP app password | `xxxx xxxx xxxx xxxx` |

> *Optional because all values can also be entered directly in the app's Configuration page. The `.env` file just pre-fills those fields automatically.

---

## 🚀 How It Works

```
User fills subject + selects tone
           ↓
   Clicks ✨ Generate Body
           ↓
   App calls OpenRouter API
   with selected model + prompt
           ↓
   AI returns email body text
           ↓
   User reviews + edits body
           ↓
   Clicks 🚀 Send Email
           ↓
   App connects to SMTP server
   via TLS → sends email
           ↓
        ✅ Done!
```

---

## 🛡️ Security Notes

- **Never commit your `.env` file** — it's listed in `.gitignore`
- Always use an **App Password** for Gmail, never your main account password
- The app sends emails over **STARTTLS** (encrypted) connections only
- API keys are stored only in session state and are never logged

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `SMTPAuthenticationError` | Wrong email/password | Re-check app password; enable 2FA on Gmail first |
| `Model returned empty response` | Model returned `null` content | Switch to a different model (e.g. `gpt-4o-mini`) |
| `API error 401` | Invalid OpenRouter key | Double-check your key at openrouter.ai/keys |
| `Connection refused` | Wrong SMTP host/port | Verify host and port for your email provider |
| `Models not loading` | Network issue or key issue | Check your internet connection and API key |

---

## 📦 Requirements

```
streamlit>=1.35.0
requests>=2.31.0
python-dotenv>=1.0.0
openai>=1.30.0
```

Python **3.10+** recommended.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io) — for the rapid web app framework
- [OpenRouter](https://openrouter.ai) — for unified access to 200+ AI models
- [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) — for the beautiful typography
- [Python smtplib](https://docs.python.org/3/library/smtplib.html) — for reliable email delivery

---

<div align="center">
  Built with ❤️ using Streamlit + OpenRouter
</div>
