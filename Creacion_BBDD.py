import sqlite3 as sql

conexion = None
cursor = None

def getConexion():
	"""Devuelve la conexion de la BBDD"""
	global conexion
	return conexion

def getCursor():
	"""Devuelve el cursor de la BBDD"""
	global cursor
	return cursor

def crear_db():
	"""Método para crear las tablas de la BBDD"""
	global conexion
	global cursor

	conexion = sql.connect("contrasennas.db")
	try:
		cursor = conexion.cursor()
		cursor.execute("""
			CREATE TABLE usuarios(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nick VARCHAR(100) UNIQUE NOT NULL,
			pass VARCHAR(300) NOT NULL)
			""")
	except sql.OperationalError as ex:
		print(type(ex).__name__)
		print("Las tabla ya existe")
	else:
		print("Tabla creada correctamente")

	try:	
		cursor.execute("""
			CREATE TABLE contrasenas(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			web VARCHAR(150), 
			username VARCHAR(50) NOT NULL, 
			password VARCHAR(300) NOT NULL, 
			id_usuario INTEGER NOT NULL,
			key VARCHAR(300) NOT NULL,
			FOREIGN KEY(id_usuario) REFERENCES usuarios(id))
			""")
	except sql.OperationalError as ex:
		print(type(ex).__name__)
		print("Las tabla ya existe")
	else:
		print("Tabla creada correctamente")