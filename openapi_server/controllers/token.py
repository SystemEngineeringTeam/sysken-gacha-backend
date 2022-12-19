import os
import time
import six
import hashlib
from jose import jwt, JWTError
from dotenv import load_dotenv
from werkzeug.exceptions import Unauthorized, BadRequest

load_dotenv()
JWT_ISSUER = os.getenv("JWT_ISSUER", "jp.ac.aitech.ie")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_LIFETIME_SECONDS = os.getenv('JWT_LIFETIME_SECONDS', 600)
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')


def generate_token(user_id):
    timestamp = int(time.time())
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }
    # try:
    #     print(decode_token(jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)))
    # except JWTError as e:
    #     six.raise_from(BadRequest, e)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)

# def get_hash(s: str):
# return hashlib.sha256(s.encode()).hexdigest()
# return hashlib.
