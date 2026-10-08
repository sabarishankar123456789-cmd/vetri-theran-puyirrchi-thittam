# EduGenie — Google Gemini Powered Learning Assistant

A VS Code-ready learning assistant built with Flask, HTML/CSS/JavaScript and Google's official `google-genai` Python SDK.

## Features
- AI Tutor chat
- Explain any topic
- Generate study notes
- Generate a 10-question quiz
- Generate a 7-day study plan
- Responsive dashboard UI
- Gemini model configurable through `.env`

## Requirements
- Python 3.10+
- A Gemini API key
- VS Code (recommended)

## Run in VS Code — Windows

Open this project folder in VS Code and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your API key:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-3.8-flash
```

Then:

```powershell
python app.py
```

Open:
http://127.0.0.1:5000

## Important
Never upload your real `.env` file or API key to GitHub.

The app uses Google's current stable `gemini-3.8-flash` model by default. If your API account does not expose that model, change `GEMINI_MODEL` to another model available to your account.

## Project structure

EduGenie_Gemini/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
