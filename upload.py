import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
from io import BytesIO
from database import conn

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    return " ".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_image(image):
    """Extract text from an image using EasyOCR."""
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image)
    return " ".join([result[1] for result in results])

# Main app
st.title("Document Processing Center")

option = st.radio("Choose input method", ("Upload Document", "Take Picture"))

if option == "Upload Document":
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file) if uploaded_file.type == "application/pdf" \
               else extract_text_from_image(Image.open(uploaded_file))
        
        if text.strip():
            # Store text in database and get auto-generated ID
            c = conn.cursor()
            c.execute("INSERT INTO texts (content) VALUES (?)", (text,))
            text_id = c.lastrowid  # Get the auto-incremented ID
            conn.commit()
            
            st.success(f"Text extracted! Your Document ID: **{text_id}**")
            st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text_id}")

elif option == "Take Picture":
    picture = st.camera_input("Take a picture")
    
    if picture:
        text = extract_text_from_image(Image.open(BytesIO(picture.getvalue())))
        
        if text.strip():
            # Store text in database and get auto-generated ID
            c = conn.cursor()
            c.execute("INSERT INTO texts (content) VALUES (?)", (text,))
            text_id = c.lastrowid  # Get the auto-incremented ID
            conn.commit()
            
            st.success(f"Text extracted! Your Document ID: **{text_id}**")
            st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text_id}")