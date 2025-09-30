# main.py
# Validacion de estructuras de datos 
# Este archivo:
#  1) Verifica operaciones basicas y de borde (errores en estructuras vacias)
#  2) Validan que se preserva el orden cuando corresponde (Queue/Hash)
#  3) Estresan crecimiento/rehash (Queue y OrderedHashMap)
# Si una aserción falla, se lanzara AssertionError con un mensaje util.
# Al final se imprime un resumen para cada sección.

from stack import Stack
from queue import Queue
from hash import OrderedHashMap

def assert_equal(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg} | Esperado: {expected!r}, Obtenido: {actual!r}")

def assert_true(cond, msg=""):
    if not cond:
        raise AssertionError(f"{msg} | Se esperaba True.")

def assert_raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except Exception as e:
        if isinstance(e, exc_type):
            return
        raise AssertionError(f"Se esperaba excepcion {exc_type.__name__}, "
                             f"pero se lanzo {type(e).__name__}: {e}")
    raise AssertionError(f"Se esperaba excepcion {exc_type.__name__}, pero no se lanzo ninguna.")

# Test Stack
def test_stack_basico():
    # Valida LIFO
    # Push y pop respetan ultimo en entrar/primero en salir
    # Peek no remueve
    # Errores controlados en pila vacía
    
    s = Stack[int]()
    assert_true(s.is_empty(), "Stack debe iniciar vacio")
    s.push(10); s.push(20); s.push(30)
    assert_equal(s.size(), 3, "Stack.size tras 3 pushes")
    assert_equal(s.peek(), 30, "Stack.peek debe ver el tope")
    assert_equal(s.pop(), 30, "Stack.pop debe sacar el tope 30")
    assert_equal(s.pop(), 20, "Stack.pop siguiente debe ser 20")
    assert_equal(s.size(), 1, "Stack.size tras 2 pops")
    assert_equal(s.peek(), 10, "Stack.peek ahora debe ser 10")
    assert_equal(s.pop(), 10, "Ultimo pop debe regresar 10")
    assert_true(s.is_empty(), "Stack vacio despues de todos los pops")
    assert_raises(IndexError, s.pop)   # pop en vacio
    assert_raises(IndexError, s.peek)  # peek en vacio

def test_stack_clear():
    #Valida clear(), elimina todos los elementos
    s = Stack[str]()
    for ch in "ABCDE":
        s.push(ch)
    assert_equal(s.size(), 5)
    s.clear()
    assert_true(s.is_empty(), "clear() debe vaciar la pila")
    assert_raises(IndexError, s.pop)

# Test Queue
def test_queue_fifo_basico():
    # Valida FIFO con buffer circular:
    # enqueue/dequeue respetan primero en entrar/salir
    # front no remueve
    # errores controlados en cola vacia
    q = Queue[str]()
    assert_true(q.is_empty(), "Queue debe iniciar vacia")
    q.enqueue("A"); q.enqueue("B"); q.enqueue("C")
    assert_equal(q.size(), 3)
    assert_equal(q.front(), "A", "front debe ser 'A'")
    assert_equal(q.dequeue(), "A", "dequeue debe sacar 'A'")
    assert_equal(q.front(), "B", "front debe avanzar a 'B'")
    q.enqueue("D")
    assert_equal(q.to_list(), ["B", "C", "D"], "orden logico interno tras operaciones")
    assert_equal(q.dequeue(), "B")
    assert_equal(q.dequeue(), "C")
    assert_equal(q.dequeue(), "D")
    assert_true(q.is_empty(), "cola vacia tras extraer todo")
    assert_raises(IndexError, q.dequeue)  # dequeue en vacio
    assert_raises(IndexError, q.front)    # front en vacio

def test_queue_growth():
    """Estresa el crecimiento automático del buffer circular."""
    q = Queue[int](capacidad_inicial=1)
    N = 64
    for i in range(N):
        q.enqueue(i)
    assert_equal(q.size(), N, "tamaño tras crecer internamente")
    # Verificar orden
    for i in range(N):
        assert_equal(q.dequeue(), i, "FIFO debe preservarse durante/adapt. de capacidad")
    assert_true(q.is_empty(), "cola debe quedar vacia")


# Test HASH
def test_hash_orden_insercion_y_operaciones():
    # Valida OrderedHashMap:
    # Insercion preserva orden
    # get/set actualiza sin cambiar orden
    # delete remueve y re-conecta lista de orden
    # manejar valores None
    # KeyError en delete de clave inexistente

    m = OrderedHashMap[str, object]()
    m.set("uno", 1)
    m.set("dos", 2)
    m.set("tres", 3)
    assert_equal(list(m.items()), [("uno", 1), ("dos", 2), ("tres", 3)], "orden inicial")

    # Actualizacion no cambia orden
    m.set("dos", 22)
    assert_equal(list(m.items()), [("uno", 1), ("dos", 22), ("tres", 3)], "update mantiene orden")
    assert_equal(m.get("dos"), 22, "get despues de update")

    # Valor None y presencia en items
    m.set("nulo", None)
    assert_equal(list(m.items()), [("uno", 1), ("dos", 22), ("tres", 3), ("nulo", None)])

    # Borrado de cabeza
    m.delete("uno")
    assert_equal(list(m.items()), [("dos", 22), ("tres", 3), ("nulo", None)], "delete('uno')")

    # Borrado de inexistente lanza
    assert_raises(KeyError, m.delete, "no-existe")

def test_hash_rehash_y_conteo():
    # Inserta muchas entradas para forzar rehash y verifica que todo siga accesible y en orden de insercion.
    m = OrderedHashMap[int, int](capacidad_inicial=2, load_factor=0.75)
    N = 200
    for i in range(N):
        m.set(i, i * 10)
    # Checar algunos valores y orden parcial
    assert_equal(m.get(0), 0)
    assert_equal(m.get(50), 500)
    assert_equal(m.get(199), 1990)

    items = list(m.items())
    # Los primeros 5 deben ser (0,0), (1,10), etc.
    assert_equal(items[:5], [(0, 0), (1, 10), (2, 20), (3, 30), (4, 40)], "orden de insercion tras rehash")

    # Conteo por items (la clase no implementa __len__)
    assert_equal(len(items), N, "numero de pares clave-valor tras rehash")


# ---- Runner -----------------------------------------------------------------
def run_all():
    print("=== VALIDACION ===")
    print("Stack: LIFO, manejo de vacios, peek sin extraer, clear.")
    print("Queue: FIFO con buffer circular, crecimiento dinamico, manejo de vacios.")
    print("OrderedHashMap: orden de insercion, update sin alterar orden, delete, valores None, rehash.\n")

    # Stack
    test_stack_basico()
    test_stack_clear()
    print("Stack: todas las pruebas pasaron")

    # Queue
    test_queue_fifo_basico()
    test_queue_growth()
    print("Queue: todas las pruebas pasaron")

    # Hash
    test_hash_orden_insercion_y_operaciones()
    test_hash_rehash_y_conteo()
    print("OrderedHashMap: todas las pruebas pasaron")

    print("\n Todas las pruebas pasaron!")

if __name__ == "__main__":
    run_all()
