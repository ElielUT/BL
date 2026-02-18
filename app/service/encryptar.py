from app.core.config import config
from cryptography.fernet import Fernet
from fastapi import HTTPException

KEY = config.encrypto_key
cipher_suite = Fernet(KEY)

def cifrar(contraseña):
    contraseña_encryptada = cipher_suite.encrypt(contraseña.encode())
    return contraseña_encryptada

def descifrar(contraseñaEncr):
    try:
        contraseña_desencryptada = cipher_suite.decrypt(contraseñaEncr.encode())
        return contraseña_desencryptada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descifrar {e}")