from dataclasses import dataclass
from datetime import date
from datetime import time
from typing import Optional


@dataclass
class Evento:
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    carga_horaria: Optional[int] = None
    data_inicio: Optional[date] = None
    hora_inicio: Optional[time] = None
    chave_unica: Optional[str] = None
    id_organizador: Optional[int] = None
