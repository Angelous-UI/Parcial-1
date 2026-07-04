"""
main.py
=======

Punto de entrada del simulador MLQ. Orquesta: parsear -> simular -> escribir.

Uso:
    python src/main.py <archivo_entrada> [archivo_salida]

Ejemplos:
    python src/main.py inputs/mlq001.txt
        -> genera outputs/mlq001_out.txt

    python src/main.py inputs/mlq001.txt outputs/resultado.txt

Si no se indica <archivo_salida>, se genera en la carpeta outputs/ con el
sufijo "_out" (ej: mlq001.txt -> outputs/mlq001_out.txt).

Esquema de colas EXIGIDO (de mayor a menor prioridad):
    Cola 1 -> Round Robin, quantum = 1   (RR(1))
    Cola 2 -> Round Robin, quantum = 3   (RR(3))
    Cola 3 -> SJF no expropiativo        (SJF)
"""

import os
import sys

from file_parser import FileParser
from mlq_scheduler import MLQScheduler
from queue import Queue
from report_writer import ReportWriter
from round_robin import RoundRobin
from sjf import SJF


def build_scheduler():
    """Construye el MLQScheduler con el esquema RR(1) / RR(3) / SJF."""
    queues = {
        1: Queue(queue_id=1, policy=RoundRobin(quantum=1)),  # maxima prioridad
        2: Queue(queue_id=2, policy=RoundRobin(quantum=3)),
        3: Queue(queue_id=3, policy=SJF()),                  # minima prioridad
    }
    return MLQScheduler(queues)


def default_output_path(input_path):
    """inputs/mlq001.txt -> outputs/mlq001_out.txt"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(project_root, "outputs", f"{base}_out.txt")


def main(argv):
    if len(argv) < 2:
        print("Uso: python src/main.py <archivo_entrada> [archivo_salida]")
        return 1

    input_path = argv[1]
    output_path = argv[2] if len(argv) >= 3 else default_output_path(input_path)

    try:
        processes = FileParser.parse(input_path)
        scheduler = build_scheduler()
        scheduler.run(processes)
        averages = scheduler.calculate_metrics(processes)
        ReportWriter.write_results(output_path, processes, averages)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"Simulacion completada. Salida: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
