import uuid
import os
from flask import Flask, redirect, render_template, request, session
from utils.utils import *

app = Flask(__name__)
app.secret_key="packman"
schema = ( "name", "description", "location", "notes")

@app.route("/",  methods=['GET' ])
def index():
    packages = getPackages()
    return render_template("index.html", packages=packages )

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
    for root, name, files in os.walk(path):
        for n in files:
            fnames.append(os.path.join(root, n))
            sizes.append(os.path.getsize(os.path.join(root,n)))
    size = sum(sizes)//1000000
    status = "There are {} files with a total size of {} MB".format(len(fnames), size)
  
    return render_template('status.html', status=status)

