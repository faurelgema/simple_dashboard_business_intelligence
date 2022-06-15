
import jwt
from app import app
from flask import request
from app.models import response_model
def getValidator():
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return response_model.BadRequest(
            401, "token is missing", []
        )
    return jwt.decode(token, app.config["JWT_PUBLIC_KEY"], algorithms=["RS256"])["sub"]