import gui
import dataController
from concurrent.futures import ThreadPoolExecutor


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
    executor = ThreadPoolExecutor(max_workers=2)
    thread1 = executor.submit(gui.run, data)
    thread2 = executor.submit(dataController.run, data)


if __name__ == '__main__':
    main()
