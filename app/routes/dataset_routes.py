from app import app
from app.controller import dataset_controller
from flask_jwt_extended import *

    
@app.route('/dataset', methods = ["GET"])
def getAll():
    return dataset_controller.getAll()

@app.route('/dataset/<username>', methods=['POST'])
def addDataset(username):
    return dataset_controller.store()

@app.route('/dataset/<username>/id=<id>', methods=['GET'])
def getById(username, id):
    return dataset_controller.takeById(id)

@app.route('/dataset/<username>/<id>', methods=['DELETE'])
def deleteDatasetById(username, id):
    return dataset_controller.deleteById(id)

@app.route('/dataset/<username>/<id>', methods=['PUT'])
def updateDatasetById(username, id):
    return dataset_controller.update(id)