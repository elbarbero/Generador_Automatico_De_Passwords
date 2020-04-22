
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
	"""Método para generar una contraseña en función de una longitud y tipo de carácteres proporcionados
		* size -> longitud de la constaseña
		* typeChar -> tipos de carácteres con la que se va a crear la contraseña. Se le pasa un número en funcion del radiobutton seleccionado
		* return la contraseña ya generada
	"""
	# string.ascii_uppercase + string.ascii_lowercase
	return ''.join(random.choice(chooseCharacters(typeChar)) for _ in range(size))

def retry(size, typeChar):
	"""Método del botón para volver a generar una contraseña en función de una longitud y tipo de carácteres proporcionados
		* size -> longitud de la constaseña
		* typeChar -> tipos de carácteres con la que se va a crear la contraseña. Se le pasa un número en funcion del radiobutton seleccionado
	"""
	# string.ascii_uppercase + string.ascii_lowercase
	try:
		txtPass.configure(state='normal')
		#txtPass.delete(0,END)
		password.set(generatePassword(size, typeChar))
		#txtPass.insert(0,generatePassword(size, typeChar))
		txtPass.configure(state='readonly')
	except IndexError as ex:
		print(printExceptionMessage())
		MessageBox.showinfo("Tipo de carácteres","Selecciona el tipo de carácteres de la contraseña")

def chooseCharacters(typeChar):
	"""Método para elegir el tipo de carácteres
		* typeChar -> tipos de carácteres con la que se va a crear la contraseña. Se le pasa un número en funcion del radiobutton seleccionado
		* return el tipo de caracteres
	"""
	# string.ascii_uppercase + string.ascii_lowercase
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
	"""
		Método para registar al usuario con su clave encriptada en la BBDD.
	"""
	try:
		if nombre.get() != "" or passw.get() != "":
			clave = s.encrypt(str(passw.get()))
			cursor.execute("INSERT INTO usuarios VALUES (null, '{}','{}')".format(str(nombre.get()), clave.decode()))
			conexion.commit()
		else:
			MessageBox.showinfo("Registro","Debes rellenar el campo del nombre y de la contraseña")
	except sql.IntegrityError as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())
		MessageBox.showinfo("Registro","El usuario ya existe")
	else:
		MessageBox.showinfo("Registro","Usuario creado correctamente")
		login()

def login():
	"""
		Método para logearse en la aplicación si los datos que ha introducido en los campos son correctos y 
		deben de corresponder con los datos que hay en la BBD que introdujo cuando se registró en la aplicación.
	"""
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
	except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken, sql.IntegrityError) as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())
		btnSave.config(state="disabled")
		btnBuscar.config(state="disabled")
		MessageBox.showinfo("Login","Contraseña incorrecta")
	else:
		btnSave.config(state="normal") if decodificado.decode() == str(passw.get()) else None
		btnBuscar.config(state="normal") if decodificado.decode() == str(passw.get()) else None


def savePassword(*args):
	"""
		Método en donde se inserta o modifica una contraseña en la BBDD en función del número de argumentos.
		Cero argumentos inserta una nueva contraseña en la BBDD
		Uno o más argumentos modifica la contraseña que le pasamos en la primera posición de los argumentos
			* args --> argumentos a pasar al metodo que pueden ser las variables que se crean oportunas
	"""
	try:
		global user, s, vSaveContrasenas
		if username.get() != '' and password.get() != '' and web.get() != '':
			clave = s.encrypt(str(password.get()))
			if len(args) == 0:
				cursor.execute("INSERT INTO contrasenas VALUES (null, '{}','{}','{}', {}, '{}')".format(web.get(), username.get(), clave.decode(), user.id, s.key.decode()))
				conexion.commit()
				cs = cursor.execute("SELECT * FROM contrasenas WHERE id_usuario = '{}'".format(user.id)).fetchall()
				decodificado = s.decrypt(clave)
				user.contrasenas.append(Contrasena(cs[-1][0], cs[-1][1], cs[-1][2], decodificado.decode()))
			else:
				#print(next((x for x in user.contrasenas if x.id == args[0].id), None))
				cursor.execute(f"UPDATE contrasenas SET web='{web.get()}', username='{username.get()}', password='{clave.decode()}', key='{s.key.decode()}' WHERE id='{args[0].id}' AND id_usuario='{user.id}'")
				conexion.commit()
				[user.contrasenas.remove(n) for n in user.contrasenas if n.id == args[0].id] #borro la contraseña de lista
				#print(next((x for x in user.contrasenas if x.id == args[0].id), None))
				cs = findOnePassword(args[0].id)
				decodificado = s.decrypt(cs.password.encode())
				cs.password = decodificado.decode()
				user.contrasenas.append(cs)
				createWidget(args[1])
			vSaveContrasenas.destroy() #cierro la ventana
			password.set("")
			username.set("")
			web.set("")
			check.set(-1)
		else:
			MessageBox.showinfo("Guardar contraseña","Debes rellenar los campos antes de poder guarda la contraseña")
	except sql.IntegrityError as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())
		MessageBox.showerror("Guardar contraseña","Ha ocurrido un error al guardar la contraseña")
	except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken) as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())
		MessageBox.showerror("Guardar contraseña","Ha ocurrido un error al guardar la contraseña")

