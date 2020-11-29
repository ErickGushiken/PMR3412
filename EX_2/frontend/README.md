# Websockets Echo Frontend

Este é apenas o frontend para o servidor echo Websocket basedo na biblioteca `websockets` do Python.
O código do servidor é:

```python
#!/usr/bin/env python

import asyncio
import websockets


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

Execute o servidor com o Python antes de iniciar o servidor de desenvolvimento do frontend

## Iniciando o servidor de desenvolvimento do frontend

Primeiro, é necessário instalar as depêndencias do Node.js

```bash
cd echoserver_frontend
npm install
```

Depois, para executar o servidor

```bash
npm run dev
```

Com isso, abra o *browser* em [localhost:5000](http://localhost:5000). Você deve observar a sua aplicação em execução. Ao editar um arquivo de componenente em `src` e salvá-lo, você deverá ser capaz de ver suas mudanças na página.

Por padrão, o servidor vai responder apenas por requisições no localhost. Para habilitar conexões de outros computadores, edite os comandos `sirv` no package.json para incluir a opção `--host 0.0.0.0`.

Se você está usando [Visual Studio Code](https://code.visualstudio.com/), é recomendado a instalação da extensão oficial [Svelte for VS Code](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode). 