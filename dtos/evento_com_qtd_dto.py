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
    id_organizador: int
    qtd_participantes: int

  
