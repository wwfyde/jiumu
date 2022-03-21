import json

import websocket
import time
from threading import Thread

BYTE = {
    'LF': '\x0A',
    'NULL': '\x00'
}

VERSIONS = '1.0,1.1'


class Stomp:
    def __init__(self, host, sockjs=False, wss=True):
        """
        Initialize STOMP communication. This is the high level API that is exposed to clients.

        Args:
            host: Hostname
            sockjs: True if the STOMP server is sockjs
            wss: True if communication is over SSL
        """
        # websocket.enableTrace(True)
        ws_host = host if sockjs is False else host + "/websocket"
        protocol = "ws://" if wss is False else "wss://"

        self.url = protocol + ws_host

        self.dispatcher = Dispatcher(self)

        # maintain callback registry for subscriptions -> topic (str) vs callback (func)
        self.callback_registry = {}

    def connect(self):
        """
        Connect to the remote STOMP server
        """
        # set flag to false
        self.connected = False

        # attempt to connect
        self.dispatcher.connect()

        # wait until connected
        while self.connected is False:
            time.sleep(.50)

        return self.connected

    def subscribe(self, destination, callback):
        """
        Subscribe to a destination and supply a callback that should be executed
        when a message is received on that destination
        """
        # create entry in registry against destination
        self.callback_registry[destination] = callback
        self.dispatcher.subscribe(destination)

    def send(self, destination, message):
        """
        Send a message to a destination
        """
        self.dispatcher.send(destination, message)


def parse_frame(frame: str):

    if frame.strip():
        lines: list = frame.split(BYTE['LF'])

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
        command, headers, body = ['', {}, '']

    return command, headers, body


    pass

def parse_frame2(frame: str):

    if frame.strip():
        lines: list = frame.split(BYTE['LF'])

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
        command, headers, body = ['', {}, '']

    return command, headers, body


    pass


class Dispatcher:
    def __init__(self, stomp):
        """
        The Dispatcher handles all network I/O and frame marshalling/unmarshalling
        """
        self.stomp = stomp
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.stomp.url)

        # register websocket callbacks
        self.ws.on_open = self._on_open
        self.ws.on_message = self._on_message
        self.ws.on_error = self._on_error
        self.ws.on_close = self._on_close

        # run event loop on separate thread
        Thread(target=self.ws.run_forever).start()

        self.opened = False

        # wait until connected
        while self.opened is False:
            time.sleep(.50)

    def _get_frame(self, ):
        """

        :return:
        """

    def _on_message(self, ws, message):
        """
        Executed when messages is received on WS
        """
        print("<<< " + message)

        command, headers, body = self._parse_message(message)

        # if connected, let Stomp know
        if command == "CONNECTED":
            self.stomp.connected = True

        # if message received, call appropriate callback
        if command == "MESSAGE":
            self.stomp.callback_registry[headers['destination']](body)

    def _on_error(self, ws, error, exception):
        """
        Executed when WS connection errors out
        """
        print(error)

    def _on_close(self, ws, code, msg):
        """
        Executed when WS connection is closed
        """
        print("### closed ###")

    def _on_open(self, ws):
        """
        Executed when WS connection is opened
        """
        self.opened = True

    def _transmit(self, command: str, headers: dict, msg=None):
        """
        Marshalls and transmits the frame
        """
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
        self.ws.send(frame)

    def _parse_message(self, frame):
        """
        Returns:
            command
            headers
            body

        Args:
            frame: raw frame string
        """
        if frame.strip():
            lines = frame.split(BYTE['LF'])

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
            command, headers, body = ['', {}, '']

        return command, headers, body

    def connect(self):
        """
        Transmit a CONNECT frame
        """
        headers = {'host': self.stomp.url,
                   'accept-version': VERSIONS,
                   'heart-beat': '10000,10000'}

        self._transmit('CONNECT', headers)

    def subscribe(self, destination):
        """
        Transmit a SUBSCRIBE frame
        """
        headers = {'id': 'sub-1',
                   'ack': 'client',
                   'destination': destination}

        # TODO id should be auto generated

        self._transmit('SUBSCRIBE', headers)

    def send(self, destination, message):
        """
        Transmit a SEND frame
        """
        headers = {}

        headers['destination'] = destination
        headers['content-length'] = str(len(message))

        self._transmit('SEND', headers, msg=message)


if __name__ == '__main__':
    def on_speech_stream(msg):
        print("正在订阅")
        print("MESSAGE: " + msg)
        command, header, body = parse_frame(msg)

        if command == "MESSAGE":
            speech_stream: dict = json.loads(command)
            # TODO
        elif command == "CONNECTED":
            pass
        else:
            pass
    def subscribe_speech_stream():
        websocket.enableTrace(True)
        token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'
        # token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'
        agent = 9999
        stomp = Stomp(f"192.168.129.176:8186/hawkeye/rest/v1/stomp?userToken={token}", sockjs=False, wss=False)
        stomp.connect()
        print("连接成功")
        stomp.subscribe(f"/topic/result/{agent}", on_speech_stream)
    # ws = websocket.WebSocketApp()



