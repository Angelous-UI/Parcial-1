"""
scheduling_policy.py
====================

Clase abstracta `SchedulingPolicy`. Equivale a la interfaz abstracta
`SchedulingPolicy` de la documentacion (seccion 3): permite intercambiar
algoritmos (Round Robin / SJF) de forma polimorfica dentro de cada cola.

Cada politica concreta debe responder tres preguntas sobre la lista de
procesos listos de SU cola:
    1. select_next(ready_list) -> que proceso despachar a continuacion.
    2. quantum_for(process)     -> cuanto tiempo (a lo sumo) dejarlo correr.
    3. requeue(...)             -> como reinsertarlo si no termino.

La lista de listos (ready_list) la administra la clase `Queue`; la politica
solo decide sobre ella.
"""

from abc import ABC, abstractmethod

# Rodaja "infinita": politicas que corren hasta completar (SJF no expropiativo).
INFINITE = float("inf")


class SchedulingPolicy(ABC):
    """Interfaz abstracta para la politica de planificacion de una cola."""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def select_next(self, ready_list):
        """
        Elige y RETIRA de `ready_list` el proximo proceso a ejecutar.
        Devuelve el `Process` seleccionado (o None si la lista esta vacia).
        """
        raise NotImplementedError

    @abstractmethod
    def quantum_for(self, process):
        """Rodaja de tiempo maxima para `process` (INFINITE si corre hasta acabar)."""
        raise NotImplementedError

    @abstractmethod
    def requeue(self, ready_list, process, quantum_expired):
        """
        Reinserta en `ready_list` un proceso que corrio pero no termino.

        quantum_expired=True  -> agoto su rodaja de forma natural (RR).
        quantum_expired=False -> fue EXPROPIADO por una cola de mayor prioridad.
        """
        raise NotImplementedError
