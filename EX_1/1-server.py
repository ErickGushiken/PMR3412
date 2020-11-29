# Aluno: Erick Gushiken
import socket
import selectors

sel = selectors.DefaultSelector()
def accept(sock, mask):
    conn, addr = sock.accept()
    print('CONECTADO com o cliente', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, response)
    #Comando programado 'dir'
    conn.sendall(b'dir')

def response(conn, mask):
    data = conn.recv(1024)
    if data:
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
while True:
  events = sel.select()
  for key, mask in events:
    callback = key.data
    callback(key.fileobj, mask)