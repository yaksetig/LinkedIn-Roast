import os
import tempfile

import pdfkit
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader


st.title("LinkedIn Roast Generator")

st.write(
    "Enter a public LinkedIn profile URL and an API key for Google\u2019s Gemini to receive a humorous roast of the profile."
)

linkedin_url = st.text_input("LinkedIn Profile URL")
api_key = st.text_input("Gemini API Key", type="password")

if st.button("Generate Roast"):
    if not linkedin_url:
        st.error("Please provide a LinkedIn profile URL.")
    elif not api_key:
        st.error("Please provide your Gemini API key.")
    else:
        try:
            # Download the LinkedIn page as PDF using pdfkit
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdfkit.from_url(linkedin_url, tmp_pdf.name)
                pdf_path = tmp_pdf.name

            # Extract text from the generated PDF
            reader = PdfReader(pdf_path)
            profile_text = "\n".join(page.extract_text() or "" for page in reader.pages)

            # Query Gemini to obtain the roast
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                f"Roast this LinkedIn profile in a humorous manner:\n{profile_text}"
            )
            roast = response.text

            st.subheader("Roast")
            st.write(roast)

            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="profile.pdf")

            os.remove(pdf_path)
        except Exception as e:
            st.error(f"Failed to process the LinkedIn profile: {e}")
