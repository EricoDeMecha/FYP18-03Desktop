import socket

from selectors import EVENT_READ, EVENT_WRITE
import proto_msg_pb2
from loop import Loop

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 1883))
s.listen(1)
s.setblocking(False)

loop = Loop()


def process_received_bytes(msg, data):
    #  get the length of the  first of message
    msg = msg[1:msg[0] + 1]  # override the  message with only the data
    reply = proto_msg_pb2.Reply()
    reply.ParseFromString(msg)
    try:
        data['temperature'].put(reply.temperature)
        data['weight'].put(reply.weight)
        data['time'].put(reply.time_interval)
    except KeyError:
        print('Key not found')
    # data['current_step'].put(reply.current_step)
    # print("\nReply Message")

    # print("Temperature: ", "{:.2f}".format(reply.temperature), "degrees celcius")
    # print("Weight: ", "{:.2f}kg".format(reply.weight))
    # print("Time Interval: ", "{:.2f}s".format(reply.time_interval))
    # print(f"Current Step: {reply.current_step}")


def generate_msg(data):
    command = proto_msg_pb2.Command()
    try:
        command.valve = data['valve'].get()
        command.diverter = data['diverter'].get()
        command.n_steps = data['steps'].get()
        command.t_steps = data['time'].get()
        command.start_btn = data['start'].get()
        command.reset_btn = data['stop'].get()
        command.next_btn = data['next'].get()
    except KeyError:
        print('Key not found')
    # command.valve = 20
    # command.diverter = True
    # command.n_steps = 0
    # command.t_steps = 0
    # command.start_btn = False
    # command.reset_btn = False
    # command.next_btn = False
    command_str = command.SerializeToString()
    return command_str


def handler(conn, data):
    while True:
        msg = yield from loop.recv(conn, 250)
        if not msg:
            conn.close()
            break
        # deal with received bytes
        process_received_bytes(msg, data)
        command_str = generate_msg(data)
        yield from loop.send(conn, command_str)


def test(data):
    while True:
        conn, addr = yield from loop.accept(s)
        conn.setblocking(False)
        loop.create_task((handler(conn, data), None))


def run(data):
    loop.create_task((test(data), None))
    loop.run()