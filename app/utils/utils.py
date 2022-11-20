import json

PACKAGE_PATH="packages.json"
def getPackages():
    with open(PACKAGE_PATH) as fh:
        txt = fh.read()
        packages = json.loads(txt)
    fh.close()
    return packages 
        
def getPackage(id):
    with open(PACKAGE_PATH) as fh:
        txt = fh.read()
        packages = json.loads(txt)
    fh.close()
    for p in packages:
        if(p['id']==id):
            return p
    return None

def putPackages(p):
    with open(PACKAGE_PATH, "w") as fh:
        txt = json.dumps(p)
        fh.write(txt)
    fh.close()
    return

 
 
 