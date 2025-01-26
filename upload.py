import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
from io import BytesIO
from database import conn

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

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
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            image = Image.open(uploaded_file)
            text = extract_text_from_image(image)
        
        if text.strip():
            # Store text in Neon database
            c = conn.cursor()
            c.execute("INSERT INTO texts (content) VALUES (%s) RETURNING id", (text,))
            text_id = c.fetchone()[0]  
            conn.commit()
            
            st.success(f"Text extracted! Your Document ID: **{text_id}**")
            
        else:
            st.warning("No text could be extracted")

elif option == "Take Picture":
    picture = st.camera_input("Take a picture")
    
    if picture:
        image = Image.open(BytesIO(picture.getvalue()))
        text = extract_text_from_image(image)
        
        if text.strip():
            # Store text in Neon database
            c = conn.cursor()
            c.execute("INSERT INTO texts (content) VALUES (%s) RETURNING id", (text,))
            text_id = c.fetchone()[0]  # Get the auto-generated ID
            conn.commit()
            
            st.success(f"Text extracted! Your Document ID: **{text_id}**")
            
        else:
            st.warning("No text could be extracted")