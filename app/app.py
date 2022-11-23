import uuid
import os, random, shutil
from flask import Flask, redirect, render_template, request, session
from flask_httpauth import HTTPDigestAuth
import matplotlib.pyplot as plt

import numpy as np

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
    count = len(packages)
    return render_template("index.html", packages=packages, schema=schema , count=count)

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

@app.route("/add_many")
def add_many():

    roots = [r'\\npa0humble\UUVData\UUV_Data\SAS_DATA\2022_SAS',
    r'\\npa0humble\UUVData\UUV_Data\SAS_DATA\2021_SAS',
    r'\\npa0humble\UUVData\UUV_Data\SAS_DATA\2020_SAS',
    r'\\npa0humble\UUVData\UUV_Data\SAS_DATA\2019_SAS',
    r'\\npa0humble\UUVData\UUV_Data\Elver\221104',
    r'\\npa0humble\UUVData\UUV_Data\Elver\221107'
    ]
    for root in roots:
        rootfiles  = os.listdir(root)
        rootdirs = [os.path.join(root, rf) for rf in rootfiles if os.path.isdir(os.path.join(root, rf))]
        for i, rd in enumerate(rootdirs):
            d={}
            d['id']=str(uuid.uuid4())
            d['name']=rootfiles[i]
            d['description']='test'
            d['location']=rd
            d['notes']=""
            packages = getPackages()
            packages.append(d)
            putPackages(packages)
    return redirect("/")

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

@app.route('/datagrowth')
def datagrowth():
    packages= getPackages()
    sizes=[]
    times=[]
    for p in packages:
        psize=[]
        path=p['location']
        for root, name, files in os.walk(path):
            for n in files:
                f =os.path.join(root, n)
                psize.append(os.path.getsize(f))
        sizes.append(sum(psize)//1000000)
        times.append(os.path.getctime(path))

    x = times
    y = sizes
    new_x, new_y = (list(n) for n in zip(*sorted(zip(x, y))))

    cumsum = np.cumsum(new_y)
    plt.figure(figsize=(12,10))
    plt.plot(new_x, cumsum)
    plt.grid(which='both')
    plt.title("Data Growth Over Time")
    plt.ylabel("Size of All Packages in MB")
    plt.savefig("app/static/datagrowth.jpg")
    return render_template("datagrowth.html",sizes=sizes, times=times)