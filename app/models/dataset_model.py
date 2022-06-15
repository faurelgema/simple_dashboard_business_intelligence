from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime

class Dataset(db.Model):
    __tablename__ = "dataset"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement= True)
    judul = db.Column('judul', db.String(255), nullable=False)
    deskripsi = db.Column('deskripsi', db.Text)
    tahun = db.Column('tahun', db.Integer, nullable=False)
    topik = db.Column('topik', db.String(255), nullable=False)
    organisasi = db.Column('organisasi', db.String(255), nullable=False)
    cuid = db.Column('cuid', db.Integer, nullable=False)
    # muid = db.Column('muid', db.Integer, ForeignKey("user.id"), nullable=True)
    muid = db.Column('muid', db.Integer, nullable=True)
    created_at = db.Column('created_at', db.DateTime, default =datetime.utcnow)
    modified_at = db.Column('modified_at', db.DateTime, default =datetime.utcnow)
    # user_id = relationship("Users", backref="dataset")

    def __repr__(self) -> str:
        return f"<Judul {self.judul}>"
    

    def __repr__(self):
        return '<Dataset {}>'.format(self.name)

    def getById(id):
        return Dataset.query.filter_by(id=id).first()
    def getByJudul(title):
        return Dataset.query.filter_by(judul=title).first()
    def getByDeskripsi(desc):
        return Dataset.query.filter_by(deskripsi=desc).first()
    def getByYear(year):
        return Dataset.query.filter_by(tahun=year).first()
    def getByTopic(topic):
        return Dataset.query.filter_by(topik=topic).first()
    def getByOrg(org):
        return Dataset.query.filter_by(organisasi=org).first()
    def getByCuid(cr_id):
        return Dataset.query.filter_by(cuid=cr_id).first()
    def getByMdate(mdate):
        return Dataset.query.filter_by(muid=mdate).first()
    
    
