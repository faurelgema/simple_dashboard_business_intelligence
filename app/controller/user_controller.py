
from flask import request
from app.models.user_model import Users
from app.models import response_model
from app import db

from datetime import timedelta
from flask_jwt_extended import *

def login():
    try:
        authLogin = request.get_json()
        print(authLogin)
        if not authLogin:
            return response_model.BadRequest(401, 'Fill your username and password!')
        user = Users.query.filter_by(username=authLogin["username"]).first()
        if not user:
            return response_model.BadRequest(402, 'Invalid username',  [])
        if not user.checkPassword(authLogin["password"]):
            return response_model.BadRequest(402, 'Invalid password',  [])
        
        data  = singleTransform(user)
    
        access_token = create_access_token(data, fresh=True,expires_delta=timedelta(days = 1))


        return response_model.Ok("200", "Login successfull", {"access_token" : access_token}, [])

    except Exception as e:
        print(e)
        return response_model.BadRequest(501, "Unknown Error", [])


def auth():
    pass

def registration():
    try:
        username = request.json["username"]
        password = request.json["password"]
        role = request.json["role"]
        if Users.query.filter_by(username = username).first():
            return response_model.BadRequest("", "Username not available: has been taken", [])
        
        users = Users(username=username, role=role)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit() 
        data  = singleTransform(users)
        return response_model.Ok(200, 'Registration successfull', {"data" : data} , "")
    except Exception as e:
        print(e)
        return response_model.BadRequest(400, e, [])


def singleTransform(user):
    data = {
        "id" : user.id,
        "username" : user.username,
        "role" : user.role
    }
    return data

def complexTransform(users):
    arr = []
    for i in users:
        arr.append(singleTransform(i))
        return arr

@jwt_required(refresh=True)
def refreshToken():
    try: 
        refresh_token = create_refresh_token(
            get_jwt_identity(), expires_delta=timedelta(days = 1)
        )
        return response_model.Ok(202, "Refresh Successfull",{"refresh_token" : refresh_token}, [])

    except Exception as e:
        print(e)
        return response_model.BadRequest(400, "Bad Request", [])