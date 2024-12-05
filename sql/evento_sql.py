SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS evento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        carga_horaria INTEGER NOT NULL,
        data_inicio DATE NOT NULL,
        hora_inicio TEXT NOT NULL,
        chave_unica TEXT NOT NULL UNIQUE,
        id_organizador INTEGER NOT NULL,
        FOREIGN KEY (id_organizador) REFERENCES usuario(id))
"""

SQL_INSERIR = """
    INSERT INTO evento(nome, descricao, carga_horaria, data_inicio, hora_inicio, chave_unica, id_organizador)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS_POR_ORGANIZADOR = """
    SELECT id, nome, descricao, carga_horaria, data_inicio, hora_inicio, chave_unica
    FROM evento
    WHERE id_organizador=?
    ORDER BY data_inicio DESC
"""


SQL_ALTERAR = """
    UPDATE evento
    SET nome=?, descricao=?, carga_horaria=?, data_inicio=?, hora_inicio=?, chave_unica=?, id_organizador=?
    WHERE id=?
"""

###
SQL_ALTERAR_TOKEN = """
    UPDATE usuario
    SET token=?
    WHERE id=?
"""

SQL_ALTERAR_SENHA = """
    UPDATE usuario
    SET senha=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM evento    
    WHERE id=?
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, descricao, carga_horaria, data_inicio, hora_inicio, chave_unica
    FROM evento
    WHERE id=?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, cpf, email, perfil, senha
    FROM usuario
    WHERE email=?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, cpf, email, perfil
    FROM usuario
    WHERE token=?
"""

SQL_OBTER_QUANTIDADE_POR_PERFIL = """
    SELECT COUNT(*)
    FROM usuario
    WHERE perfil=?
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, cpf, email
    FROM usuario
    ORDER BY nome
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, cpf, email
    FROM usuario
    WHERE nome LIKE ? OR cpf LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM usuario
    WHERE nome LIKE ? OR cpf LIKE ?
"""

SQL_OBTER_POR_CHAVE_UNICA = """
    SELECT id, nome, descricao, carga_horaria, data_inicio, hora_inicio, chave_unica
    FROM evento
    WHERE chave_unica=?
"""