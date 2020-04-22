class Usuario():
	"""Clase de tipo Usuario"""

	def __init__(self, identicador, nick, password, contrasenas = []):
		"""Constructor de la clase de tipo Usuario"""
		self.id = identicador
		self.nick = nick
		self.password = password
		self.contrasenas = contrasenas

	def __str__(self):
		return "Usario {}".format(self.nick)

	def __del__(self):
		self.contrasenas.clear()

