import streamlit as st
from version3 import ATSScanner

st.title("🚀 Smart ATS Resume Scanner")
st.write("Upload your Resume and paste the Job Description to see if you survive the robots.")

jd_input = st.text_area("Paste Job Description:")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if st.button("Scan Resume") and uploaded_file and jd_input:
    scanner = ATSScanner()
    
    # Save uploaded file temporarily
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    resume_text = scanner.extract_text_from_resume(uploaded_file)
    
    # Run Analysis
    set_score, matches, missing = scanner.scan(resume_text, jd_input)
    cosine_score = scanner.calculate_cosine_similarity(resume_text, jd_input)
    
    # Display
    col1, col2 = st.columns(2)
    col1.metric("Keyword Match", f"{set_score:.1f}%")
    col2.metric("AI Match", f"{cosine_score:.1f}%")
    
    if missing:
        st.error(f"Missing Keywords: {', '.join(list(missing)[:10])}")
    else:
        st.success("Perfect Keyword Match!")