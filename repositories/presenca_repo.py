import json
import sqlite3
from typing import List, Optional
from models.presenca_model import Presenca
from sql.presenca_sql import *
from util.database import obter_conexao


class PresencaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, presenca: Presenca) -> Optional[Presenca]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        presenca.id_participante,
                        presenca.id_evento,
                        presenca.codigo_autenticacao,
                                               
                    ),
                )
                if cursor.rowcount > 0:
                    presenca.id = cursor.lastrowid
                    return presenca
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos_por_participante(cls, participante: int = 1) -> List[Presenca]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_POR_PARTICIPANTE, (participante,)).fetchall()
                participacoes = [Presenca(*t) for t in tuplas]
                return participacoes
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, presenca: Presenca) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        presenca.id_participante,
                        presenca.id_evento,
                        presenca.codigo_autenticacao,
                        presenca.id,
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
    def obter_por_id(cls, id: int) -> Optional[Presenca]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                evento = Presenca(*tupla)
                return evento
        except sqlite3.Error as ex:
            print(ex)
            return None

