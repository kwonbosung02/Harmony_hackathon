#import requests

import firebase_admin


from firebase_admin import credentials

from firebase_admin import firestore

from firebase_admin import storage

cred = credentials.Certificate('serveceKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket' : 'hello-harmony.appspot.com'

})



bucket = storage.bucket()

blob = bucket.blob('img1.jpg')

blob.upload_from_filename(filename='img1.png')
print(blob.public_url)



db= firestore.client()
key = "bskwon0526@gmail.com"

doc_ref = db.collection(u'users').document(key)
doc_ref.set({
    u'hash': key,
  
})