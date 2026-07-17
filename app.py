import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# .env फाइल से API Key लोड करना
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 1. PDF से टेक्स्ट एक्सट्रैक्ट करने का फंक्शन
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += page_obj.extract_text() or ""
    return text

# 2. Gemini API से रिस्पॉन्स लेने का फंक्शन
def get_gemini_response(input_prompt):
    # हमने यहाँ मॉडल अपडेट करके 2.5-flash कर दिया है
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(input_prompt)
    return response.text

# 3. Streamlit UI डिज़ाइन
st.set_page_config(page_title="Smart ATS Resume Scanner", layout="wide")
st.title("🤖 AI Resume Scanner (ATS Checker)")
st.subheader("अपने रिज्यूमे को जॉब डिस्क्रिप्शन के अनुसार ऑप्टिमाइज़ करें")

# दो कॉलम्स बनाना (एक तरफ Job Description, दूसरी तरफ Resume Upload)
col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("📋 Job Description (JD) यहाँ पेस्ट करें:", height=300)

with col2:
    uploaded_file = st.file_uploader("📤 अपना रिज्यूमे अपलोड करें (PDF Format)", type="pdf")

submit = st.button("Analyze Resume")

# 4. बैकएंड लॉजिक (बटन क्लिक होने पर)
if submit:
    if uploaded_file is not None and jd != "":
        with st.spinner("AI आपके रिज्यूमे का विश्लेषण कर रहा है... कृपया प्रतीक्षा करें..."):
            # PDF से टेक्स्ट निकालना
            resume_text = input_pdf_text(uploaded_file)
            
            # प्रॉम्प्ट तैयार करना
            input_prompt = f"""
            Hey Act Like a skilled or very experienced ATS (Application Tracking System)
            with a deep understanding of tech field, software engineering, and web development.
            Your task is to evaluate the resume based on the given job description.
            You must provide:
            1. Match Percentage (how well the resume matches the JD)
            2. Missing Keywords (important keywords/skills from JD missing in the resume)
            3. Profile Summary & Recommendations (how to improve the resume)
            
            Resume Text: {resume_text}
            Job Description: {jd}
            
            Please provide the response in a structured markdown format.
            """
            
            # Gemini से रिस्पॉन्स प्राप्त करना
            response = get_gemini_response(input_prompt)
            st.success("विश्लेषण पूरा हुआ!")
            st.markdown("### 📊 AI Analysis Report")
            st.write(response)
    else:
        st.error("कृपया Job Description पेस्ट करें और Resume अपलोड करें!")