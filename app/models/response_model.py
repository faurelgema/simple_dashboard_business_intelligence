from flask import jsonify, make_response

def Ok(RC, message, data, pagination):
    response_message = {
        "code" : "200", 
        "message": message,
        "data": data,
        "pagination": pagination
    }
    return make_response(jsonify(response_message)), 200

def BadRequest(RC, message, data):
    response_message = {
        "code" : RC, 
        "message": message,
        "data": data
    }
    return make_response(jsonify(response_message)), 400