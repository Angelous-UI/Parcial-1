"""
run_all.py
==========

Utilidad: ejecuta el simulador sobre TODOS los archivos de la carpeta inputs/
y genera sus salidas en outputs/. Comodo para validar de una sola vez.

Uso (desde la carpeta mlq-scheduler/):
    python run_all.py
"""

import glob
import os
import sys

# Permitir importar los modulos de src/
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from main import build_scheduler          # noqa: E402
from file_parser import FileParser        # noqa: E402
from report_writer import ReportWriter    # noqa: E402


def main():
    inputs = sorted(glob.glob(os.path.join(ROOT, "inputs", "*.txt")))
    if not inputs:
        print("No se encontraron archivos en inputs/")
        return 1

    for path in inputs:
        base = os.path.splitext(os.path.basename(path))[0]
        out = os.path.join(ROOT, "outputs", f"{base}_out.txt")
        try:
            processes = FileParser.parse(path)
            scheduler = build_scheduler()
            scheduler.run(processes)
            averages = scheduler.calculate_metrics(processes)
            ReportWriter.write_results(out, processes, averages)
            print(f"[OK] {base}: WT={averages['WT']:.2f}  "
                  f"CT={averages['CT']:.2f}  RT={averages['RT']:.2f}  "
                  f"TAT={averages['TAT']:.2f}")
        except (FileNotFoundError, ValueError) as exc:
            print(f"[ERROR] {base}: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
