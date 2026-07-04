"""
report_writer.py
================

Clase `ReportWriter`: separa la ESCRITURA del archivo de salida de la logica de
simulacion. Equivale a `ReportWriter` de la documentacion (seccion 3).

Formato de salida (una linea por proceso):
    etiqueta;BT;AT;Q;Pr;WT;CT;RT;TAT
y al final del archivo, la linea de promedios de WT, CT, RT y TAT.
"""

import os
from process import Process


def _fmt(value):
    """Enteros exactos sin decimales; si hay decimales, 2 cifras."""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


class ReportWriter:
    """Escribe el archivo de resultados con el formato exacto pedido."""

    @staticmethod
    def write_results(filename, processes, averages):
        # Salida ordenada por etiqueta para presentacion estable.
        ordered = sorted(processes, key=lambda p: p.label)

        lines = []
        lines.append(f"# archivo: {os.path.basename(filename)}")
        lines.append("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT")

        for p in ordered:
            lines.append(";".join([
                p.label,
                _fmt(p.burst_time),
                _fmt(p.arrival_time),
                str(p.queue_id),
                str(p.priority),
                _fmt(p.waiting_time),
                _fmt(p.completion_time),
                _fmt(p.response_time),
                _fmt(p.turnaround_time),
            ]))

        lines.append(
            f"# WT={_fmt(averages['WT'])}; CT={_fmt(averages['CT'])}; "
            f"RT={_fmt(averages['RT'])}; TAT={_fmt(averages['TAT'])};"
        )

        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return filename
