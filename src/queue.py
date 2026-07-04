"""
queue.py
========

Clase `Queue`: agrupa una lista de procesos listos (`ready_list`) junto con la
politica de planificacion (`policy`) que le corresponde segun el esquema
elegido. Equivale a la clase `Queue` de la documentacion (seccion 3).

Un numero de cola MENOR significa MAYOR prioridad relativa entre colas
(la arbitracion entre colas la hace el MLQScheduler, no esta clase).
"""


class Queue:
    """Una cola del sistema MLQ con su propia politica."""

    def __init__(self, queue_id, policy):
        self.queue_id = int(queue_id)      # 1, 2, 3 ...
        self.priority_level = int(queue_id)  # menor numero = mayor prioridad
        self.policy = policy               # instancia de SchedulingPolicy
        self.ready_list = []               # procesos listos en esta cola

    # --- Gestion de la lista de listos ---
    def admit(self, process):
        """Registra un proceso que acaba de llegar a esta cola."""
        self.ready_list.append(process)

    def is_empty(self):
        return len(self.ready_list) == 0

    def pending_labels(self):
        """Utilidad de depuracion."""
        return [p.label for p in self.ready_list]

    # --- Delegacion en la politica ---
    def select_next(self):
        """Pide a la politica el proximo proceso de esta cola."""
        return self.policy.select_next(self.ready_list)

    def quantum_for(self, process):
        return self.policy.quantum_for(process)

    def requeue(self, process, quantum_expired):
        self.policy.requeue(self.ready_list, process, quantum_expired)

    def __repr__(self):
        return f"Queue(id={self.queue_id}, policy={self.policy.name}, ready={self.pending_labels()})"
