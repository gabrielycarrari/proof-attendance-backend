from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from dtos.entrar_dto import EntrarDto
from dtos.inserir_evento_dto import InserirEventoDto
from models.evento_model import Evento
from repositories.evento_repo import EventoRepo
from repositories.usuario_repo import UsuarioRepo

from routes import auth_routes
from dtos.inserir_usuario_dto import InserirUsuarioDTO
from dtos.problem_details_dto import ProblemDetailsDto
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import gerar_chave_unica, obter_hash_senha, conferir_senha


UsuarioRepo.criar_tabela()
UsuarioRepo.inserir_usuarios_json("sql/usuarios.json")
EventoRepo.criar_tabela()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cadastrar_usuario", status_code=200)
async def cadastrar_usuario(usuario_dto: InserirUsuarioDTO):
    usuario_data = usuario_dto.model_dump(exclude={"confirmacao_senha"})
    usuario_data["senha"] = obter_hash_senha(usuario_data["senha"])
    novo_usuario = UsuarioRepo.inserir(Usuario(**usuario_data))
    if not novo_usuario or not novo_usuario.id:
        pd = ProblemDetailsDto("str", "Erro ao cadastrar usuário.", "value_not_found", ["body"])
        return JSONResponse(pd.to_dict(), status_code=400)

    return JSONResponse({
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "perfil": novo_usuario.perfil
        }, status_code=200)


@app.post("/entrar", status_code=200)
async def entrar(entrar_dto: EntrarDto):
    usuario_entrou = UsuarioRepo.obter_por_email(entrar_dto.email)
    if ((not usuario_entrou)
        or (not usuario_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, usuario_entrou.senha))):
        pd = ProblemDetailsDto("str", f"Credenciais inválidas. Certifique-se de que está cadastrado e de que sua senha está correta.", "value_not_found", ["body", "email", "senha"])
        return JSONResponse(pd.to_dict(), status_code=404)
    return JSONResponse({
            "id": usuario_entrou.id,
            "nome": usuario_entrou.nome,
            "perfil": usuario_entrou.perfil
        }, status_code=200)


@app.get("/obter_eventos/{id_organizador}")
async def obter_eventos(id_organizador: int = Path(..., title="Id do Produto", ge=1)):
    eventos = EventoRepo.obter_todos_por_organizador(id_organizador)
    return eventos


@app.post("/cadastrar_evento", status_code=200)
async def cadastrar_evento(evento_dto: InserirEventoDto):
    chave_unica = gerar_chave_unica(evento_dto.id_organizador, evento_dto.nome, evento_dto.data_inicio, evento_dto.hora_inicio)

    #TODO: Validar se a chave única já existe
    #TODO: Validar se a data e hora do evento já passou
    #TODO: Validar o id do organizador
    hora_inicio = evento_dto.hora_inicio.strftime('%H:%M') 
    novo_evento = Evento(None, evento_dto.nome, evento_dto.descricao, evento_dto.carga_horaria, evento_dto.data_inicio, hora_inicio, chave_unica, evento_dto.id_organizador)
    novo_evento = EventoRepo.inserir(novo_evento)
    return novo_evento

