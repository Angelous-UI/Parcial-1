"""
round_robin.py
==============

Politica Round Robin (RR): cola FIFO con rodaja de tiempo fija (`quantum`).
Hereda de `SchedulingPolicy`.

  - select_next: toma el proceso del FRENTE (el que mas lleva esperando).
  - quantum_for: devuelve el quantum configurado.
  - requeue:
        * si agoto su quantum  -> vuelve al FINAL de la cola (RR clasico).
        * si fue expropiado     -> vuelve al FRENTE, para reanudar en cuanto
          la CPU quede libre de procesos de mayor prioridad (decision de
          diseno documentada en el informe).
"""

from scheduling_policy import SchedulingPolicy


class RoundRobin(SchedulingPolicy):
    """Round Robin con quantum fijo."""

    def __init__(self, quantum):
        super().__init__(name=f"RR({quantum})")
        if quantum <= 0:
            raise ValueError("El quantum de Round Robin debe ser > 0.")
        self.quantum = int(quantum)

    def select_next(self, ready_list):
        if not ready_list:
            return None
        return ready_list.pop(0)  # FIFO

    def quantum_for(self, process):
        return self.quantum

    def requeue(self, ready_list, process, quantum_expired):
        if quantum_expired:
            ready_list.append(process)      # al final
        else:
            ready_list.insert(0, process)   # expropiado: al frente
