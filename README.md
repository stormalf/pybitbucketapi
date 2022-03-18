# pybitbucketapi
python3 module to call bitbucket api in command line or inside a module.  


## pybitbucketapi.py


usage: pybitbucketapi.py [-h] [-V] [-U USER] [-t TOKEN] [-u URL] [-a API] [-m METHOD] [-J JSONFILE] 

pybitbucketapi is a python3 program that call bitbucket apis in command line or imported as a module

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pybitbucketapi
    -U USER, --user USER  bitbucket user
    -t TOKEN, --token TOKEN
                            bitbucket token
    -u URL, --url URL     bitbucket url
    -a API, --api API     bitbucket api should start by a slash
    -m METHOD, --method METHOD
                            should contain one of the method to use : ['DELETE', 'GET', 'POST', 'PUT']
    -J JSONFILE, --jsonfile JSONFILE
                            json file needed for POST method



## examples 

GET /repositories : list all repositories

    python3 pybitbucketapi.py 

POST /workspaces/{workspace}/projects: create a new project

    python3 pybitbucketapi.py -a /workspaces/{workspace}/projects -m POST -J project.json

POST /repositories/{workspace}/{repo_slug} : create a new repository

    python3 pybitbucketapi.py -a /repositories/{workspace}/{repo_slug} -m POST -J repository.json

DELETE /workspaces/{workspace}/projects/{project_key}: delete the resource

    python3 pybitbucketapi.py -m DELETE -a /workspaces/{workspace}/projects/{project_key}

PUT /workspaces/{workspace}/projects/{project_key}: update the resource 

    python3 pybitbucketapi.py -m PUT -J {configuration-id}.json -a /workspaces/{workspace}/projects/{project_key}


## release notes

pybitbucketapi.py

1.0.0 initial version