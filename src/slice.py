import time


dt = time.time()

while True:

    if(time.time() > dt+1):

        print(time.time())
        dt = time.time()
