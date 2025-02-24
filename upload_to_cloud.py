import cloudinary
import cloudinary.uploader
import pyttsx3 
import os 

cloudinary.config( 
  cloud_name = os.environ.get("CLOUD_NAME"),
  api_key = os.environ.get("CLOUDINARY_API_KEY"),
  api_secret = os.environ.get("CLOUDINARY_API_SECRET") 
)

def save_audio(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, "audio/audio.mp3")
    engine.runAndWait()

response = cloudinary.uploader.upload("audio/audio.mp3", resource_type="video")

# check is audio was uploaded sucessfully
if response["public_id"] == "audio/audio":
    print("Audio uploaded successfully")
    print(response["secure_url"])

# save the secure url
url = response["secure_url"]