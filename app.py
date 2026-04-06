import streamlit as st
import tempfile

# setting up the page
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# all the css styling 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:         #0a0a0f;
    --surface:    #111118;
    --surface2:   #1a1a24;
    --border:     #2a2a3a;
    --accent:     #7c6df8;
    --accent2:    #f06292;
    --accent3:    #26c6da;
    --text:       #e8e8f0;
    --muted:      #888899;
    --radius:     14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* CORRECTED SECTION: We hide the menu and footer, but keep the header/toolbar 
   functional so the sidebar button actually works */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { 
    background: rgba(0,0,0,0) !important; 
    visibility: visible !important;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 20px;
}
.card-accent { border-left: 3px solid var(--accent); }
.card-green  { border-left: 3px solid #66bb6a; }
.card-pink   { border-left: 3px solid var(--accent2); }
.card-teal   { border-left: 3px solid var(--accent3); }

.hero {
    background: linear-gradient(135deg, #0f0e1f 0%, #141228 50%, #0a1520 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 40px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, var(--accent) 60%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-sub {
    color: var(--muted);
    font-size: 15px;
    margin: 0;
    font-weight: 300;
}

.result-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    line-height: 1.75;
    font-size: 15px;
    color: var(--text);
    white-space: pre-wrap;
    margin-top: 16px;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5a4de0) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,109,248,0.35) !important;
}

.metric-row { display: flex; gap: 14px; margin-bottom: 20px; flex-wrap: wrap; }
.metric-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    flex: 1;
    min-width: 120px;
}
.metric-val { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--accent); }
.metric-label { font-size: 12px; color: var(--muted); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)


# ---- reading pdf files ----
def read_pdf(file):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text() + "\n"
        return all_text
    except ImportError:
        st.error("PyPDF2 not installed! Run: pip install PyPDF2")
        return ""
    except Exception as e:
        st.error("Error reading pdf: " + str(e))
        return ""


# ---- reading txt files ----
def read_txt(file):
    content = file.read().decode("utf-8", errors="ignore")
    return content


# ---- reading docx files ----
def read_docx(file):
    try:
        import docx
        # save it temporarily first
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        tmp.write(file.read())
        tmp.close()
        doc = docx.Document(tmp.name)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except ImportError:
        st.error("python-docx not installed! Run: pip install python-docx")
        return ""


# ---- main function to get text from any uploaded file ----
def get_text(uploaded_file):
    if uploaded_file is None:
        return ""
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return read_pdf(uploaded_file)
    elif filename.endswith(".txt"):
        return read_txt(uploaded_file)
    elif filename.endswith(".docx"):
        return read_docx(uploaded_file)
    else:
        return ""


# ---- calling openai api ----
def ask_openai(prompt, api_key, model_name):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are DocuMind AI, an expert document analyst. Give detailed and professional analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return answer
    except ImportError:
        return "openai package not installed. Run: pip install openai"
    except Exception as e:
        return "OpenAI Error: " + str(e)


# ---- calling gROQ api ----
def ask_groq(prompt, api_key):
    try:
        import requests
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are DocuMind AI, an expert document analyst. Give detailed and professional analysis."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2500,
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=body, timeout=60)
        data = response.json()
        if response.status_code != 200:
            return "❌ Groq Error: " + data.get("error", {}).get("message", str(data))
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return "❌ Groq Error: " + str(e)


# ---- this function decides which ai to call based on sidebar selection ----
GROQ_API_KEY = "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"  # 👈 paste your key here

def get_ai_response(prompt):
    return ask_groq(prompt, GROQ_API_KEY)


# ---- session state setup ----
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:

    st.markdown("""
    <div style='padding:16px 0 8px 0;'>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;
                    background:linear-gradient(135deg,#fff,#7c6df8);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;'>
            DocuMind AI
        </div>
        <div style='color:#888899;font-size:12px;margin-top:2px;'>Document Intelligence Platform</div>
    </div>
    <hr style='border:none;border-top:1px solid #2a2a3a;margin:10px 0 18px 0;'>
    """, unsafe_allow_html=True)

    # navigation buttons
    pages = ["Home", "Document Q&A", "Resume Analyzer", "Legal Analyzer", "Research Summarizer"]

    for page_name in pages:
        if st.button(page_name, key="btn_" + page_name, use_container_width=True):
            st.session_state.active_page = page_name
            st.rerun()
