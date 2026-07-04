"""
sjf.py
======

Politica Shortest Job First (SJF) NO expropiativa dentro de su propia cola.
Hereda de `SchedulingPolicy`.

  - select_next: elige el proceso con MENOR tiempo restante. Desempates:
        1) mayor prioridad interna, 2) orden alfabetico de la etiqueta,
        para que el resultado sea siempre determinista.
  - quantum_for: INFINITE -> una vez elegido corre hasta terminar; la unica
        forma de interrumpirlo es una expropiacion desde una cola de mayor
        prioridad, que gestiona el MLQScheduler.
  - requeue: reinserta el proceso (solo ocurre si fue expropiado); conserva su
        tiempo restante y volvera a competir por ser el mas corto.

Nota: como en este esquema SJF es la cola de MENOR prioridad, sus procesos
no expropian a nadie; el `quantum_expired` se mantiene por consistencia de la
interfaz.
"""

from scheduling_policy import SchedulingPolicy, INFINITE


class SJF(SchedulingPolicy):
    """Shortest Job First no expropiativo."""

    def __init__(self):
        super().__init__(name="SJF")

    def select_next(self, ready_list):
        if not ready_list:
            return None
        # menor remaining_time; empate -> mayor priority; empate -> label
        ready_list.sort(key=lambda p: (p.remaining_time, -p.priority, p.label))
        return ready_list.pop(0)

    def quantum_for(self, process):
        return INFINITE

    def requeue(self, ready_list, process, quantum_expired):
        ready_list.append(process)
