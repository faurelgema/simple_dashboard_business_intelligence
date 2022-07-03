from flask import request
from flask_jwt_extended import *
from app.models import response_model
from app import db
from datetime import datetime
from app import validator
from app.models.dataset_model import Dataset
import json
from sqlalchemy import and_
from sqlalchemy import desc, asc
from app.decorator import *

def index():
    try:
        return response_model.Ok("200", f"Hello World", [],[])
    except Exception as e:
        print(e)

# def weekly():
#     searchable = ['start_date, end_date']
#     temp = request.args
#     for index1, index2 in temp.items():
#             if index1 not in searchable:
#                 return response_model.BadRequest(403, "Request Unsolved",[])
#             else
                
    
def customization():
    try:
        page = request.args.get("page",1, type=int)
        per_page = validate_per_page(request.args.get("per_page", 100, type=int))
        searchable = ["start_date", "end_date",'like','page', 'per_page','sort', 'limit', 'where', 'offset']
        column = ['id', 'judul', 'deskripsi','topik', 'tahun', "created_at", "modified_at",'cuid', 'muid']
        start_date = request.args.get('start_date')
        temp = request.args
        query = Dataset.query
        print (temp)
        for index1, index2 in temp.items():
            if index1 not in searchable:
                return response_model.BadRequest(403, "Request Unsolved",[])
            if index1 == "sort":
                value = index2.split(":")
                if value[0] not in column:
                    return response_model.BadRequest(404, "Not found", [],)
                if value[1] == "desc":
                    query = query.order_by(getattr(Dataset, value[0]).desc())
                elif value[1]== "asc":
                    query= query.order_by(getattr(Dataset, value[0]))
            if index1 == "where":
                d = json.loads(index2)
                query = query.filter(and_(getattr(Dataset, cl).like(vl) for cl,vl in d.items()))
            if index1 == "like":
                like_value = request.args.get('like')
                query = query.filter(Dataset.judul.like( "%"+like_value + "%"))
            if index1 == "start_date" and "end_date":
                start_date = request.args.get('start_date')
                date_time_obj1 = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = request.args.get('end_date')
                date_time_obj2 = datetime.strptime(end_date, '%Y-%m-%d')
                query = query.filter(Dataset.created_at.between(date_time_obj1, date_time_obj2))
        query=query.paginate(page, per_page)
        return response_model.Ok(202, "Data Sort Completed", transform(query.items),  {
                "total_data": str(query.total),
                "page" : page,
                "per_page" : per_page,
                "total_page" : str(query.pages),
            })
        # return "hello"
    except Exception as e:
            print(e)
            return response_model.BadRequest("400", 'Error get parameter', [])

def validate_per_page(per_page):
    if per_page and per_page > 100 or per_page < 1:
        return response_model.BadRequest(450, "per page invalid", [])

    return per_page


@jwt_required()
def store():
    try:
        temp = request.get_json()

        
        data = Dataset(
                judul = temp["judul"],
                deskripsi = temp["deskripsi"],
                tahun = temp["tahun"],
                topik = temp["topik"],
                organisasi = temp["organisasi"],
                cuid = temp["cuid"]
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
        'created_at' : newData.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'modified_at': newData.modified_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return data
  

def complexTransform(newData):
    arr = []
    for i in newData:
        arr.append(singleTransform(i))
        return arr

def transform(newData):
    return [singleTransform(i) for i in newData]




def pagination(target_page = 1, limit_per_page=10):
    try:
        page = request.args.get("page", target_page, type = int)
        per_page = request.args.get("page", limit_per_page, type = int)
        data= Dataset.query.paginate(page, per_page)
        return response_model.Ok(
            "200", 
            "Success", 
            transform(data),
            {
                "count": str(data.total),
                "page" : str(page),
                "per_page" : str(per_page),
                "total_page" : str(data.pages),
            }, 
        )
    except Exception as e:
        print(e)
        return response_model.BadRequest(400, "request gagal", [])

def weekly_count(start_date, end_date):
    date_from_db = db.engine.execute(f'''
    SELECT to_char(date_trunc('week'::text, ((created_at)::date)::timestamp), 'YYYY-MM-DD'::text) AS week, COUNT(*) FROM dataset WHERE created_at BETWEEN '{start_date}' AND '{datetime.strptime(end_date, "%Y-%m-%d")+ timedelta(days=1)}' GROUP BY to_char(date_trunc('week'::text, ((created_at)::date)::timestamp), 'YYYY-MM-DD'::text) ORDER BY to_char(date_trunc('week'::text, ((created_at)::date)::timestamp), 'YYYY-MM-DD'::text)''')
    return response_model.Ok(200, "OK", [{str(i[0]): i[1] for i in date_from_db}], [])
