from app import app
from app.controller import dataset_controller
from flask_jwt_extended import *
from flask import request
    
@app.route('/dataset', methods = ["GET"])
def getAll():
    return dataset_controller.customization()

@app.route('/dataset/weekly', methods = ["GET"])
def getWeekly():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return dataset_controller.weekly_count(start_date, end_date)

@app.route('/dataset', methods=['POST'])
def addDataset():
    return dataset_controller.store()

@app.route('/dataset/<id>', methods=['GET', 'PUT', 'DELETE'])
def methodstype(id):
    if request.method == "GET":
        return dataset_controller.takeById(id)

    elif request.method == "DELETE":
        return dataset_controller.deleteById(id)

    elif request.method == "PUT":   
        return dataset_controller.update(id)