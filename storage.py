import sys
import hashlib
import uuid
import os
import shutil

store = '/home/eran/Desktop/temp'

def add_file(stream):
    md5 = hashlib.md5()
    id = str(uuid.uuid4())

    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    # sha1 = hashlib.sha1()

    # with open(filepath, 'rb') as f:
    content = stream.read()
    # while True:
    #     data = stream.read(BUF_SIZE)
    #     if not data:
    #         break
    md5.update(content)
        # sha1.update(data)

    id = md5.hexdigest()
    newfile = os.path.join(store,id)

    if(not os.path.isfile(newfile)):
        f = open(newfile, 'wb')
        f.write(content)
        f.close
    return id