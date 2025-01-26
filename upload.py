import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
from io import BytesIO
import requests

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error while reading the PDF: {e}")
        return ""

def extract_text_from_image(image):
    try:
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image)
        text = " ".join([result[1] for result in results])
        return text
    except Exception as e:
        st.error(f"Error while processing the image: {e}")
        return ""

st.title("Upload and Extract Text")

uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        image = Image.open(BytesIO(uploaded_file.read()))
        text = extract_text_from_image(image)
    
    if text.strip():
        st.success("Text extracted successfully!")
        display_url = st.text_input("Enter the display URL to forward the content:")
        if st.button("Forward Content"):
            if display_url:
                params = {"content": text}
                response = requests.get(display_url, params=params)
                if response.status_code == 200:
                    st.success("Content forwarded successfully!")
                else:
                    st.error("Failed to forward the content. Check the display URL.")
            else:
                st.warning("Please enter a valid display URL.")
    else:
        st.warning("No text could be extracted.")
