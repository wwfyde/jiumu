import uuid

import websocket
from threading import Thread
import time
import sys

BYTE = {
    'LF': '\x0A',
    'NULL': '\x00'
}


def on_message(ws, message: str):
    print("接收到消息>>>")

    if message.strip():
        print(f"解析消息: {message}")
        # TODO 解析消息


    else:
        print(f"接收到的消息为空: {message}")

    print(message)


def on_error(ws, error):
    print(f"出现错误, 错误提示: {error}")
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def get_frame():
    agent = 9999
    command = 'SUBSCRIBE'
    topic = f"/topic/result/{agent}"

    msg = None
    headers = {'id': 'sub-1',
               'ack': 'client',
               'destination': topic}

    # Contruct the frame
    lines = [command + BYTE['LF']]

    # add headers
    for key in headers:
        lines.append(key + ":" + headers[key] + BYTE['LF'])

    lines.append(BYTE['LF'])

    # add message, if any
    if msg is not None:
        lines.append(msg)

    # terminate with null octet
    lines.append(BYTE['NULL'])

    frame = ''.join(lines)

    # transmit over ws
    print(">>>" + frame)
    return frame


def on_open(ws: websocket.WebSocketApp):
    agent = 9999
    topic = f"/topic/result/{agent}"
    data = f"SUBSCRIBE\nid:{str(uuid.uuid1())}\nack:client\ndestination:{topic}\n" \
           f"content-length:{len(topic)}\n\n\x00"
    host = f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}"

    # frame = get_frame()
    connect = f"CONNECT\nhost:{host}" \
              f"\naccept-version:1.0,1.1\nheart-beat:10000,10000\n\n\x00"
    # TODO 需要等待连接成功时才发送
    time.sleep(2)
    ws.send(connect)
    # ws.send(frame)
    ws.send(data)

    # def run(*args):
    #
    #     ws.close()
    #     print("Thread terminating...")
    #
    # Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    # if len(sys.argv) < 2:
    #     host = "ws://echo.websocket.events/"
    # else:
    #     host = sys.argv[1]
    token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'
    host = f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}"
    connected = False
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close, on_open=on_open)

    # ws.on_open = on_open
    print("永久执行")
    ws.run_forever()
