
from flask import request
from functools import wraps
from app import app
from app.controller.user_controller import *
import jwt
from app.models import response_model

def need_token(param):
    @wraps(param)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")(1)
        if not token:
            return response_model.BadRequest(
                401, "You need token to access this", []
            )
        try:
            data = jwt.decode(token, app.config["JWT_PUBLIC_KEY"], algorithms=["RS256"])

        except Exception as e:
            print(e)
            return response_model.BadRequest(500, "Internal error", [])
        return param(*args, **kwargs)
    return decorated