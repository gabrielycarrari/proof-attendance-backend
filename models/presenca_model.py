from dataclasses import dataclass
from typing import Optional


@dataclass
class Presenca:
    id: Optional[int] = None
    id_participante: Optional[int] = None
    id_evento: Optional[int] = None
    codigo_autenticacao: Optional[str] = None
