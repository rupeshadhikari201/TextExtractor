import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image
import html
from io import BytesIO
# import pyttsx3  # For text-to-speech

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"An error occurred while reading the PDF: {e}")
        return ""

def extract_text_from_image(image):
    """Extract text from an image using EasyOCR."""
    try:
        reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU for Streamlit deployment
        results = reader.readtext(image)
        text = " ".join([result[1] for result in results])  # Combine all text segments
        return text
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")
        return ""

# def text_to_speech(text):
#     """Convert text to speech."""
#     try:
#         engine = pyttsx3.init()
        
#         """ Rate"""
#         rate = engine.getProperty('rate')
#         print(rate)
#         engine.setProperty('rate', 100)
        
        
#         engine.say(text)
#         engine.runAndWait()
#     except Exception as e:
#         st.error(f"An error occurred during text-to-speech: {e}")

# Streamlit App
st.title("Text Extractor: Upload a Document or Take a Picture")

# Select feature: Upload or Capture
option = st.radio("Choose input method", ("Upload Document", "Take Picture"))

if option == "Upload Document":
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_file)

        if text.strip():
            st.subheader("Extracted Text")
            st.write("Preview of the extracted text:")

            # Add text customization options
            font_size = st.slider("Font Size", 8, 48, 14)
            font_color = st.color_picker("Font Color", "#000000")
            bg_color = st.color_picker("Background Color", "#ffffff")

            # Apply styles to the text
            st.markdown(
                (
                    f"<div style='background-color: {bg_color}; color: {font_color}; "
                    f"font-size: {font_size}px; padding: 10px; border-radius: 5px;'>"
                    f"{html.escape(text)}"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            # Add a button to read the text aloud
            # if st.button("Read Aloud"):
            #     text_to_speech(text)
        else:
            st.warning("No text could be extracted from the PDF.")

elif option == "Take Picture":
    picture = st.camera_input("Take a picture")

    if picture is not None:
        # Convert image to a PIL Image object
        image = Image.open(BytesIO(picture.read()))

        # Extract text using EasyOCR
        text = extract_text_from_image(image)

        if text.strip():
            st.subheader("Extracted Text")
            st.write("Preview of the extracted text:")

            # Add text customization options
            font_size = st.slider("Font Size", 8, 48, 14)
            font_color = st.color_picker("Font Color", "#000000")
            bg_color = st.color_picker("Background Color", "#ffffff")

            # Apply styles to the text
            st.markdown(
                (
                    f"<div style='background-color: {bg_color}; color: {font_color}; "
                    f"font-size: {font_size}px; padding: 10px; border-radius: 5px;'>"
                    f"{html.escape(text)}"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            # Add a button to read the text aloud
            if st.button("Read Aloud"):
                text_to_speech(text)
        else:
            st.warning("No text could be extracted from the image.")
else:
    st.info("Choose an option to begin.")
