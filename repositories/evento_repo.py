import json
import sqlite3
from typing import List, Optional
from models.evento_model import Evento
from sql.evento_sql import *
from util.database import obter_conexao


class EventoRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, evento: Evento) -> Optional[Evento]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        evento.nome,
                        evento.descricao,
                        evento.carga_horaria,
                        evento.data_inicio,
                        evento.hora_inicio,
                        evento.chave_unica,
                        evento.id_organizador,
                                               
                    ),
                )
                if cursor.rowcount > 0:
                    evento.id = cursor.lastrowid
                    return evento
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos_por_organizador(cls, organizador: int = 1) -> List[Evento]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_POR_ORGANIZADOR, (organizador,)).fetchall()
                eventos = [Evento(*t) for t in tuplas]
                return eventos
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, evento: Evento) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        evento.nome,
                        evento.descricao,
                        evento.carga_horaria,
                        evento.data_inicio,
                        evento.hora_inicio,
                        evento.chave_unica,
                        evento.id_organizador,
                        evento.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Evento]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                evento = Evento(*tupla)
                return evento
        except sqlite3.Error as ex:
            print(ex)
            return None
    
    @classmethod
    def obter_por_chave_unica(cls, chave_unica: str) -> Optional[Evento]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_CHAVE_UNICA, (chave_unica,)).fetchone()
                evento = Evento(*tupla)
                return evento
        except sqlite3.Error as ex:
            print(ex)
            return None


    # @classmethod
    # def obter_quantidade_por_perfil(cls, perfil: int = 1) -> Optional[int]:
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             tupla = cursor.execute(SQL_OBTER_QUANTIDADE_POR_PERFIL, (perfil,)).fetchone()
    #             return int(tupla[0])
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return None

    # @classmethod
    # def inserir_usuarios_json(cls, arquivo_json: str):
    #     if UsuarioRepo.obter_quantidade_por_perfil() == 0:
    #         with open(arquivo_json, "r", encoding="utf-8") as arquivo:
    #             usuarios = json.load(arquivo)
    #             for usuario in usuarios:
    #                 UsuarioRepo.inserir(Usuario(**usuario))

    # @classmethod
    # def obter_todos(cls) -> List[Usuario]:
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             tuplas = cursor.execute(
    #                 SQL_OBTER_TODOS
    #             ).fetchall()
    #             usuarios = [Usuario(*t) for t in tuplas]
    #             return usuarios
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return None
        
    # @classmethod
    # def obter_busca(cls, termo: str, pagina: int, tamanho_pagina: int) -> List[Usuario]:
    #     termo = "%" + termo + "%"
    #     offset = (pagina - 1) * tamanho_pagina
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             tuplas = cursor.execute(
    #                 SQL_OBTER_BUSCA, (termo, termo, tamanho_pagina, offset)
    #             ).fetchall()
    #             usuarios = [Usuario(*t) for t in tuplas]
    #             return usuarios
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return None

    # @classmethod
    # def obter_quantidade_busca(cls, termo: str) -> Optional[int]:
    #     termo = "%" + termo + "%"
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             tupla = cursor.execute(
    #                 SQL_OBTER_QUANTIDADE_BUSCA, (termo, termo)
    #             ).fetchone()
    #             return int(tupla[0])
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return None

    # @classmethod
    # def obter_por_email(cls, email: str) -> Optional[Usuario]:
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             tupla = cursor.execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
    #             if tupla:
    #                 usuario = Usuario(*tupla)
    #                 return usuario
    #             else:
    #                 return None
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return None

    # @classmethod
    # def alterar_token(cls, id: int, token: str) -> bool:
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             cursor.execute(SQL_ALTERAR_TOKEN, (token, id))
    #             return cursor.rowcount > 0
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return False

    # @classmethod
    # def obter_por_token(cls, token: str) -> Optional[Usuario]:
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             tupla = cursor.execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
    #             if tupla:
    #                 usuario = Usuario(*tupla)
    #                 return usuario
    #             else:
    #                 return None
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return None

    # @classmethod
    # def alterar_senha(cls, id: int, senha: str) -> bool:
    #     try:
    #         with obter_conexao() as conexao:
    #             cursor = conexao.cursor()
    #             cursor.execute(SQL_ALTERAR_SENHA, (senha, id))
    #             return cursor.rowcount > 0
    #     except sqlite3.Error as ex:
    #         print(ex)
    #         return False
