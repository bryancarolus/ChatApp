from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

HOST = '127.0.0.1'
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)


# Handles receiving of messages
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


# Handles sending of messages
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


# Closing window
def on_closing(event=None):
    my_msg.set("{quit}")
    send()


# GUI
top = tkinter.Tk()
top.title("Chat App")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type here")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=25, width=75, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width=55)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send, bg='#151B54', fg='white')
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