# ==============================================================================
# PAGE: HOME
# ==============================================================================
current_page = st.session_state.active_page

if current_page == "Home":

    st.markdown("""
    <div class='hero'>
        <div class='hero-title'>DocuMind AI Platform</div>
        <p class='hero-sub'>Your intelligent assistant for every kind of document — powered by GPT-4o & Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='card card-accent'>
            <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;margin-bottom:10px;'>Document Q&A</div>
            <div style='color:#888899;font-size:14px;line-height:1.6;'>Upload any document and have a full conversation with it. Ask questions, get summaries, extract specific information.</div>
        </div>
        <div class='card card-teal'>
            <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;margin-bottom:10px;'>Legal Analyzer</div>
            <div style='color:#888899;font-size:14px;line-height:1.6;'>Analyze contracts, NDAs, agreements. Identify risky clauses, missing sections, obligations and key dates.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card card-pink'>
            <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;margin-bottom:10px;'>Resume Analyzer</div>
            <div style='color:#888899;font-size:14px;line-height:1.6;'>Get ATS compatibility scores, identify skill gaps, and receive actionable improvements for any job role.</div>
        </div>
        <div class='card card-green'>
            <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;margin-bottom:10px;'> Research Summarizer</div>
            <div style='color:#888899;font-size:14px;line-height:1.6;'>Break down research papers into executive summaries, methodology, findings, and research gaps.</div>
        </div>
        """, unsafe_allow_html=True)



