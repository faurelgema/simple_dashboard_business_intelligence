from app import app
from app.controller import user_controller

@app.route('/')
def index():
    return "HELLO WORLD" 

@app.route('/auth/login', methods=['POST'])
def login():
    return user_controller.login()

@app.route('/auth/registration', methods=['POST'])
def registration():
    return user_controller.registration()