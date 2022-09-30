from flask import Flask
from flask_pymongo import PyMongo
from mongo_setup import MONGO_CONFIG,UPLOAD_FOLDER
from flask import request, Flask
from flask import request,Flask,render_template,redirect
import datetime
from werkzeug.utils import secure_filename
import os
from PIL import Image
from bson.objectid import ObjectId

app = Flask(__name__)
# For security reasons Mongo_config is hidden , here is an example of setup : "mongodb+srv://<username>:<password>@cluster0.ge03ld7.mongodb.net/?retryWrites=true&w=majority"
# you can check out the details in your cloud setup
app.config["MONGO_URI"] = MONGO_CONFIG
#Upload folder variable set to : 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)

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
        createdAt = datetime.datetime.now()
        file = request.files['file']

        if request.files['file'].filename == '' or 'static/images/':
            file = None
            filepath = None

        if file != None:
            filename = secure_filename(file.filename)
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
            except PermissionError:
                pass
            
        mongo.db.notes.insert_one({"title":title,"description":description,"createdAt":createdAt, "file":filepath })         
        
        #Redirect to home
        return redirect("/")

@app.route('/edit-note', methods=['GET','POST'])
def editNote():
    if request.method == "GET":
        noteId = request.args.get('form')
        note = dict(mongo.db.notes.find_one({"_id":ObjectId(noteId)}))

        return render_template('pages/edit-note.html',note=note)

    elif request.method == "POST":
        #get the data of the note
        noteId = request.form['_id']
        title = request.form['title']
        description = request.form['description']

        mongo.db.notes.update_one({"_id":ObjectId(noteId)},{"$set":{"title":title,"description":description}})

        return redirect("/")

@app.route('/delete-note', methods=['POST'])
def deleteNote():
    noteId = request.form['_id']
    mongo.db.notes.delete_one({ "_id": ObjectId(noteId)})
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)