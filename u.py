import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
from io import BytesIO
import urllib.parse

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_image(image):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image)
    return " ".join([result[1] for result in results])

# Main processing app
st.title("Document Processing Center")

option = st.radio("Choose input method", ("Upload Document", "Take Picture"))
display_app_url = "https://display.streamlit.app"  

if option == "Upload Document":
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            image = Image.open(uploaded_file)
            text = extract_text_from_image(image)
        
        if text.strip():
            encoded_text = urllib.parse.quote(text.encode('utf-8'))
            redirect_url = f"{display_app_url}?text={encoded_text}"
            st.markdown(f"[View Enhanced Version]({redirect_url})")
        else:
            st.warning("No text could be extracted")

elif option == "Take Picture":
    picture = st.camera_input("Take a picture")
    
    if picture:
        image = Image.open(BytesIO(picture.getvalue()))
        text = extract_text_from_image(image)
        
        if text.strip():
            encoded_text = urllib.parse.quote(text.encode('utf-8'))
            redirect_url = f"{display_app_url}?text={encoded_text}"
            st.markdown(f"[View Enhanced Version]({redirect_url})")
        else:
            st.warning("No text could be extracted")