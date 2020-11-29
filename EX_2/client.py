#Nome: Erick Jooji Gushiken
#NUSP: 10333421
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            message = cliente.recv(1024).decode("utf8")
            message_list.insert(tkinter.END, message)
        except OSError:
            #no caso dos erros de clientes que sairam da lista tem um break
            break


def send(event=None):
    message = my_message.get()
    my_message.set("")
    cliente.send(bytes(message, "utf8"))
    if message == "*quit":
        cliente.close()
        top.quit()


def fechar(event=None):
    my_message.set("*quit")
    send()

#código de layout
top = tkinter.Tk()
top.title("CHAT DO PMR3412 - REDES INDUSTRIAIS")

messages_frame = tkinter.Frame(top)
my_message = tkinter.StringVar()
my_message.set("Digite sua mensagem aqui")
scrollbar = tkinter.Scrollbar(messages_frame) 
message_list = tkinter.Listbox(messages_frame, height=20, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Enviar", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", fechar)

#Código do socket
print("*********SEJA BEM VINDO, INDIQUE AS INFORMAÇÔES DE CONEXÂO***********")
HOST = input('Entre host: ')
PORT = input('Entre porta: ')
if not PORT:
    PORT = 35000
else:
    PORT = int(PORT)

ADDR = (HOST, PORT)

cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect(ADDR)

thread_cliente = Thread(target=receive)
thread_cliente.start()

tkinter.mainloop()
