import base64
import os

from cryptography.fernet import Fernet


def generate_key():
    """
    암, 복호화시 사용할 key를 생성하는 util 함수
    최초 한 번만 사용하고 환경변수로 저장해서 사용
    """
    return Fernet.generate_key()


def encrypt_token(token: str, key: bytes) -> str:
    """
    주어진 토큰을 암호화합니다.

    Args:
        token (str): 암호화할 토큰 문자열
        key (bytes): 암호화에 사용할 키

    Returns:
        str: Base64 URL-safe 인코딩된 암호화된 토큰

    Raises:
        cryptography.fernet.InvalidToken: 유효하지 않은 키가 제공된 경우
    """
    f = Fernet(key)
    token_bytes = token.encode("utf-8")
    encrypted_token = f.encrypt(token_bytes)
    return base64.urlsafe_b64encode(encrypted_token).decode("utf-8")


def decrypt_token(encrypted_token: str, key: bytes) -> str:
    """
    암호화된 토큰을 복호화합니다.

    Args:
        encrypted_token (str): Base64 URL-safe 인코딩된 암호화된 토큰
        key (bytes): 복호화에 사용할 키

    Returns:
        str: 복호화된 원본 토큰 문자열

    Raises:
        cryptography.fernet.InvalidToken: 유효하지 않은 토큰이나 키가 제공된 경우
        binascii.Error: 유효하지 않은 Base64 인코딩된 문자열이 제공된 경우
    """
    f = Fernet(key)
    token_bytes = base64.urlsafe_b64decode(encrypted_token.encode("utf-8"))
    decrypted_token = f.decrypt(token_bytes)
    return decrypted_token.decode("utf-8")
