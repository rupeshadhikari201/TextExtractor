import streamlit as st
from database import db  # Import Firestore client
from firebase_admin import firestore
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
from io import BytesIO
import random
import string

def generate_readable_id(length=5):
    """Generate a random alphanumeric ID."""
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))

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

def save_text_to_firebase(text):
    """Save text to Firebase Firestore."""
    try:
        # Generate a readable ID for the text
        text_id = generate_readable_id()
        
        # Save the text to Firestore
        db.collection("texts").document(text_id).set({
            "content": text,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return text_id
    except Exception as e:
        st.error(f"Error saving text to Firebase: {e}")
        return None

def main():
    st.title("Text Upload App")

    # Select input method
    option = st.radio("Choose input method", ("Upload Document", "Take Picture"))

    if option == "Upload Document":
        uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
        
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                # Extract text from PDF
                text = extract_text_from_pdf(uploaded_file)
            else:
                # Extract text from image
                image = Image.open(uploaded_file)
                text = extract_text_from_image(image)
            
            if text.strip():
                # Save text to Firebase
                text_id = save_text_to_firebase(text)
                if text_id:
                    st.success(f"Text extracted! Your Document ID: **{text_id}**")
                    # st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text_id}")
            else:
                st.warning("No text could be extracted")

    elif option == "Take Picture":
        picture = st.camera_input("Take a picture")
        
        if picture:
            # Extract text from image
            image = Image.open(BytesIO(picture.getvalue()))
            text = extract_text_from_image(image)
            
            if text.strip():
                # Save text to Firebase
                text_id = save_text_to_firebase(text)
                if text_id:
                    st.success(f"Text extracted! Your Document ID: **{text_id}**")
                    # st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text_id}")
            else:
                st.warning("No text could be extracted")

if __name__ == "__main__":
    main()