from enum import unique
from MySQLdb import Date
from flask import Flask, render_template, request,redirect, session, url_for , flash
from flask_sqlalchemy import SQLAlchemy 
import pandas as pd
import numpy as np
import os
import csv
import itertools, collections
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/abc_ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'ABC AI is an Artificial Intelligence based Company'    

class ObjectData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(100), unique=False)
    objects_detected = db.Column(db.String(300), unique=False)
    timestamp = db.Column(db.String(10), unique=False)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route("/", methods=['GET','POST'])
def uploadFiles():
    if request.method =='POST':

        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
        
        print(file_path)
        parseCSV(UPLOAD_FOLDER+'/data.csv')
        return render_template('index.html')

    return render_template('index.html')

@app.route('/results', methods=['GET','POST'])
def results():
    blank = []
    if request.method =='POST':
        stDate = request.form.get('stdate')
        fnDate = request.form.get('fndate')
        objdata = ObjectData.query.filter(ObjectData.timestamp.between(str(stDate), str(fnDate))).all()

        filename = "static/reports/" + stDate +" to " +fnDate + "- "+ str(time.time()) + ".csv"

        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            reportdat =[]
            for obj in objdata:
                dat = stringify(obj.objects_detected)
                reportdat.append(dat)
                
            linked = [item for sublist in reportdat for item in sublist]
            
            report = collections.Counter(linked)

            heads = report.keys()
            data = report.values()
            dater = [stDate,"from",fnDate]
            csvwriter.writerow(dater)
            csvwriter.writerow(heads)
            csvwriter.writerow(data)

        return render_template('index.html', stDate=stDate, fnDate=fnDate, objdata=objdata)
    return render_template('index.html')

def parseCSV(filePath):
        col_names = ["image_name","objects_detected","timestamp"]
        csvData = pd.read_csv(filePath,names=col_names, header=None)
        for i,row in csvData.iterrows():
            obj_data = ObjectData(image_name = row['image_name'], objects_detected = row['objects_detected'],timestamp = row['timestamp'])
            db.session.add(obj_data)
            db.session.commit()

def stringify(list):
    newlist = []
    strss = ""
    for i in list:
        if i ==",":
            newlist.append(strss)
            strss = ""
        elif i == list[len(list)-1]:
            strss += i
            newlist.append(strss)
        else:
            strss += i
    return newlist

if __name__ == '__main__':

    db.create_all()
    app.run(debug=True)