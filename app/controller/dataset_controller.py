from flask import request
from flask_jwt_extended import *
from app.models import response_model
from app import db
from app import decorator
from app import validator
from app.models.dataset_model import Dataset


def index():
    try:
        return response_model.Ok("200", f"Hello World", [],[])
    except Exception as e:
        print(e)
    

@jwt_required()
def store():
    try:
        print(get_jwt_identity()["username"])
        temp = request.get_json()

        
        data = Dataset(
                judul = temp["judul"],
                deskripsi = temp["deskripsi"],
                tahun = temp["tahun"],
                topik = temp["topik"],
                organisasi = temp["organisasi"],
                cuid = get_jwt_identity()["id"]
        )
            
        db.session.add(data) 
        db.session.commit()
        data = singleTransform(data)
        return response_model.Ok("200", 'success', {"data": data}, [])
    except Exception as e:
            print(e)
            return response_model.BadRequest("400", 'Unknown Error', [])

@jwt_required()
def update(newId):
    try:

        data = Dataset.getById(newId)
        payload  = validator.getValidator()
        if not data:
            return response_model.BadRequest("", "Id Not Found", [])

        if payload['role'] != "superuser" and payload["id"] != data.cuid:
            return response_model.BadRequest(
                400, "You need access to edit this data", []
            )
        temp = request.get_json()
        data.judul = temp['judul']
        data.deskripsi = temp['deskripsi']
        data.tahun = temp['tahun']
        data.topik = temp['topik']
        data.organisasi = temp['organisasi']
        data.cuid = temp['cuid']
        data.muid = temp['muid']
        db.session.commit()
        data = singleTransform(data)
        return response_model.Ok(
            '200',
            'Data updated successfull',
             {"data": data}, []
        )
    except Exception as e:
        print(e)
        return response_model.BadRequest(400, "Data cannot be change", [])


def getAll():
    try:
        page = request.args.get("page", 1, type = int)
        per_page = request.args.get("page", 10, type = int)
        data = Dataset.query.paginate(page, per_page)
        return response_model.Ok(
            "200", "success to get data", [{
                "id": str(a.id),
                "judul" : a.judul,
                "deskripsi": a.deskripsi,
                "tahun" : str(a.tahun),
                "topik": a.topik,
                "organisasi": a.organisasi,
                "cuid" : str(a.cuid),
                "muid" : str(a.muid),
                "created_at" : a.created_at,
                "modified_at" : a.modified_at
            } 
            for a in data.items
            ], 
            {
                "count" : str(data.total),
                "page" :  str(page),
                "per_page" : str(per_page),
                "pages" : str(data.pages)
            },
        )
    except Exception as e:
        print(e)
        return response_model.BadRequest(400, "Data cannot be show", [])


def takeById(id):
    try:
        data = singleTransform(Dataset.getById(id))
        return response_model.Ok("200", "SUCCESS", data, [])
    except Exception as e:
        print(e)
        return response_model.BadRequest(405, "Data not found - or error", [])

def takeByDesc(desc):
    try:
        data = singleTransform(Dataset.getByDeskripsi(desc))
        return response_model.Ok("200", "SUCCESS", data, [])
    except Exception as e:
        print(e)
        return response_model.BadRequest(405, "Data not found - or error", [])

def takeByTitle(title):
    try:
        data = singleTransform(Dataset.getByJudul(title))
        return response_model.Ok("200", "SUCCESS", data, [])
    except Exception as e:
        print(e)
        return response_model.BadRequest(405, "Data not found - or error", [])

@jwt_required()
def deleteById(targetId):
    try:
        data = Dataset.query.filter_by(id = targetId).first()
        payload  = get_jwt_identity()
        if not data:
            return response_model.BadRequest("", "Id Not Found", [])
        if payload["role"] != "superuser" and payload["id"] != data.cuid:
            return response_model.BadRequest(400, "you need access to delete this", [], )
  
    
        db.session.delete(data)
        db.session.commit()
        return response_model.Ok('200', "Data Deleted successfully", [], [])

    except Exception as e:
        print(e)
        return response_model.BadRequest(405, "Data delete process cannot be run - or error", [])

def singleTransform(newData):
    data = {
        'id': str(newData.id),
        'judul' : newData.judul,
        'deskripsi' : newData.deskripsi,
        'tahun': str(newData.tahun),
        'topik':newData.topik,
        'organisasi': newData.organisasi,
        'cuid' : str(newData.cuid),
        'muid':  str(newData.muid),
        'created_at' : newData.created_at,
        'modified_at': newData.modified_at
    }
    return data

def complexTransform(newData):
    arr = []
    for i in newData:
        arr.append(singleTransform(i))
    return arr