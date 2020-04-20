
import string
from Usuario import *
from Contrasena import *
import Creacion_BBDD as bd
import encriptacion as enc
try:
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import pyperclip as pc
	import sqlite3 as sql
	import cryptography
except Exception as ex:
	print('----------instalando libreria-----------')
	print(type(ex).__name__)
	import pip
	pip.main(['install', 'tkintertable'])
	pip.main(['install', 'random'])
	pip.main(['install', 'pyperclip'])
	pip.main(['install', 'pysqlite3'])
	pip.main(['install', 'cryptography'])
	pip.main(['install', 'pybase64'])
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import pyperclip as pc
	import sqlite3 as sql
	import cryptography

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
	try:
		decodificado = b''
		u = cursor.execute("SELECT * FROM usuarios WHERE nick = '{}'".format(str(nombre.get()))).fetchone()
		if u != None:
			s.key = None
			s.createKey(str(passw.get()))
			decodificado = s.decrypt(u[2].encode())
			del(user)
			user = Usuario(u[0], u[1], u[2])
			findAllPassword()
		else:
			MessageBox.showinfo("Login","Usuario no existe")
			btnSave.config(state="disabled")
			btnBuscar.config(state="disabled")
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
		global user, s, vSaveContrasenas
		if username.get() != '' and password.get() != '' and web.get() != '':
			clave = s.encrypt(str(password.get()))
			cursor.execute("INSERT INTO contrasenas VALUES (null, '{}','{}','{}', {}, '{}')".format(web.get(), username.get(), clave.decode(), user.id, s.key.decode()))
			conexion.commit()
			cs = cursor.execute("SELECT * FROM contrasenas WHERE id_usuario = '{}'".format(user.id)).fetchall()
			decodificado = s.decrypt(clave)
			user.contrasenas.append(Contrasena(cs[-1][0], cs[-1][1], cs[-1][2], decodificado.decode()))
			#vSaveContrasenas.quit()
			password.set("")
			username.set("")
			web.set("")
		else:
			MessageBox.showinfo("Guardar contraseña","Debes rellenar los campos antes de poder guarda la contraseña")
	except Exception as ex:
		print(type(ex).__name__)
		MessageBox.showerror("Save","No se ha podido guardar la contraseña")
		conexion.rollback()
	except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken) as ex:
		print(type(ex).__name__)
		MessageBox.showerror("Save","No se ha podido guardar la contraseña")

def findAllPassword():
	global user, s
	try:
		cs = cursor.execute("SELECT * FROM contrasenas WHERE id_usuario = '{}'".format(user.id)).fetchall()
		if cs != None:
			for c in cs:
				s.key = c[5].encode()
				decodificado = s.decrypt(c[3].encode())
				user.contrasenas.append(Contrasena(c[0], c[1], c[2], decodificado.decode()))
			#[print(n) for n in user.contrasenas]
	except sql.IntegrityError as ex:
		print(type(ex).__name__)
	except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken) as ex:
		print(type(ex).__name__)


def btnSaveContrasenas():
	global user, vSaveContrasenas
	p = StringVar()
	p.set(user.nick)
	vSaveContrasenas = Toplevel(root, padx=60, pady=10)
	vSaveContrasenas.title("Contraseñas")
	vSaveContrasenas.resizable(0,0)
	Label(vSaveContrasenas, text="Página web").grid(row=1, column=1)
	Entry(vSaveContrasenas, textvariable=web, font=("Arial",12)).grid(row=1, column=2)
	Label(vSaveContrasenas, text="Username").grid(row=2, column=1)
	Entry(vSaveContrasenas, textvariable=username, font=("Arial",12)).grid(row=2, column=2)
	Label(vSaveContrasenas, text="Contraseña").grid(row=3, column=1)
	Entry(vSaveContrasenas, textvariable=password, font=("Arial",12)).grid(row=3, column=2)
	Label(vSaveContrasenas, text="Usuario").grid(row=4, column=1)
	Entry(vSaveContrasenas, textvariable=p, font=("Arial",12), state="disabled").grid(row=4, column=2)
	Button(vSaveContrasenas, text="Guardar", command = savePassword).grid(row=5, column=1, columnspan=2)

def btnViewContrasenas():
	vContrasenas = Toplevel(root, padx=60, pady=10)
	vContrasenas.title("Contraseña")
	vContrasenas.resizable(0,0)
	createWidget(vContrasenas)

