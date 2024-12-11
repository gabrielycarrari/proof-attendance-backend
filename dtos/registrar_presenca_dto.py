from datetime import time
from pydantic import BaseModel, field_validator

from util.validators import *


class RegistrarPresencaDto(BaseModel):
    id_participante: int
    id_evento: int
