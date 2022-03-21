import websocket

ws = websocket.WebSocket()
ws.connect("ws://echo.websocket.events")
ws.send("Hello, Server")
print(ws.recv())
ws.close()