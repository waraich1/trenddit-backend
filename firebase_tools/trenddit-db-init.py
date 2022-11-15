import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./firebase_tools/trenddit-db-cred.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()
docs = db.collection(u'sample1').get()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')



