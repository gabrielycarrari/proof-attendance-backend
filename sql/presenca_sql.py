SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS presenca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_participante INTEGER NOT NULL,
        id_evento INTEGER NOT NULL,
        codigo_autenticacao TEXT NOT NULL UNIQUE,
        FOREIGN KEY (id_participante) REFERENCES usuario(id),
        FOREIGN KEY (id_evento) REFERENCES evento(id)
    )
"""

SQL_INSERIR = """
    INSERT INTO presenca(id_participante, id_evento, codigo_autenticacao)
    VALUES (?, ?, ?)
"""

SQL_OBTER_TODOS_POR_PARTICIPANTE = """
    SELECT id, id_participante, id_evento, codigo_autenticacao
    FROM presenca
    WHERE id_participante=?
    ORDER BY id DESC
"""

## ??
SQL_ALTERAR = """
    UPDATE presenca
    SET id_participante=?, id_evento=?, codigo_autenticacao=?
    WHERE id=?
"""


SQL_EXCLUIR = """
    DELETE FROM presenca    
    WHERE id=?
"""

SQL_OBTER_POR_ID = """
    SELECT id, id_participante, id_evento, codigo_autenticacao
    FROM presenca
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE_POR_EVENTO = """
    SELECT COUNT(*)
    FROM presenca
    WHERE id_evento=?
"""