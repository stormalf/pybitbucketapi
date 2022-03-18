#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
import requests
from json import loads as jsonload
import argparse
import os


'''
pybitbucketapi.py is to be used by other python modules to automate bitbucket api usage.
it could be called in command line.
See bitbucket official references to get the correct Api URL and method to use :
    https://developer.atlassian.com/bitbucket/api/2/reference/

Only basic authentication is supported for now with app password.

Examples : default /repositories
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

    
'''

__version__ = "1.0.1"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT"]
URL = "https://api.bitbucket.org/2.0"
NO_CONTENT = 204

def pybitbucketApiVersion():
    return f"pybitbucketapi version : {__version__}"


class bitbucketApi():
    def __init__(self, api, method, url, user, token, jsonfile):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.user = user
        self.token = bitbucketApi.crypted(token)


    def __repr__(self):
        return (f"bitbucketApi api: {self.api}, method: {self.method}, url: {self.url}")

    #return the encrypted password/token
    @classmethod
    def crypted(cls, token):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(token.encode())
        cls.token = ciphered_text
        return cls.token

    #return the decrypted password/token
    @classmethod
    def decrypted(cls, token):
        cls.token = token
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.token)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    #execute the bitbucket api using a temp instance
    @staticmethod
    def runbitbucketApi(api, method, url, user, token, json):
        if token == None:
            response = jsonload('{"message": "Error : token missing!"}')
            return response 
        tempbitbucket = bitbucketApi(api, method, url, user, token, json)
        response = tempbitbucket.bitbucketAuthentication()
        tempbitbucket = None
        return response       


    #call private function
    def bitbucketAuthentication(self):
        response = self.__bitbucketTokenAuth()
        return response

    #internal function that formats the url and calls the bitbucket apis
    def __bitbucketTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        auth =  (self.user, bitbucketApi.decrypted(self.token))  
        response = self.__bitbucketDispatch(apiurl, auth, header)
        return response

    #internal function that calls the requests
    def __bitbucketDispatch(self, apiurl, auth, header):
        response = "{}"        
        try:
            if self.method == "POST":
                contents = open(self.json, 'r')
                response = requests.post(apiurl, auth=auth, headers=header, data=contents)
                contents.close()
            elif self.method == "GET":
                response = requests.get(apiurl, auth=auth, headers=header)
            elif self.method == "PUT":
                if self.json == '':
                    response = requests.put(apiurl, auth=auth,  headers=header)
                else:
                    contents = open(self.json, 'r')                    
                    response = requests.put(apiurl, auth=auth,  headers=header, data=contents)
                    contents.close()
            elif self.method == "DELETE":
                #raise Exception("DELETE not implemented yet")
                response = requests.delete(apiurl, auth=auth, headers=header)  
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)   
        if response.status_code == NO_CONTENT:
            response = "{}"
        else:            
            response = response.json()
        return response

def pybitbucketapi(args):
    message = ''
    if args.user == '':
        user = os.environ.get("BITBUCKET_USER")
    else:
        user = args.user  
    if args.token == '':
        itoken = os.environ.get("BITBUCKET_TOKEN")
    else:
        itoken = args.token               
    if args.api == '' and args.jsonfile == '':
        api="/repositories"
    else:
        api=args.api    
    if args.url == '':
        iurl = URL
    else:
        iurl = args.url        
    method = args.method     
    if "POST" in method and args.jsonfile == "":
        print("Json file required with method POST!")
        return
    json = args.jsonfile        
    message= bitbucketApi.runbitbucketApi(api=api, method=method, url=iurl, user=user, token=itoken, json=json ) 
    return message


if __name__== "__main__":
    helpmethod = f"should contain one of the method to use : {str(ALLOWED_METHODS)}"
    parser = argparse.ArgumentParser(description="pybitbucketapi is a python3 program that call bitbucket apis in command line or imported as a module")
    parser.add_argument('-V', '--version', help='Display the version of pybitbucketapi', action='version', version=pybitbucketApiVersion())
    parser.add_argument('-U', '--user', help='bitbucket user', default='', required=False)    
    parser.add_argument('-t', '--token', help='bitbucket token', default='', required=False)    
    parser.add_argument('-u', '--url', help='bitbucket url', default='', required=False)    
    parser.add_argument('-a', '--api', help='bitbucket api should start by a slash', default='', required=False)    
    parser.add_argument('-m', '--method', help = helpmethod, default="GET", required=False)   
    parser.add_argument('-J', '--jsonfile', help='json file needed for POST method', default='', required=False)
    args = parser.parse_args()
    message = pybitbucketapi(args)
    print(message)