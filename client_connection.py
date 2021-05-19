import socket
import tkinter as tk
from functools import partial
from client import main

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)

def validateLogin(login, password,certificate):
    res = "Con|" + login.get() + "|" + password.get() + "|" + certificate.get() 
    ClientSocket.send(str.encode(res))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    if (Response.decode('utf-8') == "Yes"):
        main(host, port)
    return
#window
tkWindow = tk.Tk()   
tkWindow.title('Sign in INSAT_chat')

#username label
loginLabel = tk.Label(tkWindow, text="Login")
loginLabel.grid(row = 0, column = 0)
#text entry box
login = tk.StringVar()
loginEntry = tk.Entry(tkWindow, textvariable=login) 
loginEntry.grid(row = 0, column = 1)

#password label 
passwordLabel = tk.Label(tkWindow,text="Password")
passwordLabel.grid(row=1, column=0)  
#password entry box
password = tk.StringVar()
passwordEntry = tk.Entry(tkWindow, textvariable=password, show='*')
passwordEntry.grid(row=1, column=1)  

#certificate label 
certificateLabel = tk.Label(tkWindow,text="Certificate")
certificateLabel.grid(row=2, column=0)  
#certificate entry box
certificate = tk.StringVar()
certificateEntry = tk.Entry(tkWindow, textvariable=certificate)
certificateEntry.grid(row=2, column=1) 

validateLogin = partial(validateLogin, login, password, certificate)

#login button
loginButton = tk.Button(tkWindow, text="Sign in", command=validateLogin)
loginButton.grid(row=3, column=1) 
 
for i in range(0,4):
    tkWindow.rowconfigure(i, minsize=50, weight=1)
    tkWindow.columnconfigure(i, minsize=50, weight=1)


tkWindow.mainloop()


ClientSocket.close()