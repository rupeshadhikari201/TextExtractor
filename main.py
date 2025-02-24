import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
import html
from io import BytesIO
import pyttsx3
import threading
import tempfile
import cloudinary
import cloudinary.uploader
import dotenv

dotenv.load_dotenv()
import os 

# Cloudinary Configuration
cloudinary.config( 
  cloud_name=os.getenv("CLOUD_NAME"),
  api_key=os.getenv("CLOUDINARY_API_KEY"),
  api_secret=os.getenv("CLOUDINARY_API_SECRET") 
)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text
    except Exception as e:
        st.error(f"An error occurred while reading the PDF: {e}")
        return ""

# Function to extract text from an image using EasyOCR
def extract_text_from_image(image):
    try:
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image)
        text = "\n".join([result[1] for result in results])
        return text
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")
        return ""

# Function to convert text to speech and upload to Cloudinary
def text_to_speech(text, action):
    if action == "play":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio_path = temp_audio.name
            
        engine = pyttsx3.init()
        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(audio_path, resource_type="video")
        
        if "secure_url" in response:
            st.audio(response["secure_url"], format="audio/mp3")
            st.success("Audio uploaded and playing!")
        else:
            st.error("Failed to upload audio.")

    elif action == "stop":
        st.warning("Stopping audio is not supported in Streamlit.")

# Streamlit App
st.title("Text Extractor: Upload a Document or Take a Picture")

# Select feature: Upload or Capture
option = st.radio("Choose input method", ("Upload Document", "Take Picture"))

if option == "Upload Document":
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        if text.strip():
            st.subheader("Extracted Text")
            st.write("Preview of the extracted text:")
            
            # Styling options
            font_size = st.slider("Font Size", 8, 48, 14)
            font_color = st.color_picker("Font Color", "#000000")
            bg_color = st.color_picker("Background Color", "#ffffff")
            
            st.markdown(
                f"""<div style='background-color: {bg_color}; color: {font_color}; 
                font-size: {font_size}px; padding: 10px; border-radius: 5px; white-space: pre-line;'>{html.escape(text)}</div>""",
                unsafe_allow_html=True,
            )
            
            if st.button("Read Aloud"):
                text_to_speech(text, "play")
        else:
            st.warning("No text could be extracted from the PDF.")

elif option == "Take Picture":
    picture = st.camera_input("Take a picture")
    if picture is not None:
        image = Image.open(BytesIO(picture.read()))
        text = extract_text_from_image(image)
        if text.strip():
            st.subheader("Extracted Text")
            st.write("Preview of the extracted text:")
            
            # Styling options
            font_size = st.slider("Font Size", 8, 48, 14)
            font_color = st.color_picker("Font Color", "#000000")
            bg_color = st.color_picker("Background Color", "#ffffff")
            
            st.markdown(
                f"""<div style='background-color: {bg_color}; color: {font_color}; 
                font-size: {font_size}px; padding: 10px; border-radius: 5px; white-space: pre-line;'>{html.escape(text)}</div>""",
                unsafe_allow_html=True,
            )
            
            if st.button("Read Aloud"):
                text_to_speech(text, "play")
        else:
            st.warning("No text could be extracted from the image.")
else:
    st.info("Choose an option to begin.")
