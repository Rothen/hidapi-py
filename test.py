import sdl3
from sdl3 import SDL_GetJoysticks
sdl3.SDL_Init(sdl3.SDL_INIT_GAMEPAD)

if SDL_GetJoysticks(None):
    print("Joystick found")
else:
    print("No joystick found")

sdl3.SDL_Quit()
