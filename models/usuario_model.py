from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    perfil: Optional[int] = None
    senha: Optional[str] = None
    # usar o campo abaixo somente se 
    # for autenticação por cookie
    token: Optional[str] = None
