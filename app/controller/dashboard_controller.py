from app.models import response_model
from app import db

def organisasi_1():
    return response_model.Ok(200, "success", type1(get_data("organisasi")), [])

def organisasi_2():
    return response_model.Ok(200, type2(get_data("organisasi"),"organisasi"), [], []) 

def topik1():
    return response_model.Ok(200, "success", type1(get_data("topik")), [])

def topik2():
    return response_model.Ok(200, "SUCCESS", type2(get_data("topik"),"topik"), []) 

def tahun1():
    return response_model.Ok(200, "success", type1(get_data("tahun")), [])

def tahun2():
    return response_model.Ok(200, "SUCCESS", type2(get_data("tahun"),"tahun"), []) 

def get_data(field):
    return db.engine.execute(f'''SELECT {field}, COUNT(*) FROM dataset GROUP BY {field}''')


def type1(data):
    return{str(i[0]):i[1] for i in data}

def type2(data, other):
    return[{str(other):i[0], "count":i[1]} for i in data]