def findAllPassword():
	"""
		Método que busca en la BBDD todas las contraseñas de un suario
	"""
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
		print(printExceptionMessage())
	except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken) as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())


def btnSaveContrasenas(*args):
	"""
		Método para crear la ventana en donde se van a poder guardar o modificar las contraseñas
		en función del número de argumentos
			* args --> argumentos a pasar al metodo que pueden ser las variables que se crean oportunas
	"""
	global vSaveContrasenas
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
	if len(args) == 0:
		Button(vSaveContrasenas, text="Guardar", command = savePassword).grid(row=5, column=1, columnspan=2)
	else:
		c = findOnePassword(check.get())
		if c != None:
			web.set(c.web)
			username.set(c.username)
			password.set(s.decrypt(c.password.encode()).decode())
			Button(vSaveContrasenas, text="Modificar", command = lambda: savePassword(c, args[0])).grid(row=5, column=1, columnspan=2)

def btnViewContrasenas():
	"""
		Método para inicializar y crear la ventana donde se van a mostrar tdas las contraseñas del usuario
	"""
	vContrasenas = Toplevel(root, padx=60, pady=10)
	vContrasenas.title("Contraseña")
	vContrasenas.resizable(0,0)
	createWidget(vContrasenas)

def createWidget(vContrasenas):
	"""
		Método para crear todos los widgets que va a tener la ventana donde van a mostrar las contraseás del suario.
			* vContrasenas -> objeto de la ventana donde se van a crear y mostrar todos los widgets
	"""
	try:
		miPass = StringVar()
		miUsername = StringVar()
		miWeb = StringVar()
		check.set(-1)
		index = 1

		lista = vContrasenas.grid_slaves()
		for l in lista: # Borro todos los widget de la ventana
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
		Button(vContrasenas, text = "Borrar selecionada", command=lambda: deletePassword(vContrasenas) if len(user.contrasenas) > 0 and int(check.get()) >-1 else None).grid(row=index+1, column=1, columnspan=2)
		Button(vContrasenas, text = "Modificar selecionada", command=lambda: btnSaveContrasenas(vContrasenas) if len(user.contrasenas) > 0 and int(check.get()) >-1 else None).grid(row=index+1, column=4, columnspan=2)
	except Exception as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())


def deletePassword(vContrasenas):
	"""
		Método para borrar una contraseña de la BBDD. Después se refresca la ventana donde se muestran las contraseñas
			* vContrasenas -> objeto de la ventana donde se van a crear y mostrar todos los widgets
	"""
	cursor.execute("DELETE FROM contrasenas WHERE id='{}'".format(check.get()))
	conexion.commit()
	first_or_default = next((n for n in user.contrasenas if n.id==check.get()), None)
	user.contrasenas.remove(first_or_default)
	#[print(n) for n in user.contrasenas]
	createWidget(vContrasenas)

def findOnePassword(id):
	"""
		Método para buscar una contraseña en la BBDD en función del id de la contraseña a buscar.
			* id -> clave primaria de la contraseña a buscar
			* return un objeto de tipo Contraseña
	"""
	try:
		result = cursor.execute("SELECT * FROM contrasenas WHERE id = '{}'".format(str(id))).fetchone()
		if result != None:
			c = Contrasena(result[0], result[1], result[2], result[3])
			s.key = result[-1]
			return c
	except sql.IntegrityError as ex:
		print(type(ex).__name__)
		print(printExceptionMessage())

def center_window (window,w=0, h=0):
	"""
		Método para centrar la ventana a la pantalla
			* w --> El ancho de la ventana, si no se le pasa nada, el ancho es 0
			* h --> El alto de la ventana, si no se le pasa nada, el alto es 0
	"""
	# get screen width and height
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()
	w = window.winfo_width() if w == 0 else w
	h = window.winfo_height() if h == 0 else h
	print(w)
	print(h)
	# calculate position x, y
	x = (ws/2) - (w/2)    
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def printExceptionMessage():
	"""
		Metodo para mostrar un mensaje de error según la excepción producida
			* return el mensaje a mostrar
	"""
	import sys, traceback
	exc_type, exc_value, exc_traceback = sys.exc_info()
	track = traceback.format_exception(exc_type, exc_value, exc_traceback)
	return traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

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