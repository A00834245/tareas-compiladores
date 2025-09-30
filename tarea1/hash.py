# Hash con orden de insercion

from typing import Generic, Iterator, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class _Node(Generic[K, V]):
    def __init__(self, key: K, value: V, h: int) -> None:
        self.key = key
        self.value = value
        self.h = h
        self.next: Optional["_Node[K, V]"] = None
        self.prev_order: Optional["_Node[K, V]"] = None
        self.next_order: Optional["_Node[K, V]"] = None

class OrderedHashMap(Generic[K, V]):
 
    def __init__(self, capacidad_inicial: int = 8, load_factor: float = 0.75) -> None:
        cap = 1
        while cap < capacidad_inicial:
            cap <<= 1
        self._buckets: List[Optional[_Node[K, V]]] = [None] * cap
        self._size = 0
        self._load_factor = load_factor
        self._head: Optional[_Node[K, V]] = None
        self._tail: Optional[_Node[K, V]] = None

    def _cap(self) -> int:
        return len(self._buckets)

    def _index(self, h: int) -> int:
        return h & (self._cap() - 1)

    def _rehash(self) -> None:
        old = self._buckets
        new_cap = len(old) * 2
        self._buckets = [None] * new_cap
        n = self._head
        while n is not None:
            idx = self._index(n.h)
            n.next = self._buckets[idx]
            self._buckets[idx] = n
            n = n.next_order

    def set(self, key: K, value: V) -> None:
        h = hash(key)
        idx = self._index(h)
        node = self._buckets[idx]
        while node is not None:
            if node.h == h and node.key == key:
                node.value = value
                return
            node = node.next
        new_node = _Node(key, value, h)
        new_node.next = self._buckets[idx]
        self._buckets[idx] = new_node
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            new_node.prev_order = self._tail
            self._tail.next_order = new_node
            self._tail = new_node
        self._size += 1
        if self._size / self._cap() > self._load_factor:
            self._rehash()

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        h = hash(key)
        idx = self._index(h)
        node = self._buckets[idx]
        while node is not None:
            if node.h == h and node.key == key:
                return node.value
            node = node.next
        return default

    def delete(self, key: K) -> None:
        h = hash(key)
        idx = self._index(h)
        prev: Optional[_Node[K, V]] = None
        node = self._buckets[idx]
        while node is not None:
            if node.h == h and node.key == key:
                if prev is None:
                    self._buckets[idx] = node.next
                else:
                    prev.next = node.next
                if node.prev_order is not None:
                    node.prev_order.next_order = node.next_order
                else:
                    self._head = node.next_order
                if node.next_order is not None:
                    node.next_order.prev_order = node.prev_order
                else:
                    self._tail = node.prev_order
                self._size -= 1
                return
            prev, node = node, node.next
        raise KeyError(key)

    def items(self) -> Iterator[Tuple[K, V]]:
        n = self._head
        while n is not None:
            yield (n.key, n.value)
            n = n.next_order

    def __repr__(self) -> str:
        contenido = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"OrderedHashMap({{{contenido}}})"
