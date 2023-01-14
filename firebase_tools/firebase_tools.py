from logging import Filterer
from flask import redirect
import praw
from os import environ
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseC:
    cred = credentials.Certificate("./firebase_tools/trenddit-db-cred.json")
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    def get_token(self):
        token = FirebaseC.db.collection("access_token").document("outh").get()
        result = token.to_dict()
        return result["access_token"]
