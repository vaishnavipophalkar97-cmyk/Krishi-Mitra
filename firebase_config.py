import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_farmer_profile(uid: str, name: str, region: str, crop: str, soil: str):
    """Saves or updates a unique profile record for a registered farmer."""
    doc_ref = db.collection("farmers").document(uid)
    doc_ref.set({
        "name": name,
        "region": region,
        "primary_crop": crop,
        "soil_type": soil
    })

def get_farmer_profile(uid: str) -> dict:
    """Fetches unique farmer profile details; defaults if not found."""
    doc_ref = db.collection("farmers").document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {"name": "Farmer", "region": "Unknown", "primary_crop": "General Crops", "soil_type": "Loam"}
    3