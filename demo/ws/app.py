import websocket


def on_message(wsapp, message):
    print(message)


wsapp = websocket.WebSocketApp("wss://testnet-explorer.binance.org/ws/block", on_message=on_message)
wsapp.run_forever()
