# PackMan

A "package manager" to support long term, large scale data management.  Fundamental concepts are 

* A "package" is a collection of directories and datafiles with a single top level root.  A package is a specified location on a filesystem (NFS, smb, local storage, or S3). 

* Users enter metadata relevant to each data package

* Metrics can be different for each package 

# Installation
Clone the repo and cd to packman.   Start the server for development:

flask --app app/app.py --debug run 

If using authentication (ref https://flask-httpauth.readthedocs.io/en/latest/ )  start with run --cert=adhoc

Note this requires that pyopenssl is installed