# ==============================================================================
# PAGE: DOCUMENT Q&A
# ==============================================================================
elif current_page == "Document Q&A":

    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;margin-bottom:6px;'>Document Q&A</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888899;margin-bottom:24px;'>Upload any document and ask it anything.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt", "docx"], key="qa_upload")

    if uploaded_file is not None:
        doc_text = get_text(uploaded_file)

        if doc_text:
            total_words = len(doc_text.split())
            total_chars = len(doc_text)
            total_pages = max(1, round(total_chars / 3000))

            st.markdown(f"""
            <div class='metric-row'>
                <div class='metric-tile'><div class='metric-val'>{total_pages}</div><div class='metric-label'>Est. Pages</div></div>
                <div class='metric-tile'><div class='metric-val'>{total_words:,}</div><div class='metric-label'>Words</div></div>
                <div class='metric-tile'><div class='metric-val'>{total_chars:,}</div><div class='metric-label'>Characters</div></div>
                <div class='metric-tile'><div class='metric-val'><span style='color:#66bb6a;'>✓</span></div><div class='metric-label'>Loaded</div></div>
            </div>
            """, unsafe_allow_html=True)

            # show previous chat messages
            for msg in st.session_state.chat_messages:
                if msg["role"] == "You":
                    st.markdown("<div class='result-box'><span style='color:#7c6df8;font-weight:700;'>You:</span><br>" + msg["content"] + "</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='result-box'><span style='color:#26c6da;font-weight:700;'>DocuMind AI:</span><br>" + msg["content"] + "</div>", unsafe_allow_html=True)

            user_question = st.text_input("Ask a question about your document...", placeholder="e.g. What is the main topic? Summarize section 2.", key="qa_input")

            col1, col2 = st.columns([1, 5])
            with col1:
                ask_btn = st.button("Ask AI", key="ask_btn")
            with col2:
                clear_btn = st.button("Clear Chat", key="clear_btn")

            if clear_btn:
                st.session_state.chat_messages = []
                st.rerun()

            if ask_btn and user_question:
                # only send first 12000 chars to avoid hitting token limits
                short_text = doc_text[:12000]

                prompt = "Here is the document content:\n---\n" + short_text + "\n---\n\nQuestion: " + user_question + "\n\nPlease give a clear and detailed answer based only on the document above."

                with st.spinner("Thinking..."):
                    ai_reply = get_ai_response(prompt)

                st.session_state.chat_messages.append({"role": "You", "content": user_question})
                st.session_state.chat_messages.append({"role": "DocuMind AI", "content": ai_reply})
                st.rerun()

    else:
        st.markdown("<div style='color:#888899;text-align:center;padding:40px;'>Upload a PDF, TXT, or DOCX file to start chatting with it.</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE: RESUME ANALYZER
# ==============================================================================
elif current_page == "Resume Analyzer":

    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;margin-bottom:6px;'>Resume Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888899;margin-bottom:24px;'>Get ATS score, skill gap analysis, and actionable improvements.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("Upload Resume (PDF / TXT / DOCX)", type=["pdf", "txt", "docx"], key="resume_upload")

    with col2:
        job_title = st.text_input("Target Job Role", placeholder="e.g. Senior Data Scientist at Google", key="job_title")
        job_description = st.text_area("Paste Job Description (optional)", height=120, placeholder="Paste the full job description here for better analysis...", key="job_desc")

    analyze_btn = st.button("🔍 Analyze Resume", key="resume_btn")

    if analyze_btn:
        if resume_file is None:
            st.warning("Please upload a resume first!")
        else:
            resume_text = get_text(resume_file)

            if resume_text:
                jd_part = ""
                if job_description:
                    jd_part = "\n\nJob Description:\n" + job_description[:3000]

                prompt = "You are an expert ATS analyzer and career coach.\n\nAnalyze this resume for the role: " + (job_title or "General Professional Role") + jd_part + "\n\nResume:\n---\n" + resume_text[:8000] + "\n---\n\nGive a full analysis in this exact format:\n\n##  ATS Compatibility Score: [X/100]\n\n##  Category Scores\n- **Formatting and Structure**: [X/10] — [brief reason]\n- **Keywords and Skills Match**: [X/10] — [brief reason]\n- **Experience Section**: [X/10] — [brief reason]\n- **Education and Certifications**: [X/10] — [brief reason]\n- **Quantified Achievements**: [X/10] — [brief reason]\n\n## Strengths (Top 5)\n[List the top 5 strengths]\n\n##  Critical Issues (Must Fix)\n[List must-fix problems]\n\n##  Missing Keywords and Skills\n[List important missing keywords for this role]\n\n## Top 5 Actionable Improvements\n[List specific improvement steps]\n\n##  Suggested Professional Summary\n[Write an improved 3-4 line professional summary]\n\n## Final Verdict\n[2-3 sentence overall assessment]"

                with st.spinner("Analyzing your resume..."):
                    result = get_ai_response(prompt)

                st.markdown("<div class='result-box'>" + result.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
                st.download_button("⬇️ Download Analysis", data=result, file_name="resume_analysis.txt", mime="text/plain")


# ==============================================================================
# PAGE: LEGAL ANALYZER
# ==============================================================================
elif current_page == "Legal Analyzer":

    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;margin-bottom:6px;'>Legal Document Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888899;margin-bottom:24px;'>Extract key clauses, risks, obligations and important dates from any legal document.</p>", unsafe_allow_html=True)

    st.markdown("<div style='background:#1a0f0f;border:1px solid #3a2020;border-radius:10px;padding:12px 16px;margin-bottom:20px;font-size:13px;color:#f4a261;'>⚠️ <strong>Disclaimer:</strong> This is for informational purposes only and is not legal advice. Always consult a qualified lawyer.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        legal_file = st.file_uploader("Upload Legal Document", type=["pdf", "txt", "docx"], key="legal_upload")

    with col2:
        doc_type = st.selectbox("Document Type", [
            "Auto-detect",
            "Employment Contract",
            "NDA / Confidentiality Agreement",
            "Service Agreement",
            "Lease / Rental Agreement",
            "Partnership Agreement",
            "Terms of Service",
            "Privacy Policy",
            "Settlement Agreement",
            "Other"
        ], key="doc_type")
        party = st.text_input("Your Party Name (optional)", placeholder="e.g. ABC Corp or John Doe", key="party_name")

    legal_btn = st.button("Analyze Document", key="legal_btn")

    if legal_btn:
        if legal_file is None:
            st.warning("Please upload a legal document first!")
        else:
            legal_text = get_text(legal_file)

            if legal_text:
                party_part = ""
                if party:
                    party_part = "\nReviewing from perspective of: " + party

                prompt = "You are an experienced legal analyst specializing in contract review.\n\nDocument Type: " + doc_type + party_part + "\n\nDocument:\n---\n" + legal_text[:10000] + "\n---\n\nGive a thorough legal analysis in this exact format:\n\n## Document Overview\n[Document type, parties involved, effective date, duration]\n\n##  High-Risk Clauses (Red Flags)\n[List risky or problematic clauses]\n\n## Clauses Requiring Attention\n[List clauses that need review]\n\n## Standard and Favorable Clauses\n[List clauses that are standard or favorable]\n\n##  Key Dates and Deadlines\n[List all important dates and notice periods]\n\n##  Financial Obligations\n[List all financial terms, payments, penalties]\n\n## Confidentiality and IP\n[Summarize IP ownership and confidentiality]\n\n##  Termination Conditions\n[How can this be terminated? What are the penalties?]\n\n##  Missing or Ambiguous Clauses\n[Identify missing standard clauses]\n\n##  Negotiation Recommendations\n[Top 5 recommendations before signing]\n\n##  Summary\n[Overall risk level: LOW / MEDIUM / HIGH, and key takeaway]"

                with st.spinner("Analyzing legal document..."):
                    result = get_ai_response(prompt)

                st.markdown("<div class='result-box'>" + result.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
                st.download_button("⬇️ Download Analysis", data=result, file_name="legal_analysis.txt", mime="text/plain")


# ==============================================================================
# PAGE: RESEARCH SUMMARIZER
# ==============================================================================
elif current_page == "Research Summarizer":

    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;margin-bottom:6px;'>Research Paper Summarizer</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888899;margin-bottom:24px;'>Break down research papers into clear, structured insights in seconds.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        research_file = st.file_uploader("Upload Research Paper", type=["pdf", "txt", "docx"], key="research_upload")

    with col2:
        audience = st.selectbox("Explain for:", [
            "Expert Researcher",
            "Graduate Student",
            "Industry Professional",
            "General Public (Simple English)"
        ], key="audience")

        focus_areas = st.multiselect("Focus Areas", [
            "Methodology",
            "Key Findings",
            "Limitations",
            "Future Work",
            "Statistical Analysis",
            "Practical Applications"
        ], default=["Key Findings", "Methodology"], key="focus")

    research_btn = st.button("Summarize Paper", key="research_btn")

    if research_btn:
        if research_file is None:
            st.warning("Please upload a research paper first!")
        else:
            paper_text = get_text(research_file)

            if paper_text:
                focus_str = ", ".join(focus_areas) if focus_areas else "all sections"

                prompt = "You are an expert research analyst and science communicator.\n\nTarget Audience: " + audience + "\nFocus Areas: " + focus_str + "\n\nResearch Paper:\n---\n" + paper_text[:10000] + "\n---\n\nGive a comprehensive research summary in this exact format:\n\n##  Paper Overview\n- **Title**: [paper title]\n- **Authors and Institution**: [if mentioned]\n- **Published**: [date/journal if mentioned]\n- **Research Type**: [empirical / theoretical / review / meta-analysis]\n\n##  Core Research Question\n[What problem does this paper address?]\n\n## Key Hypothesis\n[What is the central claim?]\n\n## Methodology\n[How was the research conducted?]\n\n##  Key Findings and Results\n[Most important findings with data]\n\n##  Novel Contribution\n[What is NEW about this research?]\n\n## Limitations and Caveats\n[What are the limitations?]\n\n##  Real-World Applications\n[How can findings be applied in practice?]\n\n##  Future Research Directions\n[What follow-up work is suggested?]\n\n## 🧠 Simple English Summary\n[Explain in 3-4 sentences for a non-expert]\n\n## ⭐ Research Impact\n[Rate: LOW / MEDIUM / HIGH impact with justification]"

                with st.spinner("Analyzing research paper..."):
                    result = get_ai_response(prompt)

                st.markdown("<div class='result-box'>" + result.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
                st.download_button("⬇️ Download Summary", data=result, file_name="research_summary.txt", mime="text/plain")
