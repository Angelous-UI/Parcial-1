"""
process.py
==========

Clase `Process`: contenedor de los datos de un proceso individual y de sus
metricas calculadas. Equivale a la clase `Process` de la arquitectura descrita
en la documentacion (seccion 3).

Atributos de entrada (leidos del archivo):
    label        -> etiqueta / identificador del proceso (ej. "A", "p1")
    burst_time   -> BT, tiempo total de CPU que necesita
    arrival_time -> AT, instante en que llega al sistema
    queue_id     -> Q, numero de cola a la que pertenece (1, 2 o 3)
    priority     -> prioridad interna (5 = alta ... 1 = baja)

Estado de simulacion:
    remaining_time -> tiempo de CPU que aun le falta (arranca igual a BT)
    start_time     -> primer instante en que toca la CPU (para el RT)

Metricas finales (se calculan como propiedades a partir de completion_time y
start_time, para que nunca queden desincronizadas):
    completion_time (CT), waiting_time (WT), response_time (RT),
    turnaround_time (TAT)
"""


class Process:
    """Representa un unico proceso a planificar y sus metricas."""

    def __init__(self, label, burst_time, arrival_time, queue_id, priority):
        # --- Datos de entrada ---
        self.label = str(label)
        self.burst_time = int(burst_time)
        self.arrival_time = int(arrival_time)
        self.queue_id = int(queue_id)
        self.priority = int(priority)

        # --- Estado interno de la simulacion ---
        self.remaining_time = int(burst_time)
        self.start_time = None       # se fija la 1a vez que usa CPU
        self.completion_time = None  # se fija al terminar

    # ------------------------------------------------------------------
    # Metricas derivadas (validas una vez el proceso arranco/termino)
    # ------------------------------------------------------------------
    @property
    def response_time(self):
        """RT = primer instante en CPU - llegada."""
        return self.start_time - self.arrival_time

    @property
    def turnaround_time(self):
        """TAT = finalizacion - llegada."""
        return self.completion_time - self.arrival_time

    @property
    def waiting_time(self):
        """WT = TAT - BT."""
        return self.turnaround_time - self.burst_time

    # ------------------------------------------------------------------
    def is_finished(self):
        """True cuando ya no le queda tiempo de CPU."""
        return self.remaining_time <= 0

    def __repr__(self):
        return (f"Process({self.label}, BT={self.burst_time}, "
                f"AT={self.arrival_time}, Q={self.queue_id}, "
                f"Pr={self.priority}, rem={self.remaining_time})")
