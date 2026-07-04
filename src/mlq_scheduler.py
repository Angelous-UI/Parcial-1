"""
mlq_scheduler.py
================

Clase `MLQScheduler`: orquesta la simulacion completa. Equivale a la clase
`MLQScheduler` de la documentacion (seccion 3).

Politica de despacho ENTRE colas (decision de diseno, seccion 2.2 del doc):
PRIORIDAD ESTRICTA CON EXPROPIACION.
  - La cola de menor numero (mayor prioridad) se ejecuta siempre que tenga
    procesos listos.
  - Si mientras corre un proceso de una cola inferior llega un proceso a una
    cola de mayor prioridad, el proceso en ejecucion es EXPROPIADO: vuelve a su
    cola conservando su tiempo restante y el recien llegado toma la CPU.
  - Dentro de cada cola, el orden lo decide su propia politica (RR o SJF).

Modelo de simulacion dirigido por eventos:
  En cada iteracion:
    1. Se admiten las llegadas cuyo AT <= tiempo actual.
    2. Se elige la cola no vacia de mayor prioridad (la "cola activa").
    3. Se pide a su politica el proximo proceso y su quantum.
    4. La rodaja real = min(quantum, tiempo restante, tiempo hasta la proxima
       llegada a una cola de MAYOR prioridad).
    5. Se ejecuta esa rodaja, se actualiza el reloj y el remaining_time, y se
       registra start_time la primera vez que el proceso usa CPU.
    6. Si termina, se fija completion_time; si no, se reencola.

Se salta de evento en evento (no "tic a tic"): es eficiente y exacto.
"""

from queue import Queue


class MLQScheduler:
    """Planificador multinivel con prioridad estricta y expropiacion entre colas."""

    def __init__(self, queues):
        """
        queues: dict {queue_id: Queue}. Numero de cola MENOR = mayor prioridad.
        """
        if not queues:
            raise ValueError("Debe proporcionar al menos una cola.")
        self.queues = queues
        self.priority_order = sorted(queues.keys())  # colas mas prioritarias primero

    # ------------------------------------------------------------------
    def run(self, processes):
        """
        Ejecuta la simulacion sobre `processes` y devuelve la misma lista con
        completion_time / start_time calculados.
        """
        self._validate(processes)

        # Pendientes por llegar, ordenados por instante de llegada (desempates
        # estables: AT, cola, prioridad desc, label).
        pending = sorted(
            processes,
            key=lambda p: (p.arrival_time, p.queue_id, -p.priority, p.label),
        )

        current_time = max(0, pending[0].arrival_time) if pending else 0
        completed = []
        total = len(processes)

        self._admit_arrivals(pending, current_time)

        while len(completed) < total:
            active_id = self._highest_priority_ready_queue()

            # Ninguna cola lista: saltar al proximo arribo (CPU ociosa).
            if active_id is None:
                if not pending:
                    break
                current_time = pending[0].arrival_time
                self._admit_arrivals(pending, current_time)
                continue

            queue = self.queues[active_id]
            proc = queue.select_next()

            # Response Time: primera vez que el proceso toca la CPU.
            if proc.start_time is None:
                proc.start_time = current_time

            quantum = queue.quantum_for(proc)
            run_time = min(quantum, proc.remaining_time)
            slice_end = current_time + run_time

            # Punto de expropiacion: llegada a una cola de MAYOR prioridad.
            preempt_time = self._next_preemption_time(pending, active_id, slice_end)

            if preempt_time is not None:
                actual_run = preempt_time - current_time
                proc.remaining_time -= actual_run
                current_time = preempt_time
                self._admit_arrivals(pending, current_time)

                if proc.is_finished():
                    proc.completion_time = current_time
                    completed.append(proc)
                else:
                    queue.requeue(proc, quantum_expired=False)
            else:
                proc.remaining_time -= run_time
                current_time = slice_end
                self._admit_arrivals(pending, current_time)

                if proc.is_finished():
                    proc.completion_time = current_time
                    completed.append(proc)
                else:
                    queue.requeue(proc, quantum_expired=True)

        return processes

    # ------------------------------------------------------------------
    def calculate_metrics(self, processes):
        """
        Devuelve un dict con los promedios de WT, CT, RT y TAT sobre todos los
        procesos (todas las metricas individuales ya viven en cada Process).
        """
        n = len(processes)
        return {
            "WT": sum(p.waiting_time for p in processes) / n,
            "CT": sum(p.completion_time for p in processes) / n,
            "RT": sum(p.response_time for p in processes) / n,
            "TAT": sum(p.turnaround_time for p in processes) / n,
        }

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------
    def _admit_arrivals(self, pending, time):
        """Mueve de `pending` a su cola todo proceso con AT <= time."""
        while pending and pending[0].arrival_time <= time:
            proc = pending.pop(0)
            if proc.queue_id not in self.queues:
                raise ValueError(
                    f"El proceso {proc.label} referencia la cola {proc.queue_id}, "
                    f"no definida en el esquema."
                )
            self.queues[proc.queue_id].admit(proc)

    def _highest_priority_ready_queue(self):
        """Numero de la cola no vacia de mayor prioridad, o None."""
        for qid in self.priority_order:
            if not self.queues[qid].is_empty():
                return qid
        return None

    def _next_preemption_time(self, pending, active_id, slice_end):
        """
        Menor instante de llegada (estrictamente antes de slice_end) de un
        proceso destinado a una cola de MAYOR prioridad que `active_id`.
        None si no habra expropiacion durante esta rodaja.
        """
        candidates = [
            p.arrival_time
            for p in pending
            if p.queue_id < active_id and p.arrival_time < slice_end
        ]
        return min(candidates) if candidates else None

    @staticmethod
    def _validate(processes):
        if not processes:
            raise ValueError("No hay procesos para planificar.")
        labels = [p.label for p in processes]
        if len(labels) != len(set(labels)):
            raise ValueError("Hay etiquetas de proceso duplicadas.")
        for p in processes:
            if p.burst_time <= 0:
                raise ValueError(f"El proceso {p.label} tiene BT <= 0.")
            if p.arrival_time < 0:
                raise ValueError(f"El proceso {p.label} tiene AT negativo.")
