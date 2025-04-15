import time
from sdl3 import *

class Gamepad:
    def __init__(self):
        SDL_Init(SDL_INIT_GAMEPAD)
        self.axis = {}
        self.button = {}

    def update(self):
        event: SDL_Event = SDL_Event()
        while SDL_PollEvent(event) != 0:
            if event.type == SDL_EVENT_GAMEPAD_ADDED:
                print(event.gdevice.which)
                self.device = SDL_OpenGamepad(event.gdevice.which)
                print(SDL_GetGamepadTypeForID(event.gdevice.which), SDL_GAMEPAD_TYPE_PS5)
            elif event.type == SDL_EVENT_GAMEPAD_AXIS_MOTION:
                self.axis[event.gaxis.axis] = event.gaxis.value
            elif event.type == SDL_EVENT_GAMEPAD_BUTTON_DOWN:
                self.button[event.gbutton.button] = True
            elif event.type == SDL_EVENT_GAMEPAD_BUTTON_UP:
                self.button[event.gbutton.button] = False
            elif event.type == SDL_EVENT_GAMEPAD_TOUCHPAD_MOTION:
                pass # print(event.gtouchpad.finger, event.gtouchpad.x, event.gtouchpad.y)


if __name__ == "__main__":
    gamepad = Gamepad()
    while True:
        start = time.perf_counter()
        gamepad.update()
        time.sleep(0.01)
        # print((time.perf_counter() - start) * 1000)
        # print(joystick.axis)
        # print(gamepad.button)
