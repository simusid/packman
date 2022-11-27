# Primary requrements
*  The system shall allow a user to manage a collection of data packages.
*  A package shall refer to a single top level object such as a folder, tarball, or s3 bucket
*  The system shall have a default set of metadata attributes that a user can enter.
 
# Major requirements
* The system shall allow a user to assign unique metadata attributes to a package.
* The system shall graph data growth based on the size and creation date of each package
* The system shall show a list of packages and indicate if the package is present 

# Minor requirements
* The system shall export a package (possibly to a tarball?)
* The system shall asynchronously move packages between systems (possibly via rsync?)
