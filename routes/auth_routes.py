from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dtos.inserir_usuario_dto import InserirUsuarioDTO
from dtos.problem_details_dto import ProblemDetailsDto
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import obter_hash_senha, conferir_senha


router = APIRouter(prefix="/auth")

@router.post("/cadastrar_usuario", status_code=200)
async def cadastrar_usuario(usuario_dto: InserirUsuarioDTO):
    usuario_data = usuario_dto.model_dump(exclude={"confirmacao_senha"})
    usuario_data["senha"] = obter_hash_senha(usuario_data["senha"])
    novo_usuario = UsuarioRepo.inserir(Usuario(**usuario_data))
    if not novo_usuario or not novo_usuario.id:
        pd = ProblemDetailsDto("str", "Erro ao cadastrar usuário.", "value_not_found", ["body"])
        return JSONResponse(pd.to_dict(), status_code=400)

    return JSONResponse({"perfil": novo_usuario.perfil}, status_code=200)


