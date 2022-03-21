import time

import websocket

BYTE = {
    'LF': '\x0A',
    'NULL': '\x00'
}


def on_message(wsapp, message):
    print(message)

def on_close(wsapp):
    print("连接已经关闭")


if __name__ == '__main__':
    token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'
    url = f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}"
    # ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close)
    ws = websocket.WebSocket()
    # ws.connect(f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}")
    # ws.connect(f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}")
    connect_frame = msg = f"CONNECT{BYTE['LF']}host:{url}{BYTE['LF']}heart-beat:10000,10000{BYTE['LF']}" \
                          f"accept-version:1.0,1.1{BYTE['LF']}{BYTE['LF']}{BYTE['NULL']}"
    ws.connect(url, )
    # ws = websocket.WebSocketApp(f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}",
    #                              on_message=on_message)
    print("连接成功")
    # ws.send("SUBSCRIBE")
    # TODO 构造 frame
    frame = ''
    agent = 9999
    destination = f"/topic/result/{agent}"
    # header
    msg = f"SUBSCRIBE{BYTE['LF']}id:sub-2{BYTE['LF']}ack:client{BYTE['LF']}destination:{destination}{BYTE['LF']}" \
          f"content-length:{len(destination)}{BYTE['LF']}{BYTE['LF']}{BYTE['NULL']}"
    print(f">>>\n{msg}")
    msg = f"VERSION"
    ws.send(msg)
    while True:
        data: str = ws.recv()
        print(data, 'hello')

        if not data.strip():
            ws.close()
            break
    # ws.run_forever()


    #
    # while True:
    #     print("Received")
    #     result = ws.recv_frame()
    #     print(f"Received: {result}")
    #
    # # ws.recv()
    # # print(ws.recv())
    # ws.close()
    # for item in ws.recv():
    #     print(item)
    # r = ws.recv()
    # print(r)
    # while True:
    #     print('receiveing')
    #     r = ws.recv()
    #     print(r)
    #     time.sleep(1)
    # print(ws.recv())
    # ws.close()
