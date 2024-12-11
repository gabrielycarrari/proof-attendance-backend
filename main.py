from io import BytesIO
import io
from fastapi import FastAPI, Form, Path
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from fastapi import HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from dtos.alterar_evento_dto import AlterarEventoDto
from dtos.entrar_dto import EntrarDto
from dtos.evento_com_qtd_dto import EventoComQtdDto
from dtos.inserir_evento_dto import InserirEventoDto
from dtos.registrar_presenca_dto import RegistrarPresencaDto
from models.evento_model import Evento
from models.presenca_model import Presenca
from repositories.evento_repo import EventoRepo
from repositories.presenca_repo import PresencaRepo
from repositories.usuario_repo import UsuarioRepo

from routes import auth_routes, certificate_routes
from dtos.inserir_usuario_dto import InserirUsuarioDTO
from dtos.problem_details_dto import ProblemDetailsDto
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import gerar_chave_unica, obter_hash, conferir_senha
from util.generate_certificate import generate_certificate

UsuarioRepo.criar_tabela()
UsuarioRepo.inserir_usuarios_json("sql/usuarios.json")
EventoRepo.criar_tabela()
EventoRepo.inserir_eventos_json("sql/eventos.json")
PresencaRepo.criar_tabela()


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
    usuario_data["senha"] = obter_hash(usuario_data["senha"])
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
async def obter_eventos(id_organizador: int = Path(..., title="Id do Organizador", ge=1)):
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


@app.get("/obter_evento/{id_evento}")
async def obter_evento(id_evento: int = Path(..., title="Id do Evento", ge=1)):
    evento = EventoRepo.obter_por_id(id_evento)
    return evento


@app.post("/alterar_evento", status_code=200)
async def alterar_evento(evento_dto: AlterarEventoDto):
    evento_old = EventoRepo.obter_por_id(evento_dto.id)
    if not evento_old:
        pd = ProblemDetailsDto("str", "Evento não encontrado.", "value_not_found", ["body", "id"])
        return JSONResponse(pd.to_dict(), status_code=404)
    
    chave_unica = gerar_chave_unica(evento_dto.id_organizador, evento_dto.nome, evento_dto.data_inicio, evento_dto.hora_inicio)

    
    #TODO: Validar se a chave única já existe
    #TODO: Validar se a data e hora do evento já passou
    #TODO: Validar o id do organizador
    hora_inicio = evento_dto.hora_inicio.strftime('%H:%M') 
    novo_evento = Evento(evento_dto.id, evento_dto.nome, evento_dto.descricao, evento_dto.carga_horaria, evento_dto.data_inicio, hora_inicio, chave_unica, evento_dto.id_organizador)
    novo_evento = EventoRepo.alterar(novo_evento)
    return novo_evento

@app.post("/excluir_evento", status_code=204)
async def excluir_evento(id_evento: int = Form(..., title="Id do Evento", ge=1)):
    if EventoRepo.excluir(id_evento):
        return None
    pd = ProblemDetailsDto(
        "int",
        f"O evento com id <b>{id_evento}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id_evento"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)

@app.get("/obter_evento_por_chave/{chave_unica}")
async def obter_evento_por_chave(chave_unica: str = Path(..., title="Chave única")):
    evento = EventoRepo.obter_por_chave_unica(chave_unica)
    return evento


### Presenças
@app.get("/obter_presencas/{id_participante}")
async def obter_presencas(id_participante: int = Path(..., title="Id do Participante", ge=1)):
    presencas = PresencaRepo.obter_todos_por_participante(id_participante)
    eventos = []
    for presenca in presencas:
        evento = EventoRepo.obter_por_id(presenca.id_evento)
        qtd_participantes = PresencaRepo.obter_quantidade_por_evento(presenca.id_evento)
        evento_com_qtd = EventoComQtdDto(
            id = evento.id,
            nome = evento.nome,
            descricao = evento.descricao,
            carga_horaria = evento.carga_horaria,
            data_inicio = evento.data_inicio,
            hora_inicio = evento.hora_inicio,
            id_organizador = evento.id_organizador,
            id_presenca = presenca.id,
            qtd_participantes = qtd_participantes
        )
        eventos.append(evento_com_qtd)
    return eventos


@app.post("/registrar_presenca", status_code=200)
async def registrar_presenca(presenca_dto: RegistrarPresencaDto):
    evento = EventoRepo.obter_por_id(presenca_dto.id_evento)
    if not evento:
        pd = ProblemDetailsDto("str", "Evento não encontrado.", "value_not_found", ["body", "id_evento"])
        return JSONResponse(pd.to_dict(), status_code=404)

    participante = UsuarioRepo.obter_por_id(presenca_dto.id_participante)
    if not participante:
        pd = ProblemDetailsDto("str", "Participante não encontrado.", "value_not_found", ["body", "id_participante"])
        return JSONResponse(pd.to_dict(), status_code=404)
    
    # TODO: verificar se presenca já existe
    chave_evento = gerar_chave_unica(evento.id_organizador, evento.nome, evento.data_inicio, evento.hora_inicio)
    codigo_autenticacao = str(presenca_dto.id_participante) + chave_evento
    codigo_autenticacao = obter_hash(codigo_autenticacao)
    #TODO: Validar hora, data e evento finalizado

    nova_presenca = Presenca(None, participante.id, evento.id, codigo_autenticacao)
    nova_presenca = PresencaRepo.inserir(nova_presenca)
    return nova_presenca



@app.get("/generate-certificate/{id_presenca}")
async def generate_pdf(id_presenca: int = Path(..., title="Id da Presença", ge=1)):
    presenca = PresencaRepo.obter_por_id(id_presenca)
    if not presenca:
        pd = ProblemDetailsDto("str", "Presença não encontrada.", "value_not_found", ["body", "id_presenca"])
        return JSONResponse(pd.to_dict(), status_code=404)
    
    evento = EventoRepo.obter_por_id(presenca.id_evento)
    participante = UsuarioRepo.obter_por_id(presenca.id_participante)
    if not evento or not participante:
        pd = ProblemDetailsDto("str", "Evento ou participante não encontrado.", "value_not_found", ["body", "id_evento", "id_participante"])
        return JSONResponse(pd.to_dict(), status_code=404)
    
    # certificate_pdf = generate_certificate(participante.nome, evento.data_inicio, evento.hora_inicio, evento.carga_horaria, evento.chave_unica, evento.nome)
    # with open(certificate_pdf, "rb") as file:
    #     filename = f"certificate_{evento.nome.split(" ")[0]}_{participante.nome.split(" ")[0]}.pdf"
    #     return FileResponse(file, media_type='application/pdf', filename=filename)
    pdf_content = generate_certificate(participante.nome, evento.data_inicio, evento.hora_inicio, evento.carga_horaria, evento.chave_unica, evento.nome)

    # Cria um buffer com o conteúdo do PDF
    pdf_buffer = io.BytesIO(pdf_content)

    # Define o nome do arquivo para download
    filename = f"certificate_{evento.nome.split(' ')[0]}_{participante.nome.split(' ')[0]}.pdf"
    
    # Retorna o PDF como uma resposta de streaming
    return StreamingResponse(pdf_buffer, media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename={filename}"})