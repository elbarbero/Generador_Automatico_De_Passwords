import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class Seguridad():

	def __init__(self, key=None):
		self.key = key

	def createKey(self, data):
		password = data.encode() # Convert to type bytes
		salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=100000,
			backend=default_backend()
		)
		self.key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

	def encrypt(self, data):
		self.createKey(data) if self.key == None else self.key
		f = Fernet(self.key)
		encrypted = f.encrypt(data.encode())
		return encrypted
			 
	def decrypt(self, dataEncrypt):
		f = Fernet(self.key)
		decrypted = f.decrypt(dataEncrypt)
		return decrypted

#s = Seguridad()
#s.createKey("12345Ral")
#print(s.key)
#dataENc = s.encrypt(s.key, "12345Ral")
#print(dataENc)
#print(s.decrypt(s.key, dataENc))