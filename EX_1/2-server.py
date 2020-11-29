# Aluno: Erick Gushiken
import socket
import selectors
import threading

command = "dir"
def change_command():
  global command
  new_command = input("Digite o novo comando: ")
  if len(new_command)>0:
    print("Novo comando:", new_command)
    command = new_command
  return change_command()

inputThread = threading.Thread(target=change_command)
inputThread.daemon = True

sel = selectors.DefaultSelector()
def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('Cliente conectado', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    conn.sendall(str.encode(command))

def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
      print("OLA")
      print(repr(data))
    else:
      sel.unregister(conn)
      conn.close()

HOST = ''
PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

def run_server():
  while True:
    events = sel.select()
    for key, mask in events:
      callback = key.data
      callback(key.fileobj, mask)

serverThread = threading.Thread(target=run_server)
serverThread.start()
inputThread.start()