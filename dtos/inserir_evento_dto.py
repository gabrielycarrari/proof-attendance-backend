from datetime import time
from pydantic import BaseModel, field_validator

from util.validators import *


class InserirEventoDto(BaseModel):
    nome: str
    descricao: str
    carga_horaria: int
    data_inicio: date
    hora_inicio: time
    id_organizador: int

    # @field_validator("nome")
    # def validar_nome(cls, v):
    #     msg = is_size_between(v, "Nome", 2, 128)
    #     if msg: raise ValueError(msg)
    #     return v
