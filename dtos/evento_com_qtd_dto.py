from datetime import time
from pydantic import BaseModel

from util.validators import *


class EventoComQtdDto(BaseModel):
    id: int
    nome: str
    descricao: str
    carga_horaria: int
    data_inicio: date
    hora_inicio: time
    chave_unica: str
    id_organizador: int
    id_presenca: int
    qtd_participantes: int

  
