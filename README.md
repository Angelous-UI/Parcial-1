# Simulador de Planificación MLQ (Multilevel Queue)

Simulador del algoritmo de planificación de procesos **Multilevel Queue (MLQ)**
implementado en **Python 3** con paradigma **orientado a objetos**.
Parcial 1 — Sistemas Operativos · Universidad del Valle.

> La documentación de planeación original está pensada para C++; este proyecto
> mantiene la misma arquitectura de clases y estructura de carpetas, pero
> implementada en Python.

## Esquema de colas (de mayor a menor prioridad)

| Cola | Política | Quantum |
|------|----------|---------|
| 1 (máxima prioridad) | Round Robin | 1 |
| 2 | Round Robin | 3 |
| 3 (mínima prioridad) | SJF (no expropiativo) | — |

**Despacho entre colas:** prioridad estricta con expropiación. La cola de menor
número se ejecuta siempre que tenga procesos listos; si llega un proceso a una
cola de mayor prioridad mientras corre uno de menor prioridad, este es
expropiado y vuelve a su cola conservando su tiempo restante.

## Estructura del proyecto

```
mlq-scheduler/
├── README.md
├── .gitignore
├── run_all.py                # ejecuta todos los inputs de una vez
├── src/
│   ├── main.py               # punto de entrada (parsear -> simular -> escribir)
│   ├── process.py            # clase Process (datos + métricas)
│   ├── scheduling_policy.py  # clase abstracta SchedulingPolicy
│   ├── round_robin.py        # política Round Robin
│   ├── sjf.py                # política SJF
│   ├── queue.py              # clase Queue (lista de listos + política)
│   ├── mlq_scheduler.py      # núcleo de la simulación + métricas
│   ├── file_parser.py        # lectura del archivo de entrada
│   └── report_writer.py      # escritura del archivo de salida
├── inputs/                   # archivos de prueba (formato del enunciado)
├── outputs/                  # resultados generados por el simulador
└── docs/
    └── informe.md            # informe técnico + declaración de uso de IA
```

## Formato de entrada

Una línea por proceso (las líneas que empiezan con `#` son comentarios):

```
etiqueta; BT; AT; Q; Prioridad
```

- **BT**: Burst Time (tiempo de ráfaga)
- **AT**: Arrival Time (tiempo de llegada)
- **Q**: número de cola (1, 2 o 3)
- **Prioridad**: 5 (alta) … 1 (baja)

## Formato de salida

```
etiqueta;BT;AT;Q;Pr;WT;CT;RT;TAT
```

Y al final del archivo, una línea con los promedios de WT, CT, RT y TAT.
- **WT**: Waiting Time · **CT**: Completion Time · **RT**: Response Time · **TAT**: Turnaround Time

## Cómo ejecutar

Requisitos: solo **Python 3.8+** (sin librerías externas).

Un solo archivo:

```bash
cd mlq-scheduler
python src/main.py inputs/mlq001.txt
# -> genera outputs/mlq001_out.txt
```

Elegir el nombre de salida:

```bash
python src/main.py inputs/mlq001.txt outputs/resultado.txt
```

Todos los archivos de `inputs/` de una vez:

```bash
python run_all.py
```

## Métricas

$$TAT = CT - AT \qquad WT = TAT - BT \qquad RT = start - AT$$
