import json
import os

import firebase_admin
from firebase_admin import credentials

from dotenv import load_dotenv

load_dotenv()

FIREBASE_SERVICE_ACCOUNT_CREDENTIALS = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"])

cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_CREDENTIALS)
firebase_app = firebase_admin.initialize_app(cred)