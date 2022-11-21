import uuid
import os, random, shutil
from flask import Flask, redirect, render_template, request, session
from flask_httpauth import HTTPDigestAuth

from utils.utils import *

app = Flask(__name__)
app.secret_key="packman"  # for session
app.config['SECRET_KEY'] = 'secret key here'  # for https

users = {
    "gary": "password",
}
auth = HTTPDigestAuth() 

schema = ( "name", "description", "location", "notes")

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route("/",  methods=['GET' ])
@auth.login_required
def index():
    packages = getPackages()
    return render_template("index.html", packages=packages, schema=schema )

@app.route("/add/", methods=['GET','POST'])
def add():     
    if(request.method=="POST"):
        d={}
        d['id']=str(uuid.uuid4())
      
        for k,v in request.form.items():
            print(k,v)
            d[k]=v
        packages = getPackages()
        packages.append(d)
        putPackages(packages)
        return redirect("/")

    return render_template("add.html", schema=schema)

@app.route("/delete/<id>")
def delete(id):
    packages = getPackages()
    keep = []
    for p in packages:
        if (p['id']!=id):
            keep.append(p)
    putPackages(keep)
    return redirect("/")

@app.route("/edit/<id>", methods=['GET'])
@app.route("/edit/", methods=['POST'])
def edit(id=None):
    if(request.method=="POST"):
        d={}
        for k,v in request.form.items():
            d[k]=v
            print("*****  " , k, d[k])
        packages = getPackages()
        newpackages=[]
        for p in packages:
            if(p['id']!= d['id']):
                newpackages.append(p)
        newpackages.append(d)
        putPackages(newpackages)
        return redirect('/')

    p = getPackage(id)
    return render_template("edit.html", schema=schema, package=p)

@app.route("/status/<id>")
def status(id):
    package = getPackage(id)
    path = package['location']
    fnames = []
    sizes = []
    jpgs =[]
    audio = []
    try:
        os.mkdir("app/static/{}".format(id))
    except:
        pass
    for root, name, files in os.walk(path):
        for n in files:
            f =os.path.join(root, n)
            fnames.append(f)
            sizes.append(os.path.getsize(f))
            if(".jpg" in f):
                jpgs.append(f)
            if(".wav" in f or "*.mp3" in f):
                audio.append(f)

    size = sum(sizes)//1000000
    status = "There are {} files with a total size of {} MB".format(len(fnames), size)
    random.shuffle(jpgs)
    jpg_samples = []
    audio_samples=[]
    for j in jpgs[:6]:
        dest = "app/static/{}/{}".format(id,os.path.split(j)[-1] )
        shutil.copy(j, dest)
        jpg_samples.append(dest[3:])  # a hack to trim off the "app", keep the /

    for a in audio[:4]:
        dest = "app/static/{}/{}".format(id,os.path.split(a)[-1] )
        shutil.copy(a, dest)
        audio_samples.append(dest[3:])
    return render_template('status.html', 
            status=status, 
            image_samples=jpg_samples,
            audio_samples=audio_samples)
