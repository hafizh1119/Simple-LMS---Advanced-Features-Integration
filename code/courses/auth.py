import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from ninja.security import HttpBearer
from ninja.errors import HttpError


ALGORITHM = "HS256"


def create_token(user, token_type="access"):
    minutes = 60 if token_type == "access" else 60 * 24 * 7

    payload = {
        "user_id": user.id,
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
        "iat": datetime.utcnow(),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Token expired")

    except jwt.InvalidTokenError:
        raise HttpError(401, "Invalid token")


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HttpError(401, "Invalid token type")

        try:
            return User.objects.get(
                id=payload["user_id"]
            )

        except User.DoesNotExist:
            raise HttpError(401, "User not found")


auth = JWTAuth()