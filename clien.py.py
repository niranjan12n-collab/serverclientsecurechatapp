import socket
import threading
import tkinter as tk
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 4100

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

root = tk.Tk()
root.withdraw()

username = simpledialog.askstring("Username", "Enter username")

chat = tk.Toplevel(root)
chat.title("Chat Client")

chat_box = tk.Text(chat)
chat_box.pack()

msg = tk.Entry(chat)
msg.pack()


def receive():

    while True:
        try:
            message = client.recv(1024).decode()

            if message == "USERNAME":
                client.send(username.encode())
            else:
                chat_box.insert(tk.END, message + "\n")
        except:
            break


def send_message(event=None):

    message = msg.get()

    client.send(f"{username}: {message}".encode())

    msg.delete(0, tk.END)


msg.bind("<Return>", send_message)

thread = threading.Thread(target=receive)
thread.start()

root.mainloop()