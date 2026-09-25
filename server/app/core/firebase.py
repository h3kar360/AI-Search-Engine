from pathlib import Path

import firebase_admin
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_PATH = BASE_DIR / "secrets" / "firebase-service-account.json";

cred = credentials.Certificate(CREDENTIALS_PATH)
firebase_app = firebase_admin.initialize_app(cred)