from app import app
from app.controller import dashboard_controller

@app.route('/dashboard/organisasi1', methods = ["GET"])
def dashboard1():
    return dashboard_controller.organisasi_1()

@app.route('/dashboard/organisasi2', methods = ["GET"])
def dashboard2():
    return dashboard_controller.organisasi_2()

@app.route('/dashboard/topik1', methods = ["GET"])
def topik1():
    return dashboard_controller.topik1()

@app.route('/dashboard/topik2', methods = ["GET"])
def topik2():
    return dashboard_controller.topik2()

@app.route('/dashboard/tahun1', methods = ["GET"])
def tahun1():
    return dashboard_controller.tahun1()

@app.route('/dashboard/tahun2', methods = ["GET"])
def tahun2():
    return dashboard_controller.tahun2()