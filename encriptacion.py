import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class Seguridad():
	"""Clase de de tipo Seguridad"""

	def __init__(self, key=None):
		"""Constructor de la clase de tipo Seguridad
		Si no se pasa la key, por defecto es None"""
		self.key = key

	def createKey(self, data):
		"""Método para crear la key en función de la contraseña a encriptar
			* data -> constaseña a encriptar con la que se va a crear la key
		"""
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
		"""Método para encriptar la contraseña
			* data -> constaseña a encriptar
			* return la contraseña ya encriptada en formato de bytes
		"""
		self.createKey(data)
		f = Fernet(self.key)
		encrypted = f.encrypt(data.encode())
		return encrypted
			 
	def decrypt(self, dataEncrypt):
		"""Método para desencriptar la contraseña
			* data -> constraseña ya encriptada
			* return la contraseña ya desencriptada en formato de bytes
		"""
		f = Fernet(self.key)
		decrypted = f.decrypt(dataEncrypt)
		return decrypted

#s = Seguridad()
#s.createKey("12345Ral")
#print(s.key)
#dataENc = s.encrypt(s.key, "12345Ral")
#print(dataENc)
#print(s.decrypt(s.key, dataENc))