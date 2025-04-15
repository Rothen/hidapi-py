from typing import TypeVar, Generic, Final, Callable, TypeAlias

from reactivex import Subject
from reactivex.abc import DisposableBase

T = TypeVar("T")

ChangeCallable: TypeAlias = Callable[[T], None]
ButtonPressedCallable: TypeAlias = Callable[[], None]
ButtonReleasedCallable: TypeAlias = Callable[[], None]


class ReadableValue(Generic[T]):
    """A class to represent a readable value from the DualSense controller."""
    __slots__ = ("_change", "_value")

    def __init__(self, init_value: T):
        """Initialize the ReadableValue with a name and value.

        Args:
            name (str): The name of the readable value.
            value (T): The value of the readable value.
        """
        self._change: Final[Subject[T]] = Subject[T]()
        self._value: T = init_value
    
    def set_value(self, value: T) -> None:
        """Set the value of the ReadableValue and notify subscribers.

        Args:
            value (T): The new value to set.
        """
        self._value = value
        self._change.on_next(value)
    
    def _subscribe(self, callback: ChangeCallable[T]) -> DisposableBase:
        """Subscribe to changes in the value.

        Args:
            callback (ChangeCallable): The function to call when the value changes.
        """
        return self._change.subscribe(callback)


class ButtonValue(ReadableValue[bool]):
    """A class to represent a readable value from the DualSense controller."""
    __slots__ = (
        "pressed_subject",
        "released_subject"
    )

    def __init__(self):
        """Initialize the ReadableValue with a name and value.

        Args:
            name (str): The name of the readable value.
            value (T): The value of the readable value.
        """
        super().__init__(False)
        self.pressed_subject: Final[Subject[bool]] = Subject[bool]()
        self.released_subject: Final[Subject[bool]] = Subject[bool]()

    def set_value(self, value: bool) -> None:
        super().set_value(value)
        if value:
            self.pressed_subject.on_next(value)
        else:
            self.released_subject.on_next(value)
    
    def pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        """Subscribe to pressed events."""
        return self.pressed_subject.subscribe(lambda _: callback())

    def released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        """Subscribe to pressed events."""
        return self.released_subject.subscribe(lambda _: callback())
