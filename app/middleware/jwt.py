from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):

    print("ENCODE SECRET:", SECRET_KEY)

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    print("GENERATED TOKEN:", token)

    return token

def verify_access_token(token: str):

    try:

        print("DECODE SECRET:", SECRET_KEY)
        print("RECEIVED TOKEN:", repr(token))

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD:", payload)

        return payload

    except JWTError as e:
        print("JWT ERROR:", str(e))
        return None