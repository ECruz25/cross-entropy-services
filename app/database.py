from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import pymongo
import pickle
import time

DATABASE_URL = 'postgres://jkvztitm:rbbVDY8O51ZPFFA5o50aAkW78BxHaxUV@raja.db.elephantsql.com:5432/jkvztitm'
MONGO_DATABASE_URL = 'mongodb://root:root123@ds353378.mlab.com:53378/cross-entropy?authSource=cross-entropy&retryWrites=false'


engine = create_engine(DATABASE_URL, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)


def shutdown_db_session():
    db_session.remove()


def load_saved_model_from_db(model_type, user):
    db = 'cross-entropy'
    dbconnection = 'predictive_models' 
    json_data = {}
    myclient = pymongo.MongoClient(MONGO_DATABASE_URL)
    mydb = myclient[db]
    mycon = mydb[dbconnection]
    data = mycon.find({'type': model_type, 'user': user })
    for i in data:
        json_data = i
    pickled_model = json_data['model']
    return pickle.loads(pickled_model)

def load_models_by_user(user):
    db = 'cross-entropy'
    dbconnection = 'predictive_models' 
    json_data = {}
    models = []
    myclient = pymongo.MongoClient(MONGO_DATABASE_URL)
    mydb = myclient[db]
    mycon = mydb[dbconnection]
    data = mycon.find({ 'user': user })
    for i in data:
        i['model'] = ''
        i['_id'] = ''
        json_data = i
        models.append(json_data)
    return models


def save_model_to_db(model, model_type, user, model_details):
    db = 'cross-entropy'
    dbconnection = 'predictive_models' 
    pickled_model = pickle.dumps(model)
    myclient = pymongo.MongoClient(MONGO_DATABASE_URL)
    mydb = myclient[db]
    mycon = mydb[dbconnection]
    mycon.delete_many({'type': model_type, 'user': user })
    info = mycon.insert_one({ 'model': pickled_model, 'type': model_type, 'created_time': time.time(), 'user': user, 'model_details': model_details })