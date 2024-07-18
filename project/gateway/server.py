"""Module"""

import os
import json
import gridfs
import pika
from flask import Flask ,request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util


app = Flask(__name__)
app.config['MONGO_URI'] ="mongodb://host.minikube.internal:27017/videos"
mongo = PyMongo(app)

fs = gridfs.GridFS(mongo.db)
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.route("/login",methods=["POST"])
def login():
    """Method"""
    token ,err = access.login(request)
    if not err:
        return token
    return err

@app.route('/upload',methods=["POST"])
def upload():
    """Method """

    access_ ,err = validate.token(request)
    access_ = json.loads(access_)
    if access_['admin']:
        if len(request.files) != 1:
            return "exactly 1 file is required"
        for _ , f in request.files.items():
            err =util.upload(f,fs,channel,access_)
            if err:
                return err
        return "success",200
    return "Not Authorized" ,401

@app.route('/download',methods=["GET"])
def download():
    """Method"""
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
