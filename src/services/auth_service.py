from __future__ import annotations
import hashlib
import secrets

from models.user import User
from repositories import user_repository

def _verify_password(password: str, password_hash: str) -> bool:
    """Проверяет, совпадает ли введенный пароль с хешем из БД."""
    try:
        algorithm, iterations, salt_hex, digest_hex = password_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)

        actual_digest = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt, int(iterations)
        )
        return actual_digest == expected_digest
    except (ValueError, IndexError):
        return False


def authenticate(login: str, password: str) -> User | None:
    """Возвращает объект User, если логин и пароль верны, иначе None."""
    if not login or not password:
        return None

    user = user_repository.get_by_login(login)
    if not user:
        return None

    if _verify_password(password, user.password_hash):
        return user

    return None