def createWidget(vContrasenas):
	global user
	try:
		miPass = StringVar()
		miUsername = StringVar()
		miWeb = StringVar()
		index = 1

		lista = vContrasenas.grid_slaves()
		for l in lista:
			l.destroy()

		Label(vContrasenas, text="", font=("Arial",12, "bold", "underline")).grid(row=index, column=1)
		Label(vContrasenas, text="Web", font=("Arial",12, "bold", "underline")).grid(row=index, column=2)
		Label(vContrasenas, text="Username", font=("Arial",12, "bold", "underline")).grid(row=index, column=3)
		Label(vContrasenas, text="Contraseña", font=("Arial",12, "bold", "underline")).grid(row=index, column=4)

		img1 = PhotoImage(file="pencil.gif")
		img2 = PhotoImage(file="delete.gif")

		for c in user.contrasenas:
			index+=1
			miWeb.set(c.web)
			miUsername.set(c.username)
			miPass.set(c.password)
			Checkbutton(vContrasenas, variable = check, onvalue=f'{c.id}', offvalue=-1).grid(row=index, column=1)
			Label(vContrasenas, text=f'{c.web}', font=("Arial",10)).grid(row=index, column=2)
			Label(vContrasenas, text=f'{c.username}', font=("Arial",10)).grid(row=index, column=3)
			Label(vContrasenas, text=f'{c.password}', font=("Arial",10)).grid(row=index, column=4)
			#Button(vContrasenas, image = "pencil.gif", height = 25, width = 25).grid(row=index, column=5)
			#Button(vContrasenas, image = "delete.gif", height = 25, width = 25).grid(row=index, column=6)
		Button(vContrasenas, text = "Borrar selecionada", command=lambda: deletePassword(vContrasenas) if len(user.contrasenas) > 0 and int(check.get()) >-1 else None).grid(row=index+1, column=1, columnspan=2)
		Button(vContrasenas, text = "Modificar selecionada", command=lambda: deletePassword(vContrasenas) if len(user.contrasenas) > 0 and int(check.get()) >-1 else None).grid(row=index+1, column=4, columnspan=2)
	except Exception as ex:
		print(type(ex).__name__)


def deletePassword(vContrasenas):
	print(check.get())
	cursor.execute("DELETE FROM contrasenas WHERE id='{}'".format(check.get()))
	conexion.commit()
	first_or_default = next((n for n in user.contrasenas if n.id==check.get()), None)
	user.contrasenas.remove(first_or_default)
	#[print(n) for n in user.contrasenas]
	createWidget(vContrasenas)


# ******************* VARIABLES ******************
root = Tk()
bd.crear_db()
vSaveContrasenas = '' # Interfaz para guardar las contraseñas
s = enc.Seguridad() # Objeto de tipo encriptacion
conexion = bd.getConexion() # La conexion de la bbdd
cursor = bd.getCursor() #El cursor de la bbdd
user = None # Objeto de tipo Usuario
check = IntVar() # Variable de los checkbuttons para saber que contraseña borra
check.set(-1)
n_characters = IntVar() # Variable de los radiokbuttons para saber la longitud de la contraseña
characters = IntVar() # Variable de los radiobuttons para saber el tipo de caracteres para crear la contraseña
password = StringVar() # Variable de los Enty Widget con la contraseña ya generada
passw = StringVar() # Variable del password del usuario cuando se loguea
nombre = StringVar() # Variable del nombre del usuario cuando se loguea
username = StringVar() # Variable del nick que esta asociado a una contraseña al guardarla en la pantalla vContrasenas
web = StringVar() # Variable de la web que esta asociada a una contraseña al guardarla en la pantalla vContrasenas

root.title("Generador de contraseñas")

root.resizable(0,0)
root.iconbitmap('keys.ico')
root.config(padx=15)


# ******************* INTERFAZ ******************
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
btnSave = Button(root, image=imagen3, height = 55, width = 50, state="disabled", command = btnSaveContrasenas)
btnSave.grid(row=2, column=8)
imagen4 = PhotoImage(file="find.gif")
btnBuscar = Button(root, image=imagen4, height = 55, width = 50, state="disabled", command = btnViewContrasenas)
btnBuscar.grid(row=2, column=9)

root.mainloop()