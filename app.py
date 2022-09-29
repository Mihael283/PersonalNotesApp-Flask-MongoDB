from flask import Flask
from flask_pymongo import PyMongo
from mongo_setup import MONGO_CONFIG,UPLOAD_FOLDER
from flask import request, Flask
from flask import request,Flask,render_template,redirect
import datetime
from werkzeug.utils import secure_filename
import os
from PIL import Image

app = Flask(__name__)
# For security reasons Mongo_config is hidden , here is an example of setup : "mongodb+srv://<username>:<password>@cluster0.ge03ld7.mongodb.net/?retryWrites=true&w=majority"
# you can check out the details in your cloud setup
app.config["MONGO_URI"] = MONGO_CONFIG
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)
print(mongo.db.notes)
@app.route('/')
def home():
    notes = list(mongo.db.notes.find({}).sort("createdAt",-1));
    return render_template("/pages/home.html",homeIsActive=True,addNoteIsActive=False,notes=notes)

@app.route('/add-note', methods = ['GET','POST'])
def addNote():
    if(request.method == "GET"):
        return render_template("pages/add-note.html",homeIsActive=False,addNoteIsActive=True)
    elif(request.method == "POST"):
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        createdAt = datetime.datetime.now()

        mongo.db.notes.insert_one({"title":title,"description":description,"createdAt":createdAt, "file":filepath })

        return redirect("/")

@app.route('/edit-note', methods=['GET','POST'])
def editNote():
    if(request.method == "GET"):
        return "<p>Edit note page</p>"
    elif (request.method == "POST"):
        return 0
        #logic for editing a note

@app.route('/delete-note', methods=['POST'])
def deleteNote():
    return 0
# logic for deleting a note

if __name__ == "__main__":
    app.run(debug=True)