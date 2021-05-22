import socket
import tkinter as tk
from functools import partial
from tkinter import ttk
from client import main
from utils_client import createRequest
import json

def send_create_request_certif(name, password, ClientSocket, tkWindow):
    host = '127.0.0.1'
    port = 1233
    req = "Req|" + name + "|" + password
    ClientSocket.send(str.encode(req))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    if (Response.decode('utf-8') == "ClientAndCertified"):
        print("Nadiaaaa", name)
        main(host, port, name, tkWindow)

def popup_window_request_certif(title, message, button, name, password, ClientSocket):
    win = tk.Toplevel()
    win.wm_title(title)
    l = tk.Label(win, text=message)
    l.grid(row=0, column=0)
    sendCreateRequestCertif = partial(send_create_request_certif, name, password, ClientSocket, win)

    b = ttk.Button(win, text=button, command=sendCreateRequestCertif)
    b.grid(row=1, column=0)

    for i in range(0,2):
        win.rowconfigure(i, minsize=100, weight=1)
        win.columnconfigure(i, minsize=100, weight=1)




def popup_window(title, message, button):
    win = tk.Toplevel()
    win.wm_title(title)
    l = tk.Label(win, text=message)
    l.grid(row=0, column=0)

    b = ttk.Button(win, text=button, command=win.destroy)
    b.grid(row=1, column=0)

    for i in range(0,2):
        win.rowconfigure(i, minsize=100, weight=1)
        win.columnconfigure(i, minsize=100, weight=1)


def popup_window_create_request_for_certif(name, password, title, message, button, ClientSocket):
    win = tk.Toplevel()
    win.wm_title(title)
    l = tk.Label(win, text=message)
    l.grid(row=0, column=0)
    
    popupWindowRequestCertif = partial(popup_window_request_certif, "INSAT_Chat Notification", "Request is under treatment", "Okey!", name, password, ClientSocket)

    b = ttk.Button(win, text=button, command=popupWindowRequestCertif)
    b.grid(row=1, column=1)

    for i in range(0,2):
        win.rowconfigure(i, minsize=100, weight=1)
        win.columnconfigure(i, minsize=100, weight=1)


def clear_inputs(loginEntry, passwordEntry):
    loginEntry.delete(0, tk.END)
    passwordEntry.delete(0, tk.END)

def client_connect():

    ClientSocket = socket.socket()
    host = '127.0.0.1'
    port = 1233

    print('Waiting for connection')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    #Response = ClientSocket.recv(1024)
    

    def validateLogin(login, password, tkWindow):
        res = "Con|" + login.get() + "|" + password.get()
        print("signup ", res, str.encode(res))
        ClientSocket.send(str.encode(res))
        Response = ClientSocket.recv(1024)
        if (Response.decode('utf-8') == "ClientAndCertified"):
            tkWindow.destroy()
            main("127.0.0.1", 1060, login.get(), tkWindow)
        if (Response.decode('utf-8') == "NotClient"):
            print("No you are not a client")
            popup_window("INSAT_Chat Notification", "Check your credentials", "Got it!")
            clear_inputs(loginEntry, passwordEntry)
        if (Response.decode('utf-8') == "ClientAndNotCertified"):
            print("You are not certified or your certification has expired!")
            popup_window_create_request_for_certif(login.get(),password.get(),"INSAT_Chat Notification", "Certificate is needed if you want to join the INSAT_Chat", "Request Certificate!", ClientSocket)

  

        return
    #window
    tkWindow = tk.Tk()   
    tkWindow.title('Sign in INSAT_chat')
    WIDTH, HEIGTH = 400, 500
    tkWindow.geometry('{}x{}'.format(WIDTH, HEIGTH))

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

    validateLogin = partial(validateLogin, login, password, tkWindow)

    #login button
    loginButton = tk.Button(tkWindow, text="Sign in", command=validateLogin)
    loginButton.grid(row=3, column=1) 
    
    for i in range(0,4):
        tkWindow.rowconfigure(i, minsize=30, weight=1)
        tkWindow.columnconfigure(i, minsize=30, weight=1)

    tkWindow.mainloop()
    ClientSocket.close()
client_connect()