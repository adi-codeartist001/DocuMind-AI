# 🧠 DocuMind AI — Multi-Tool Document Intelligence Platform

A professional, production-ready AI web app built with Streamlit that transforms any document into actionable insights using GPT-4o and Google Gemini.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 💬 **Document Q&A** | Chat with any document — ask questions, get answers |
| 📝 **Resume Analyzer** | ATS score, skill gaps, actionable improvements |
| ⚖️ **Legal Analyzer** | Risk clauses, obligations, key dates from contracts |
| 🔬 **Research Summarizer** | Break down papers into structured insights |

### 🤖 Supports Both:
- **OpenAI GPT-4o / GPT-4 Turbo**
- **Google Gemini 1.5 Flash**

### 📄 Supported File Formats:
- PDF
- TXT
- DOCX (Word)

---

## 🚀 Quick Start

### 1. Clone / Download
```bash
# If using git
git clone <your-repo>
cd documind
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
The app will automatically open at `http://localhost:8501`

---

## 🔑 API Keys

You'll need at least one API key:

- **OpenAI**: Get yours at [platform.openai.com](https://platform.openai.com)
- **Google Gemini**: Get yours at [aistudio.google.com](https://aistudio.google.com)

Enter your key in the sidebar when the app launches. No `.env` file needed — keys are entered directly in the UI.

---

## 📁 Project Structure

```
documind/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🧑‍💻 Tech Stack

- **Frontend**: Streamlit + Custom CSS (Dark theme, Syne + DM Sans fonts)
- **AI**: OpenAI API + Google Generative AI
- **Document Parsing**: PyPDF2, python-docx
- **Language**: Python 3.9+

---

## 💡 How It Works

1. User uploads a document (PDF/TXT/DOCX)
2. Text is extracted using PyPDF2 or python-docx
3. A structured prompt is built based on the selected tool
4. The prompt is sent to the chosen AI model (OpenAI or Gemini)
5. The response is displayed in a formatted result box
6. User can download the analysis as a .txt file

---

## 🌟 What Makes This Professional

- Clean dark-mode UI with custom CSS
- Multi-model AI support (switch between GPT-4o and Gemini)
- Document statistics (word count, pages, characters)
- Structured, consistent AI output formats
- Download analysis functionality
- Interactive chat history for Q&A tool
- Professional disclaimers for legal tool

---

## 📈 Potential Extensions

- [ ] Add ChromaDB/FAISS for true RAG (vector search)
- [ ] Add support for Excel, CSV, HTML files
- [ ] Add user authentication
- [ ] Deploy to Streamlit Cloud (free)
- [ ] Add email export functionality
- [ ] Multi-document comparison feature

---

## 🚀 Deploy to Streamlit Cloud (Free!)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Deploy in 2 minutes — free forever

---

Built with ❤️ using Streamlit + OpenAI + Google Gemini
