
import string
import Usuario as us
import Contrasena as cn
import encriptacion as enc
import cryptography
try:
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import pyperclip as pc
	import sqlite3 as sql
except Exception as ex:
	print('----------instalando libreria-----------')
	print(type(ex).__name__)
	import pip
	pip.main(['install', 'tkintertable'])
	pip.main(['install', 'random'])
	pip.main(['install', 'pyperclip'])
	pip.main(['install', 'pysqlite3'])
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import pyperclip as pc
	import sqlite3 as sql

def generatePassword(size, typeChar):
	# string.ascii_uppercase + string.ascii_lowercase
	return ''.join(random.choice(chooseCharacters(typeChar)) for _ in range(size))

def retry(size, typeChar):
	try:
		txtPass.configure(state='normal')
		#txtPass.delete(0,END)
		password.set(generatePassword(size, typeChar))
		#txtPass.insert(0,generatePassword(size, typeChar))
		txtPass.configure(state='readonly')
	except IndexError as ex:
		MessageBox.showinfo("Tipo de carácteres","Selecciona el tipo de carácteres de la contraseña")

def chooseCharacters(typeChar):
	var=''
	if typeChar == 1: # all characters
		var += string.ascii_letters + string.digits + string.punctuation
	elif typeChar == 2: # only letters
		var += string.ascii_letters
	elif typeChar == 3: # only numbers
		var += string.digits
	elif typeChar == 4: # letters and numbers
		var += string.ascii_letters + string.digits
	return var

def register():
	try:
		if nombre.get() != "" or passw.get() != "":
			clave = s.encrypt(str(passw.get()))
			print(type(clave))
			print(clave)
			cursor.execute("INSERT INTO usuarios VALUES (null, '{}','{}')".format(str(nombre.get()), clave.decode()))
			conexion.commit()
		else:
			MessageBox.showinfo("Registro","Debes rellenar el campo del nombre y de la contraseña")
	except sql.IntegrityError as ex:
		print(type(ex).__name__)
		MessageBox.showinfo("Registro","El usuario ya existe")
	else:
		MessageBox.showinfo("Registro","Usuario creado correctamente")
		login()

def login():
	global user, s
	#users = cursor.execute("SELECT * FROM usuarios").fetchall()
	#print(users)
	#s.createKey(str(passw.get()))
	#print(s.key)
	#users[1][2].encode()
	#print(s.decrypt(users[5][2].encode()))
	try:
		user = cursor.execute("SELECT * FROM usuarios WHERE nick = '{}'".format(str(nombre.get()))).fetchone()
		if user != None:
			s.key = None
			s.createKey(str(passw.get()))
			print(user[2].encode())
			decodificado = s.decrypt(user[2].encode())
			print(decodificado.decode())
			print(str(passw.get()))
	#		if decodificado.decode() == str(passw.get()):
	#			btnSave.config(state="normal")
	#		else:
	#			MessageBox.showinfo("Login","Contraseña incorrecta")
		else:
			MessageBox.showinfo("Login","Usuario no existe")
	except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken) as ex:
		print(type(ex).__name__)
		btnSave.config(state="disabled")
		btnBuscar.config(state="disabled")
		MessageBox.showinfo("Login","Contraseña incorrecta")
	else:
		btnSave.config(state="normal") if decodificado.decode() == str(passw.get()) else None
		btnBuscar.config(state="normal") if decodificado.decode() == str(passw.get()) else None


def savePassword():
	try:
		global user, s			
		clave = s.encrypt(str(password.get()))
		print(type(clave))
		print(clave)
		cursor.execute("INSERT INTO contrasenas VALUES (null, '{}','{}','{}', {})".format(web.get(), username.get(), clave.decode(), user[0]))
		conexion.commit()
	except Exception as ex:
		print(type(ex).__name__)
		MessageBox.showerror("Save","No se ha podido guardar la contraseña")
		conexion.rollback()

