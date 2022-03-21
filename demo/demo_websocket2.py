import json
import time
from threading import Thread

import websocket

BYTE = {
    'LF': '\x0A',
    'NULL': '\x00'
}


def print_frame(frame):
    print(json.loads(frame.body))



class NewApp:
    def __init__(self, url, topic):
        """
        The Dispatcher handles all network I/O and frame marshalling/unmarshalling
        """
        self.url = url
        self.topic = topic

        self.ws = websocket.WebSocketApp(self.url)

        # register websocket callbacks
        self.ws.on_open = self._on_open
        self.ws.on_message = self._on_message
        self.ws.on_error = self._on_error
        # TODO 不实现
        self.ws.on_close = self._on_close

        # run event loop on separate thread
        Thread(target=self.ws.run_forever).start()
        self.connected = False

        self.opened = False

        # wait until connected
        while self.opened is False:
            time.sleep(.50)

    def _on_message(self, ws, message):
        """
        Executed when messages is received on WS
        """
        print("<<< " + message)
        print("接收到消息")

        command, headers, body = self._parse_message(message)
        print(body)
        print(headers)
        print(command)

        # if connected, let Stomp know
        if command == "CONNECTED":
            print("连接成功")
            self.connected = True

        # if message received, call appropriate callback
        if command == "MESSAGE":
            print("收到消息 receive message")
            # TODO 接收到消息时, 处理接收到的数据
            # self.stomp.callback_registry[headers['destination']](body)
        if command == "ERROR":
            self.connect()
        if not command:
            print("解析到空消息, 不做任何事情")

    def _on_error(self, ws, error, *args):
        """
        Executed when WS connection errors out
        """
        print(f"出现错误, 额外参数{args}")
        self.connect()
        print(f"错误提示: {error}")

    def _on_close(self, ws, code, msg):
        """
        Executed when WS connection is closed
        """
        print(f"### closed ### 额外参数{code}")

    def _on_open(self, ws):
        """
        Executed when WS connection is opened
        """
        self.opened = True

    def _transmit(self, command, headers, msg=None):
        """
        Marshalls and transmits the frame
        """
        # Contruct the frame
        print("传送指令")

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
        self.ws.send(frame)

    def _parse_message(self, frame: str):
        """
        Returns:
            command
            headers
            body

        Args:
            frame: raw frame string
        """
        print(f"内容解析: {frame}")
        lines = frame.split(BYTE['LF'])
        print('解析完毕')

        if frame.strip():
            command = lines[0].strip()
            headers = {}

            # get all headers
            i = 1
            while lines[i] != '':
                # get key, value from raw header
                (key, value) = lines[i].split(':')
                headers[key] = value
                i += 1

            # set body to None if there is no body
            body = None if lines[i + 1] == BYTE['NULL'] else lines[i + 1]
        else:
            print("解析到的信息为空")
            command, headers, body = ['', '', '']

        return command, headers, body

    def connect(self):
        """
        Transmit a CONNECT frame
        """
        self.connected = False
        headers = {}

        headers['host'] = self.url
        headers['accept-version'] = '1.0,1.1'
        headers['heart-beat'] = '10000,10000'

        self._transmit('CONNECT', headers)

        while self.connected is False:
            time.sleep(.50)

        return self.connected

    def subscribe(self, destination):
        """
        Transmit a SUBSCRIBE frame
        """
        headers = {}

        # TODO id should be auto generated
        headers['id'] = 'sub-1'
        headers['ack'] = 'client'
        headers['destination'] = destination

        self._transmit('SUBSCRIBE', headers)

    def send(self, message):
        """
        Transmit a SEND frame
        """
        self.ws.send(message)


def on_message(wsapp, message):
    print("接收到消息:")
    print(message)

def on_close(wsapp):
    print("连接已经关闭")


if __name__ == '__main__':
    token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'
    urls = f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}"
    # ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close)
    agent = 9999
    destination = f"/topic/result/{agent}"

    ws = NewApp(urls, destination)
    # ws.connect(f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}")
    # ws.connect(f"ws://192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}")
    connect_frame = msg = f"CONNECT{BYTE['LF']}host:{urls}{BYTE['LF']}heart-beat:10000,10000{BYTE['LF']}" \
                          f"accept-version:1.0,1.1{BYTE['LF']}{BYTE['LF']}{BYTE['NULL']}"
    ws.connect()
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
    # msg = f"VERSION"
    # ws.send(msg)
    ws.send(msg)
    # while True:
    #     data: str = ws.recv()
    #     print(data, 'hello')
    #
    #     if not data.strip():
    #         ws.close()
    #         break
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
