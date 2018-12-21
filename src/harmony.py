
from __future__ import print_function

import pyzbar.pyzbar as pyzbar

import numpy as np
import cv2
import time

import pygame

import firebase_admin

from firebase_admin import credentials

from firebase_admin import firestore

from firebase_admin import storage

from datetime import datetime


img_key = 0

dt = 0
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
music_file = "music.mp3"  
music_file2 = "music2.mp3"
music_file3 = "music3.mp3"

freq = 24000   
bitsize = -16   
channels = 1 
buffer = 2048   


cred = credentials.Certificate('serveceKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket' : 'hello-harmony.appspot.com'

})
bucket = storage.bucket()

db= firestore.client()


cap = cv2.VideoCapture(0)

cap.set(3,640)

cap.set(4,480)

time.sleep(2)

def decode(im) : 
    
    decodedObjects = pyzbar.decode(im)

    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
while(cap.isOpened()):
 
    ret, frame = cap.read()
   
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     

        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        
        else : 
          hull = points
         
   
        n = len(hull)     
   
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        
        y = decodedObject.rect.top

        print(x, y)
        barCode = str(decodedObject.data)

        #cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
        #cv2.putText(im, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
        
        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,'\n')
        
        key = str(decodedObject.data)
        key = key.replace("'","")
        key = key[1:]

        print('파이어베이스 전송키')
        print(key)
      
        print('QR코드가 입력되었습니다')
        print('키오스크 감지')

        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        pygame.mixer.quit()   

        doc_ref = db.collection(u'users').document(key)
        doc_ref.set({
        u'hash': key,
  
        })


        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.load(music_file2)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        pygame.mixer.quit()   

        time.sleep(0.1)
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.load(music_file3)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        pygame.mixer.quit() 
      
        img_key = 1
        dt = time.time()
        #cv2.imwrite('img1.jpg',im)




    cv2.imshow('frame',frame)
        

    cv2.imshow('BGR',im)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    if img_key == 1 :
        if(time.time() > dt +1 ):
            print("사진찍습니다")
            cv2.imwrite('img1.png',frame)
            blob = bucket.blob('img1.png')

            blob.upload_from_filename(filename='img1.png')
            print(blob.public_url)

            pygame.mixer.init(freq, bitsize, channels, buffer)
            pygame.mixer.music.load(music_file2)
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(30)
            pygame.mixer.quit() 

            dt = time.time()
            img_key = 0


            



cap.release()

cv2.destroyAllWindows()