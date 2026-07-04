"""
file_parser.py
==============

Clase `FileParser`: separa la LECTURA del archivo de entrada de la logica de
simulacion (principio de responsabilidad unica). Equivale a `FileParser` de la
documentacion (seccion 3).

Formato de entrada (una linea por proceso):
    etiqueta; BT; AT; Q; Prioridad

  - Los campos se separan por ';' y pueden llevar espacios alrededor.
  - Las lineas que empiezan por '#' son comentarios y se ignoran.
  - Las lineas en blanco se ignoran.
"""

import os
from process import Process


class FileParser:
    """Lee un archivo de entrada y devuelve una lista de `Process`."""

    @staticmethod
    def parse(filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"No se encontro el archivo de entrada: {filename}")

        processes = []
        with open(filename, "r", encoding="utf-8") as f:
            for line_number, raw in enumerate(f, start=1):
                line = raw.strip()

                if not line or line.startswith("#"):
                    continue  # comentario o linea vacia

                fields = [field.strip() for field in line.split(";")]
                # eliminar campos vacios finales (por ';' al final de linea)
                while fields and fields[-1] == "":
                    fields.pop()

                if len(fields) < 5:
                    raise ValueError(
                        f"Linea {line_number}: se esperaban 5 campos "
                        f"(etiqueta;BT;AT;Q;Prioridad), se recibieron {len(fields)}: {raw!r}"
                    )

                label, bt, at, q, pr = fields[:5]
                try:
                    processes.append(
                        Process(
                            label=label,
                            burst_time=int(bt),
                            arrival_time=int(at),
                            queue_id=int(q),
                            priority=int(pr),
                        )
                    )
                except ValueError as exc:
                    raise ValueError(
                        f"Linea {line_number}: valor numerico invalido -> {exc}"
                    ) from exc

        if not processes:
            raise ValueError(f"El archivo {filename} no contiene procesos validos.")
        return processes
