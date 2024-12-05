from web3 import Web3
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

web3 = Web3()
router = APIRouter(prefix="/certificate")

@router.post("/registrar_certificado", status_code=200)
async def registrar_certificado(certificate_id: str = Form(...), signature: str = Form(...), address: str = Form(...)):
    try:
        message = f"Certificado: {certificate_id}"
        
        if not verify_signature(message, signature, address):
            raise HTTPException(status_code=400, detail="Assinatura inválida")
        
        certificate_hash = Web3.solidityKeccak(['string'], [certificate_id])       

        return JSONResponse({"message": "Certificado registrado com sucesso."}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verificar_certificado", status_code=200)
async def verificar_certificado(certificate_id: str = Form(...), signature: str = Form(...), address: str = Form(...)):
    try:
        message = f"Certificado: {certificate_id}"
        certificate_hash = Web3.solidityKeccak(['string'], [certificate_id])

        if verify_signature(message, signature, address):
            return JSONResponse({"message": "Certificado válido."}, status_code=200)
        else:
            return JSONResponse({"message": "Certificado inválido."}, status_code=400)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def verify_signature(message: str, signature: str, address: str) -> bool:
    """
    Verifica se a assinatura corresponde ao endereço.
    
    Args:
        message (str): A mensagem que foi assinada.
        signature (str): A assinatura a ser verificada.
        address (str): O endereço que deve corresponder à assinatura.

    Returns:
        bool: True se a assinatura for válida, caso contrário False.
    """
    signature_bytes = Web3.toBytes(hexstr=signature)

    v = signature_bytes[-1]
    r = signature_bytes[:32]
    s = signature_bytes[32:64]

    message_hash = Web3.solidityKeccak(['string'], [message])

    recovered_address = web3.eth.account.recoverHash(message_hash, vrs=(v, r, s))

    return recovered_address.lower() == address.lower()
