from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

class Loop(object):
    def __init__(self):
        self.sel = DefaultSelector()
        self.queue = []

    def create_task(self, task):
        self.queue.append(task)

    def polling(self):
        for e, m in self.sel.select(0):
            self.queue.append((e.data, None))
            self.sel.unregister(e.fileobj)

    def is_registered(self, fileobj):
        try:
            self.sel.get_key(fileobj)
        except KeyError:
            return False
        return True

    def register(self, t, data):
        if not data:
            return False

        if data[0] == EVENT_READ:
            if self.is_registered(data[1]):
                self.sel.modify(data[1], EVENT_READ, t)
            else:
                self.sel.register(data[1], EVENT_READ, t)
        elif data[0] == EVENT_WRITE:
            if self.is_registered(data[1]):
                self.sel.modify(data[1], EVENT_WRITE, t)
            else:
                self.sel.register(data[1], EVENT_WRITE, t)
        else:
            return False

        return True

    def accept(self, s):
        conn, addr = None, None
        while True:
            try:
                conn, addr = s.accept()
            except BlockingIOError:
                yield (EVENT_READ, s)
            else:
                break
        return conn, addr

    def recv(self, conn, size):
        msg = None
        while True:
            try:
                msg = conn.recv(size)
            except BlockingIOError:
                yield (EVENT_READ, conn)
            else:
                break
        return msg

    def send(self, conn, msg):
        size = 0
        while True:
            try:
                size = conn.send(msg)
            except BlockingIOError:
                yield (EVENT_WRITE, conn)
            else:
                break
        return size

    def once(self):
        self.polling()
        unfinished = []
        for t, data in self.queue:
            try:
                data = t.send(data)
            except StopIteration:
                continue

            if self.register(t, data):
                unfinished.append((t, None))

        self.queue = unfinished

    def run(self):
        while self.queue or self.sel.get_map():
            self.once()