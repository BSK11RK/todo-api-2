from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings


# パスワードハッシュ
password_hash = PasswordHash.recommended()


def verify_password(
    plain_password: str, 
    hashed_password: str
) -> bool:
    return password_hash.verify(
        plain_password, 
        hashed_password
    )


def create_access_token(
    data: dict, 
    expire_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    
    if expire_delta is not None:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    # JWTに有効期限を追加
    to_encode.update({"exp": expire})
    
    # JWTを作成
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token, 
        settings.secret_key, 
        algorithms=[settings.algorithm]
    )
    
    return payload