
import string
try:
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import pyperclip as pc
except Exception as ex:
	print('----------instalando libreria-----------')
	print(type(ex).__name__)
	import pip
	pip.main(['install', 'tkintertable'])
	pip.main(['install', 'random'])
	pip.main(['install', 'pyperclip'])
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import pyperclip as pc


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

def copy():
	pass

root = Tk()
n_characters = IntVar()
characters = IntVar()
password = StringVar()
root.title("Generador de contraseñas")

root.resizable(0,0)
root.iconbitmap('keys.ico')
root.config(padx=15)

txtPass = Entry(root, textvariable=password)
txtPass.grid(row=1, column=1, columnspan=5, padx=15, pady=15)
txtPass.config(width=25, justify="center", state="readonly", font=("Arial",30, "bold", "italic"), borderwidth=5, highlightbackground ='gray22', highlightthickness=3)

Label(root, text="Longitud de la contraseña", font=("Arial",12, "bold", "underline")).grid(row=2, column=1, sticky="w")
Radiobutton(root, text="8 carácteres", variable=n_characters, value=8, state="active").grid(row=2, column=2)
Radiobutton(root, text="12 carácteres", variable=n_characters, value=12, state="active").grid(row=2, column=3)
Radiobutton(root, text="16 carácteres", variable=n_characters, value=16, state="active").grid(row=2, column=4)
Radiobutton(root, text="20 carácteres", variable=n_characters, value=20, state="active").grid(row=2, column=5)

Label(root, text="Carácteres", font=("Arial",12, "bold", "underline")).grid(row=3, column=1, sticky="w")
Radiobutton(root, text="Todos carácteres", variable=characters, value=1, state="active").grid(row=3, column=2)
Radiobutton(root, text="Solo letras", variable=characters, value=2, state="active").grid(row=3, column=3)
Radiobutton(root, text="Solo números", variable=characters, value=3, state="active").grid(row=3, column=4)
Radiobutton(root, text="Letras y números", variable=characters, value=4, state="active").grid(row=3, column=5)

imagen1 = PhotoImage(file="retry.gif")
Button(root, image=imagen1, height = 55, width = 50, command=lambda: retry(n_characters.get(), characters.get())).grid(row=1, column=6, sticky="w")
imagen2 = PhotoImage(file="copy.gif")
Button(root, image=imagen2, height = 55, width = 50, command=lambda: pc.copy(password.get())).grid(row=1, column=7, sticky="w")


root.mainloop()