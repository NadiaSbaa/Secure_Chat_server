import socket
import tkinter as tk
from functools import partial
from tkinter import ttk

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)

def popup_window(title, type, message, button):
    win = tk.Toplevel()
    win.wm_title(title)

    l = tk.Label(win, text=type)
    l.grid(row=0, column=0)

    l = tk.Label(win, text=message)
    l.grid(row=1, column=1)

    b = ttk.Button(win, text=button, command=win.destroy)
    b.grid(row=2, column=1)

    for i in range(0,3):
        win.rowconfigure(i, minsize=50, weight=1)
        win.columnconfigure(i, minsize=50, weight=1)

def clear_inputs(carteidEntry, firstnameEntry, lastnameEntry, loginEntry, passwordEntry):
    carteidEntry.delete(0, tk.END)
    firstnameEntry.delete(0, tk.END)
    lastnameEntry.delete(0, tk.END)
    loginEntry.delete(0, tk.END)
    passwordEntry.delete(0, tk.END)

def signup(carteid, firstname, lastname, login, password):
    res = "Ins|" + carteid.get() + "|" + firstname.get() + "|" + lastname.get() + "|" + login.get() + "|" + password.get()
    ClientSocket.send(str.encode(res))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    popup_window("Save Certificate", "Generated Certicate :", Response.decode('utf-8'), "Saved")
    clear_inputs(carteidEntry, firstnameEntry, lastnameEntry, loginEntry, passwordEntry)
    return
#window
tkWindow = tk.Tk()
tkWindow.title('Sign up INSAT_chat')

#(N°carte, Nom, Prénom, Pseudo = Login, Pwd (qui devrait être haché (sha256))) et une demande de certification. 
#username label
carteidLabel = tk.Label(tkWindow, text="Card Number")
carteidLabel.grid(row = 0, column = 0)
#text entry box
carteid = tk.StringVar()
carteidEntry = tk.Entry(tkWindow, textvariable=carteid) 
carteidEntry.grid(row = 0, column = 1)

#firstname label
firstnameLabel = tk.Label(tkWindow, text="First Name")
firstnameLabel.grid(row = 1, column = 0)
#text entry box
firstname = tk.StringVar()
firstnameEntry = tk.Entry(tkWindow, textvariable=firstname) 
firstnameEntry.grid(row = 1, column = 1)

#lastname label
lastnameLabel = tk.Label(tkWindow, text="Last Name")
lastnameLabel.grid(row = 2, column = 0)
#text entry box
lastname = tk.StringVar()
lastnameEntry = tk.Entry(tkWindow, textvariable=lastname) 
lastnameEntry.grid(row = 2, column = 1)

#login label
loginLabel = tk.Label(tkWindow, text="Login")
loginLabel.grid(row = 3, column = 0)
#text entry box
login = tk.StringVar()
loginEntry = tk.Entry(tkWindow, textvariable=login) 
loginEntry.grid(row = 3, column = 1)

#password label 
passwordLabel = tk.Label(tkWindow,text="Password")
passwordLabel.grid(row=4, column=0)  
#password entry box
password = tk.StringVar()
passwordEntry = tk.Entry(tkWindow, textvariable=password, show='*')
passwordEntry.grid(row=4, column=1)  

signup = partial(signup, carteid, firstname, lastname, login, password)

#login button
loginButton = tk.Button(tkWindow, text="Certification Request", command=signup)
loginButton.grid(row=5, column=1) 

for i in range(0,6):
    tkWindow.rowconfigure(i, minsize=50, weight=1)
    tkWindow.columnconfigure(i, minsize=50, weight=1)

tkWindow.mainloop()


ClientSocket.close()