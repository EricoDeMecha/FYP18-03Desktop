import gui
import dataController
from threading import Thread
from queue import Queue


def main():
    data = {
        'temperature': Queue(),
        'weight': Queue(),
        'valve': Queue(),
        'steps': Queue(),
        'time': Queue(),
        'diverter': Queue(),
        'start': Queue(),
        'stop': Queue(),
        'next': Queue(),
        'current_step': Queue()
    }
    thread1 = Thread(target=gui.run, args=(data))
    thread2 = Thread(target=dataController.run, args=(data))
    thread1.start()
    thread2.daemon = True
    thread2.start()
