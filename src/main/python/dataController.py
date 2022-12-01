import socket

from selectors import EVENT_READ, EVENT_WRITE
import proto_msg_pb2
from loop import Loop

class DataController():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("", 1883))
        self.s.listen(1)
        self.s.setblocking(False)

        self.loop = Loop()

        self.data = {}

    def process_received_bytes(self, msg):
        #  get the length of the  first of message
        msg = msg[1:msg[0] + 1]  # override the  message with only the data
        reply = proto_msg_pb2.Reply()
        reply.ParseFromString(msg)
        try:
            self.data['temperature'] = reply.temperature
            self.data['weight'] = reply.weight
            self.data['time_interval'] = reply.time_interval
        except KeyError:
            print('Key not found')


    def generate_msg(self):
        command = proto_msg_pb2.Command()
        try:
            command.valve = self.data['valve']
            command.diverter = self.data['diverter']
            command.n_steps = self.data['n_steps']
            command.t_steps = self.data['t_steps']
            command.start_btn = self.data['start_btn']
            command.reset_btn = self.data['reset_btn']
            command.next_btn = self.data['next_btn']
        except KeyError:
            print('Key not found')
        command_str = command.SerializeToString()
        return command_str


    def handler(self, conn):
        while True:
            msg = yield from self.loop.recv(conn, 250)
            if not msg:
                conn.close()
                break
            # deal with received bytes
            self.process_received_bytes(msg)
            command_str = self.generate_msg()
            yield from self.loop.send(conn, command_str)


    def test(self):
        while True:
            conn, addr = yield from self.loop.accept(self.s)
            conn.setblocking(False)
            self.loop.create_task((self.handler(conn), None))


def run(data):
    dataController = DataController()
    dataController.data = data
    dataController.loop.create_task((dataController.test(), None))
    dataController.loop.run()