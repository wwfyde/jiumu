import sys
import time

import stomp


def connect_and_subscribe(conn):
    conn.connect('guest', 'guest', wait=True)
    conn.subscribe(destination='/queue/test', id=1, ack='auto')


class MyListener(stomp.ConnectionListener):
    def __init__(self, _conn):
        self._conn = _conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)


    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self._conn)


conn = stomp.Connection()
conn.set_listener('', MyListener(conn))
conn.connect('admin', 'password', wait=True)
conn.subscribe(destination='/queue/test', id='1', ack='auto')
# conn.send(body=' '.join(sys.argv[1:]), destination='/queue/test')
# time.sleep(2)
# conn.disconnect()

if __name__ == '__main__':

    print("run")