def btnViewContrasenas():
	global user
	p = StringVar()
	p.set(user[1])
	print(p.get())
	vContrasenas = Toplevel(root, padx=60, pady=10)
	vContrasenas.title("Contraseña")
	vContrasenas.resizable(0,0)
	Label(vContrasenas, text="Página web").grid(row=1, column=1)
	Entry(vContrasenas, textvariable=web, font=("Arial",12)).grid(row=1, column=2)
	Label(vContrasenas, text="Username").grid(row=2, column=1)
	Entry(vContrasenas, textvariable=username, font=("Arial",12)).grid(row=2, column=2)
	Label(vContrasenas, text="Contraseña").grid(row=3, column=1)
	Entry(vContrasenas, textvariable=password, font=("Arial",12)).grid(row=3, column=2)
	Label(vContrasenas, text="Usuario").grid(row=4, column=1)
	Entry(vContrasenas, textvariable=p, font=("Arial",12), state="disabled").grid(row=4, column=2)
	Button(vContrasenas, text="Guardar", command = savePassword).grid(row=5, column=1, columnspan=2)


def crear_db():
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
			FOREIGN KEY(id_usuario) REFERENCES usuarios(id))
			""")
	except sql.OperationalError as ex:
		print(type(ex).__name__)
		print("Las tabla ya existe")
	else:
		print("Tabla creada correctamente")

root = Tk()
s = enc.Seguridad()
conexion = None
cursor = None
user = None
n_characters = IntVar()
characters = IntVar()
password = StringVar()
passw = StringVar()
nombre = StringVar()
username = StringVar()
web = StringVar()
crear_db()
root.title("Generador de contraseñas")

root.resizable(0,0)
root.iconbitmap('keys.ico')
root.config(padx=15)

Label(root, text="Usuario").grid(row=1, column=1)
Entry(root, textvariable=nombre, font=("Arial",12)).grid(row=1, column=2)
Label(root, text="Contraseña").grid(row=1, column=3)
Entry(root, textvariable=passw, font=("Arial",12), show="*").grid(row=1, column=4)
Button(root, text="Registro", command = register).grid(row=1, column=5, sticky='w')
Button(root, text="Login", command = login).grid(row=1, column=5, padx=60)

txtPass = Entry(root, textvariable=password)
txtPass.grid(row=2, column=1, columnspan=6, padx=15, pady=15)
txtPass.config(width=30, justify="center", state="readonly", font=("Arial",30, "bold", "italic"), borderwidth=5, highlightbackground ='gray22', highlightthickness=3)

Label(root, text="Longitud de la contraseña", font=("Arial",12, "bold", "underline")).grid(row=3, column=1, sticky="w")
Radiobutton(root, text="8 carácteres", variable=n_characters, value=8, state="active").grid(row=3, column=2)
Radiobutton(root, text="12 carácteres", variable=n_characters, value=12, state="active").grid(row=3, column=3)
Radiobutton(root, text="16 carácteres", variable=n_characters, value=16, state="active").grid(row=3, column=4)
Radiobutton(root, text="20 carácteres", variable=n_characters, value=20, state="active").grid(row=3, column=5)

Label(root, text="Carácteres", font=("Arial",12, "bold", "underline")).grid(row=4, column=1, sticky="w")
Radiobutton(root, text="Todos carácteres", variable=characters, value=1, state="active").grid(row=4, column=2)
Radiobutton(root, text="Solo letras", variable=characters, value=2, state="active").grid(row=4, column=3)
Radiobutton(root, text="Solo números", variable=characters, value=3, state="active").grid(row=4, column=4)
Radiobutton(root, text="Letras y números", variable=characters, value=4, state="active").grid(row=4, column=5)

imagen1 = PhotoImage(file="retry.gif")
Button(root, image=imagen1, height = 55, width = 50, command = lambda: retry(n_characters.get(), characters.get())).grid(row=2, column=6)
imagen2 = PhotoImage(file="copy.gif")
Button(root, image=imagen2, height = 55, width = 50, command = lambda: pc.copy(password.get())).grid(row=2, column=7)
imagen3 = PhotoImage(file="save.gif")
btnSave = Button(root, image=imagen3, height = 55, width = 50, state="disabled", command = btnViewContrasenas)
btnSave.grid(row=2, column=8)
imagen4 = PhotoImage(file="find.gif")
btnBuscar = Button(root, image=imagen4, height = 55, width = 50, state="disabled")
btnBuscar.grid(row=2, column=9)


root.mainloop()