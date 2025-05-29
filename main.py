import streamlit as st
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")
st.title("📃 AI Resume Critiquer")
st.markdown("Upload your resume and get **AI-powered feedback** tailored to your target job role!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")
analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("❌ The uploaded file appears to be empty.")
            st.stop()

        messages = [
            {
                "role": "user",
                "content": f"""
You are a professional resume reviewer. Analyze the following resume and provide detailed feedback.
Resume content: {file_content}
Job Role Target: {job_role if job_role else 'General job applications'}

Focus your feedback on:
1. Content clarity and professionalism
2. Skills presentation and alignment with job roles
3. Description of work experience and impact
4. Suggestions for improvements (structure, wording, formatting)

Return the feedback in a structured format with bullet points and actionable suggestions.
"""
            }
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )

        st.markdown("### 📝 Analysis Results")
        # chat_completion.choices[0].message.content holds the reply text
        st.markdown(chat_completion.choices[0].message.content)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
