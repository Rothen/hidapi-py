from typing import Final

from reactivex.abc import DisposableBase

from .readable_value import ButtonValue, ButtonPressedCallable, ButtonReleasedCallable

class DualSenseController:
    __slots__ = (
        "_square",
        "_cross",
        "_circle",
        "_triangle",
        "_dpad_up",
        "_dpad_right",
        "_dpad_down",
        "_dpad_left",
        "_l1",
        "_r1",
        "_l2",
        "_r2",
        "_share",
        "_options",
        "_l3",
        "_r3",
        "_ps",
        "_touch",
        "_mikrophone",
    )

    def __init__(self):
        self._square: Final[ButtonValue] = ButtonValue()
        self._cross: Final[ButtonValue] = ButtonValue()
        self._circle: Final[ButtonValue] = ButtonValue()
        self._triangle: Final[ButtonValue] = ButtonValue()
        self._dpad_up: Final[ButtonValue] = ButtonValue()
        self._dpad_right: Final[ButtonValue] = ButtonValue()
        self._dpad_down: Final[ButtonValue] = ButtonValue()
        self._dpad_left: Final[ButtonValue] = ButtonValue()
        self._l1: Final[ButtonValue] = ButtonValue()
        self._r1: Final[ButtonValue] = ButtonValue()
        self._l2: Final[ButtonValue] = ButtonValue()
        self._r2: Final[ButtonValue] = ButtonValue()
        self._share: Final[ButtonValue] = ButtonValue()
        self._options: Final[ButtonValue] = ButtonValue()
        self._l3: Final[ButtonValue] = ButtonValue()
        self._r3: Final[ButtonValue] = ButtonValue()
        self._ps: Final[ButtonValue] = ButtonValue()
        self._touch: Final[ButtonValue] = ButtonValue()
        self._mikrophone: Final[ButtonValue] = ButtonValue()
        
    def press_square(self) -> None:
        self._square.set_value(True)

    def release_square(self) -> None:
        self._square.set_value(False)

    def press_cross(self) -> None:
        self._cross.set_value(True)

    def release_cross(self) -> None:
        self._cross.set_value(False)

    def press_circle(self) -> None:
        self._circle.set_value(True)

    def release_circle(self) -> None:
        self._circle.set_value(False)

    def press_triangle(self) -> None:
        self._triangle.set_value(True)

    def release_triangle(self) -> None:
        self._triangle.set_value(False)

    def press_dpad_up(self) -> None:
        self._dpad_up.set_value(True)

    def release_dpad_up(self) -> None:
        self._dpad_up.set_value(False)

    def press_dpad_right(self) -> None:
        self._dpad_right.set_value(True)

    def release_dpad_right(self) -> None:
        self._dpad_right.set_value(False)

    def press_dpad_down(self) -> None:
        self._dpad_down.set_value(True)

    def release_dpad_down(self) -> None:
        self._dpad_down.set_value(False)

    def press_dpad_left(self) -> None:
        self._dpad_left.set_value(True)

    def release_dpad_left(self) -> None:
        self._dpad_left.set_value(False)

    def press_l1(self) -> None:
        self._l1.set_value(True)

    def release_l1(self) -> None:
        self._l1.set_value(False)

    def press_r1(self) -> None:
        self._r1.set_value(True)

    def release_r1(self) -> None:
        self._r1.set_value(False)

    def press_l2(self) -> None:
        self._l2.set_value(True)

    def release_l2(self) -> None:
        self._l2.set_value(False)

    def press_r2(self) -> None:
        self._r2.set_value(True)

    def release_r2(self) -> None:
        self._r2.set_value(False)

    def press_share(self) -> None:
        self._share.set_value(True)

    def release_share(self) -> None:
        self._share.set_value(False)

    def press_options(self) -> None:
        self._options.set_value(True)

    def release_options(self) -> None:
        self._options.set_value(False)

    def press_l3(self) -> None:
        self._l3.set_value(True)

    def release_l3(self) -> None:
        self._l3.set_value(False)

    def press_r3(self) -> None:
        self._r3.set_value(True)

    def release_r3(self) -> None:
        self._r3.set_value(False)

    def press_ps(self) -> None:
        self._ps.set_value(True)

    def release_ps(self) -> None:
        self._ps.set_value(False)

    def press_touch(self) -> None:
        self._touch.set_value(True)

    def release_touch(self) -> None:
        self._touch.set_value(False)

    def press_mikrophone(self) -> None:
        self._mikrophone.set_value(True)

    def release_mikrophone(self) -> None:
        self._mikrophone.set_value(False)

    def square_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._square.pressed(callback)

    def cross_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._cross.pressed(callback)

    def circle_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._circle.pressed(callback)

    def triangle_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._triangle.pressed(callback)

    def dpad_up_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_up.pressed(callback)

    def dpad_right_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_right.pressed(callback)

    def dpad_down_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_down.pressed(callback)

    def dpad_left_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_left.pressed(callback)

    def l1_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._l1.pressed(callback)

    def r1_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._r1.pressed(callback)

    def l2_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._l2.pressed(callback)

    def r2_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._r2.pressed(callback)

    def share_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._share.pressed(callback)

    def options_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._options.pressed(callback)

    def l3_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._l3.pressed(callback)

    def r3_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._r3.pressed(callback)

    def ps_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._ps.pressed(callback)

    def touch_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._touch.pressed(callback)

    def mikrophone_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._mikrophone.pressed(callback)

    def square_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._square.released(callback)

    def cross_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._cross.released(callback)

    def circle_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._circle.released(callback)

    def triangle_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._triangle.released(callback)

    def dpad_up_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_up.released(callback)

    def dpad_right_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_right.released(callback)

    def dpad_down_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_down.released(callback)

    def dpad_left_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_left.released(callback)

    def l1_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._l1.released(callback)

    def r1_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._r1.released(callback)

    def l2_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._l2.released(callback)

    def r2_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._r2.released(callback)

    def share_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._share.released(callback)

    def options_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._options.released(callback)

    def l3_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._l3.released(callback)

    def r3_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._r3.released(callback)

    def ps_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._ps.released(callback)

    def touch_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._touch.released(callback)

    def mikrophone_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._mikrophone.released(callback)
