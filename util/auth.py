from datetime import datetime
import bcrypt

def obter_hash(termo: str) -> str:
    try:
        hashed = bcrypt.hashpw(termo.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False
    

def gerar_chave_unica(id_organizador, nome_evento, data_inicio, hora_inicio):
    sigla_evento = ''.join([word[0].upper() for word in nome_evento.split()][:3])

    if not isinstance(data_inicio, datetime):
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')

    if not isinstance(hora_inicio, datetime):
        hora_inicio = datetime.strptime(hora_inicio, '%H:%M')

    data_formatada = data_inicio.strftime('%d%m%Y')  
    hora_formatada = hora_inicio.strftime('%H%M') 
    
    chave_unica = f"{id_organizador}{sigla_evento}{data_formatada}{hora_formatada}"
    
    return chave_unica