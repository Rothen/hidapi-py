import signal
import time
from typing import Any
from threading import Event

from py.hidapi_py_dualsense import DualSenseController, get_all_dual_sense_controllers

exit_event = Event()

def signal_handler(sig: int, frame: Any, controller: DualSenseController) -> None:
    """Handles Ctrl+C to stop the session gracefully."""
    print("\nCtrl+C detected! Stopping controller...")
    controller.close()
    exit_event.set()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, controller))

    controller = get_all_dual_sense_controllers()[0]
    controller.open()
    controller.cross_pressed(lambda: print("Cross pressed!", controller.loop_time))
    controller.cross_released(lambda: print("Cross released!"))

    while not exit_event.is_set():
        time.sleep(0.1)
