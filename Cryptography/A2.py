# Authors: Wanuch Inthiravoranont and Ekkasit Smithipanon
# Assignment: A2 Project
# Date: 04/13/2018

import hashlib
import os
import binascii
import ast
import dropbox
from dropbox.files import WriteMode
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.PublicKey import RSA

def readFile():
	input = open('input.txt','r') 
	message = input.read()
	input.close()	
	return message

def readPI():
	input = open('PI.pem','r') 
	PI = input.read()
	PI = RSA.importKey(PI)
	print(PI)
	input.close()
	return PI

def writeFile(M):
	file = open('output.txt','w+')
	file.write(M.decode('UTF-8'))
	file.close()

def writePU(key):
	print(key.exportKey('PEM'))
	file = open('PU.pem','wb')
	file.write(key.exportKey())
	file.close()

def writePI(key):
	print(key.exportKey('PEM'))
	file = open('PI.pem','wb')
	file.write(key.exportKey())
	file.close()

def generateKey(F):
	hash_object = hashlib.sha256(F.encode('utf-8'))
	key = hash_object.hexdigest()
	return key

def generateIV():
	iv = os.urandom(16)
	return iv

def encrypt_message(iv, key, plaintext):
	ctr = Counter.new(128, initial_value = int(binascii.hexlify(iv), 16))
	aes = AES.new(key, AES.MODE_CTR, counter = ctr)
	ciphertext = iv + aes.encrypt(plaintext)
	return ciphertext

def decrypt_ciphertext(key, ciphertext):
	iv = ciphertext[:16]
	ctr = Counter.new(128, initial_value = int(binascii.hexlify(iv), 16))
	aes = AES.new(key, AES.MODE_CTR, counter=ctr)
	message = aes.decrypt(ciphertext[16:])
	return message

def generateRSA_keys():
	private_key = RSA.generate(1024 ,Random.new().read)
	public_key = private_key.publickey()
	return private_key ,public_key

def connectDropBox():
	token= open("token.txt", "r") 
	token=token.read()
#	print(token)

# connect to dropbox api
	dbx = dropbox.Dropbox(token)
#	print(dbx.users_get_current_account())
	return dbx

def uploadFile(dbx, uploadedFile, path):
	dbx.files_upload(uploadedFile, path, mode = WriteMode('overwrite'))

def downloadFile(dbx, path):
	md, res = dbx.files_download(path)
	data = res.content
	return data

def main():
	while True:
		print('1. Generate public key & private key')
		print('2. Upload')
		print('3. Download')
		print('4. Exit')
		option = input('Please select the option: ')

		if option == '1':
# Read input file
			F = readFile()
			print('--------------------------------------------------------------')
			print('Input:')
			print(F)

# Generate key K with SHA-256 using F
			key = generateKey(F)
			H = key
			K = (key)[:32]
			print('--------------------------------------------------------------')
			print('Key:')
			print(K)

# Generate initial vector
			IV = generateIV()
			print('--------------------------------------------------------------')
			print('IV:')
			print(IV)	

# Encrypt the file F into a ciphertext C with AES in Counter mode (AES-CTR) under the key K
			C = encrypt_message(IV, K, F)
			print('--------------------------------------------------------------')
			print('Ciphertext:')
			print(C)
	
# Generate public key and private key for RSA
			private_key ,public_key = generateRSA_keys()
			writePU(public_key)
			writePI(private_key)

# Protect the key K by encrypting it into W using RSA public key
			W_array = public_key.encrypt(K.encode('utf-8'), 32)
			W = W_array[0]
			print('--------------------------------------------------------------')
			print('W:')
			print(W)

		if option == '2':
# Connect to dropbox
			dbx = connectDropBox()

# Upload both C and W  to the cloud storage server
			uploadFile(dbx, C, '/Apps/DB-MC-A2/C')
			uploadFile(dbx, W, '/Apps/DB-MC-A2/W')
			uploadFile(dbx, str.encode(H), '/Apps/DB-MC-A2/H')

			print('Upload successful')

		if option == '3':
# Download both C and W from the cloud storage server
			Dropbox_C = downloadFile(dbx, '/Apps/DB-MC-A2/C')
			print('--------------------------------------------------------------')
			print('C from Dropbox:')
			print(Dropbox_C)

			Dropbox_W = downloadFile(dbx, '/Apps/DB-MC-A2/W')
			print('--------------------------------------------------------------')
			print('W from Dropbox:')
			print(Dropbox_W)

# Extract the key K from W by the use of private RSA decryption key
			PI = readPI()
			Key = PI.decrypt(ast.literal_eval(str(Dropbox_W)))
			print('--------------------------------------------------------------')
			print('Key:')
			print(Key)

# Decrypting the ciphertext C with AES-CTR under the key K to recover the original file F
			M = decrypt_ciphertext(Key, Dropbox_C)

			print('--------------------------------------------------------------')
			print('Output:')
			print(M.decode('UTF-8'))

# Write output file
			writeFile(M)

		if option == '4':
			break

if __name__ == '__main__':
    main()