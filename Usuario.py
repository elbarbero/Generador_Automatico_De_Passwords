class Usuario():
	def __init__(self, identicador, nick, password, contrasenas = []):
		self.id = identicador
		self.nick = nick
		self.password = password
		self.contrasenas = contrasenas

	def __str__(self):
		return "Usario {}".format(self.nick)

