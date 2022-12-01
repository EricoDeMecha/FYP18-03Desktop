import gui
import dataController
from threading import Thread



def main():
    data = {
        'valve': 0,
        'diverter': False,
        'n_steps': 0,
        't_steps': 0,
        'start_btn': False,
        'reset_btn': False,
        'next_btn': False, #  Command ends here
        'temperature': 0.0,
        'weight': 0.0,
        'time_interval': 0,
        'current_step': 0
    }
    thread1 = Thread(target=gui.run, args=(data,))
    thread2 = Thread(target=dataController.run, args=(data,))
    thread1.start()
    thread2.daemon = True
    thread2.start()

if __name__ == '__main__':
    main()
