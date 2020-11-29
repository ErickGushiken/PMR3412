# Aluno: Erick Gushiken
# Atualizado em 25/11/2020
import asyncio
import websockets
import json

clients={}




async def receive_message(websocket, path):
    # Determina qual o tipo de dado que vem do socket para definir a função a ser chamada
  async for msg in websocket:
    message = json.loads(msg)
    if message['type'] == 'create_name':
      if not clients.get(message['user'].lower()):
        # Se não existe o usuário na lista, cria um novo usuário, sempre com letra minuscula
        clients [message['user'].lower()] = [websocket, message['userId']]
        await new_user(message['user'], message['userId'])
        await listUsers()
      else:
        await already_exist(websocket, message['user'], message['userId'])
    if message['type'] == 'message':
        #Tipo de mensagem de texto a ser enviada
      if message['message'][0:4] == "*pvt":
        #indicativo *pvt mostra que a mensagem é privada
        user = message['message'][4:].split('@')[0].lower()
        await send_private(user, message)
      elif clients.get(message['user']):
        # Caso contrário manda para todos
        await broadcast_message(msg)
    if message['type'] == 'welcome':
        message['type'] = 'message'
        message['message']="Bem Vindo, utilize o campo ao lado para cadastro de usuário"
        await websocket.send(json.dumps(message))

async def send_private(user,message):
  global clients
  if clients.get(user):
    client = clients.get(user)[0]
    msg = message['message'][4:].split('@')[1]
    message['message'] = "".join(msg)
    print(message,"mensagem")
    try:
      await client.send(json.dumps(message))
    except:
      clients.pop(user)
      await listUsers()

async def broadcast_message(message):
  global clients
  disconnectedUsers = []
  for user in clients.keys():
    client = clients.get(user)[0]
    try:
      await client.send(message)
    except:
      disconnectedUsers.append(user)

  for user in disconnectedUsers:
    clients.pop(user)
  if len(disconnectedUsers) > 0:
    await listUsers()

async def already_exist(websocket, username,userId):
  reject_message = json.dumps({
    'type': 'user_exist',
    'user':username,
    'message':'Nome já existente',
    'userId':userId}
  )
  await websocket.send(reject_message)

async def new_user(username,userId):
  accept_message = json.dumps({
    'type': 'new_user',
    'user':username,
    'message':'Novo usuário criado com sucesso',
    'userId':userId}
  )
  await broadcast_message(accept_message)

async def listUsers():
  users = []
  for key in clients.keys():
    users.append(key)
  users_message = json.dumps({
    'type': 'users',
    'message': users
  })
  print("Broadcasting:", users_message)
  await broadcast_message(users_message)


start_server = websockets.serve(receive_message, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
