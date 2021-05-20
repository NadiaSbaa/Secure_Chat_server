import pymongo
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as syrine
import base64
import binascii
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["python_chat"]
mycol = mydb["clients"]

#client = { "carteid": "John", "firstname": "Highway 37" , "lastname": "John", "login": "Highway 37", "password": "Highway 37" , "certifRequest": "John", "certif": "Highway 37"}

#x = mycol.insert_one(client)
login = "NadiaSbaa"
l = "nadia"
password = sha256(l.encode('utf_8')).hexdigest()

#myquery = { "login": login, "password": password}
#newvalues = { "$set": { "certifRequest": "", "certif": ""} }
#mycol.update_one(myquery, newvalues)

#for x in mycol.find():
#  print(x)
#for x in mycol.find({"login": login, "password": password},{"certif"}):
#  if (x['certif'] != ''):
#    print("ClientAndCertified")
#  else:
#    print("ClientAndNotCertified")

#client = { "carteid": "2", "firstname": "Nadia" , "lastname": "Sbaa", "login": "NadiaSbaa", "password": "nadia" , "certifRequest": '', "certif": ''}
#x = mycol.insert_one(client)
origin = "NadiaSbaa"
filename = '../Client/keys/' + str(origin)
f = open(filename + '.cert','r')
key = RSA.import_key(f.read())
print(key)
cipher = syrine.new(key)
message = "hi"
ciphertext = cipher.encrypt(message.encode('utf8'))
encrypted = base64.b64encode(ciphertext).decode('ascii')
print("encrypted", encrypted)
f = open(filename + '.pkey','r')
key = RSA.import_key(f.read())
cipher = syrine.new(key)
ciphertext = base64.b64decode(encrypted.encode('ascii'))
plaintext = cipher.decrypt(ciphertext, b'DECRYPTION FAILED')
print("msg",plaintext.decode('utf8'))