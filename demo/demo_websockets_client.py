#!/usr/bin/env python

import asyncio
import websockets


def hello():
    token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'

    uri = f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}"
    websocket = websockets.connect(uri)
    # name = input("What's your name? ")
    frame = ''
    agent = 9999
    destination = f"/topic/result/{agent}"
    # header
    msg = f"""SUBSCRIBE\nid:sub-1\nack:client\ndestination:{destination}\ncontent-length:{len(destination)}\n\n
            """
    websocket.send(msg)
    print(f">>> {msg}")

    greeting = websocket.recv()
    print(f"<<< {greeting}")


if __name__ == "__main__":
    # asyncio.run(hello())
    hello()
