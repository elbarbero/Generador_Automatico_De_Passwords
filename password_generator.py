
try:
	from tkinter import *
	from tkinter import messagebox as MessageBox
	import random
	import string
except:
	print('----------instalando libreria-----------')
	import pip
	pip.main(['install', 'tkintertable'])
	pip.main(['install', 'random'])
	from tkinter import *
	from tkinter import messagebox as MessageBox
	from random import *


def generatePassword(size):
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(size))

def retry(size):
	txtPass.configure(state='normal')
	txtPass.delete(0,END)
	txtPass.insert(0,generatePassword(size))
	txtPass.configure(state='readonly')


root = Tk()
option = IntVar()
root.title("Generador de contraseñas")

root.resizable(0,0)
root.iconbitmap('keys.ico')
root.config(padx=15)

"""txtPass = Entry(root, width=20, justify="center", state="normal", font=("Arial",30, "bold", "underline"), borderwidth=5, highlightbackground ='gray22', highlightthickness=3)
txtPass.pack(padx=15, pady=15,side="left")

option = IntVar()

Radiobutton(root, text="8", variable=option, value=1).pack()
Radiobutton(root, text="12", variable=option, value=2).pack()
Radiobutton(root, text="16", variable=option, value=3).pack()
Radiobutton(root, text="20", variable=option, value=4).pack()

frame = Frame(root)
frame.pack(side="left")
imagen1 = PhotoImage(file="retry.gif")
Button(frame, image=imagen1, height = 55, width = 50, command=lambda: retry(8)).pack(side="left")
imagen2 = PhotoImage(file="copy.gif")
Button(frame, image=imagen2, height = 55, width = 50).pack(side="left")"""



txtPass = Entry(root)
txtPass.grid(row=1, column=1, columnspan=5, padx=15, pady=15)
txtPass.config(width=25, justify="center", state="readonly", font=("Arial",30, "bold", "italic"), borderwidth=5, highlightbackground ='gray22', highlightthickness=3)

Label(root, text="Longitud de la contraseña", font=("Arial",12, "bold", "underline")).grid(row=2, column=1, sticky="w")
Radiobutton(root, text="8 caracteres", variable=option, value=8, state="active").grid(row=2, column=2)
Radiobutton(root, text="12 caracteres", variable=option, value=12, state="active").grid(row=2, column=3)
Radiobutton(root, text="16 caracteres", variable=option, value=16, state="active").grid(row=2, column=4)
Radiobutton(root, text="20 caracteres", variable=option, value=20, state="active").grid(row=2, column=5)

imagen1 = PhotoImage(file="retry.gif")
Button(root, image=imagen1, height = 55, width = 50, command=lambda: retry(option.get())).grid(row=1, column=6, sticky="w")
imagen2 = PhotoImage(file="copy.gif")
Button(root, image=imagen2, height = 55, width = 50).grid(row=1, column=7, sticky="w")



root.mainloop()