# Queue (cola FIFO)
from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")

class Queue(Generic[T]):

    def __init__(self, capacidad_inicial: int = 8) -> None:
        if capacidad_inicial < 1:
            capacidad_inicial = 1
        cap = 1
        while cap < capacidad_inicial:
            cap <<= 1
        self._buf: List[Optional[T]] = [None] * cap
        self._head = 0
        self._tail = 0
        self._size = 0

    def _cap(self) -> int:
        return len(self._buf)

    def _mask(self) -> int:
        return self._cap() - 1

    def _grow(self) -> None:
        old = self._buf
        n = self._cap()
        new = [None] * (n * 2)
        for i in range(self._size):
            new[i] = old[(self._head + i) & (n - 1)]
        self._buf = new
        self._head = 0
        self._tail = self._size

    def enqueue(self, x: T) -> None:
        if self._size == self._cap():
            self._grow()
        self._buf[self._tail] = x
        self._tail = (self._tail + 1) & self._mask()
        self._size += 1

    def dequeue(self) -> T:
        if self._size == 0:
            raise IndexError("dequeue desde cola vacia")
        x = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) & self._mask()
        self._size -= 1
        return x

    def front(self) -> T:
        if self._size == 0:
            raise IndexError("front en cola vacia")
        return self._buf[self._head]  

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def clear(self) -> None:
        self._buf = [None] * self._cap()
        self._head = self._tail = self._size = 0

    def to_list(self) -> List[T]:
        return [self._buf[(self._head + i) & self._mask()] for i in range(self._size)]  # type: ignore

    def __repr__(self) -> str:
        return f"Queue({self.to_list()!r})"
