import websockets

class WebSocketUserInterface:
    def __init__(self, websocket_url):
        self.websocket_url = websocket_url
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.websocket_url)

    async def send_message(self, message):
        if self.connection is None or self.connection.closed:
            await self.connect()
        await self.connection.send(message)

    async def receive_message(self):
        if self.connection is None or self.connection.closed:
            await self.connect()
        return await self.connection.recv()

    async def close_connection(self):
        if self.connection and not self.connection.closed:
            await self.connection.close()
