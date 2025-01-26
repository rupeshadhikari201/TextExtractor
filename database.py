import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    """Initialize Firebase Admin SDK if not already initialized."""
    try:
        # Check if Firebase app is already initialized
        if not firebase_admin._apps:
            # Load Firebase credentials
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully!")
        else:
            print("Firebase already initialized.")
        
        # Return Firestore client
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise

# Initialize Firestore
db = init_firebase()