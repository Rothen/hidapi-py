import signal
import time
from typing import Any
from threading import Event

from sdl3 import SDL_Init, SDL_INIT_GAMEPAD, SDL_Gamepad

from py.hidapi_py_dualsense import DualSenseController
from py.hidapi_py_dualsense.backends import SDL3Backend

exit_event = Event()

def signal_handler(sig: int, frame: Any, controller: DualSenseController) -> None:
    """Handles Ctrl+C to stop the session gracefully."""
    print("\nCtrl+C detected! Stopping controller...")
    controller.close()
    exit_event.set()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, controller))

    # Backend = HidAPIBackend
    SDL_Init(SDL_INIT_GAMEPAD)
    Backend = SDL3Backend
    
    device = Backend.get_available_devices()[0]
    controller = DualSenseController(Backend(device))
    controller.open()
    controller.square_pressed(lambda: print("Square"))
    controller.cross_pressed(lambda: print("Cross"))
    controller.circle_pressed(lambda: print("Circle"))
    controller.triangle_pressed(lambda: print("Triangle"))
    controller.dpad_up_pressed(lambda: print("Up"))
    controller.dpad_right_pressed(lambda: print("Right"))
    controller.dpad_down_pressed(lambda: print("Down"))
    controller.dpad_left_pressed(lambda: print("Left"))
    controller.l1_pressed(lambda: print("L1"))
    controller.r1_pressed(lambda: print("R1"))
    controller.l2_pressed(lambda: print("L2"))
    controller.r2_pressed(lambda: print("R2"))
    controller.share_pressed(lambda: print("Share"))
    controller.options_pressed(lambda: print("Options"))
    controller.l3_pressed(lambda: print("L3"))
    controller.r3_pressed(lambda: print("R3"))
    controller.ps_pressed(lambda: print("PS"))
    controller.touch_pressed(lambda: print("Touch"))
    controller.mikrophone_pressed(lambda: print("Mikrophone"))
    # controller.left_joy_stick_changed(lambda joy_stick: print("Left Joystick", joy_stick))
    # controller.right_joy_stick_changed(lambda joy_stick: print("Right Joystick", joy_stick))
    # controller.l2_trigger_changed(lambda value: print("L2 Grad", value))
    # controller.r2_trigger_changed(lambda value: print("R2 Grad", value))
    # controller.orientation_changed(lambda orientation: print(orientation))

    while not exit_event.is_set():
        time.sleep(0.1)
