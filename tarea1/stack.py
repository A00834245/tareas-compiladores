# Stack (pila LIFO)
from typing import List, TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):

    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, x: T) -> None:
        self._data.append(x)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop desde pila vacia")
        return self._data.pop()

    def peek(self) -> T:
        if not self._data:
            raise IndexError("peek en pila vacia")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def size(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        self._data.clear()

    def to_list(self) -> List[T]:
        return list(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"
