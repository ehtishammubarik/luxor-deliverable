from fastapi import FastAPI, Request, Response 
import requests 
import os, json
from fastapi_utils.tasks import repeat_every


app = FastAPI()
@app.get("/")
async def first():
    return {"Hello": "World"}

@app.get("/ping/")
async def pong():
    resp = 'pong'
    return Response(resp) 
#@app.get("/pods/")
@app.on_event("startup")
@repeat_every(seconds=30)
async def pod():
    BASE_URL = os.getenv('BASE_URL')
    APPLICATION_BEARER = os.getenv('BEARER')
    AUTH_HEADER = {
        'accept': "application/json",
        'content-type': "application/json",
        'Connection': "keep-alive",
        'Authorization': "Bearer " + APPLICATION_BEARER
    }
    namespaces_url = BASE_URL + '/k8s/clusters/c-8cnzq/api/v1/namespaces/default/pods'
    response = requests.get(namespaces_url, headers=AUTH_HEADER, verify=False)
    if response.status_code == 200:
        response_json = response.json()
        ips = []
        for i in range(len(response_json["items"])):
            #if (response_json['items'][i]['metadata']['labels']['app.kubernetes.io/name']=="demo"):
            ip = response_json['items'][i]['status']['podIP']
            #url = "http://"+ip+"/ping/"
            url = "http://aceso-fastapi-schedule/ping/"
            #print("find me here")
            print(url)
            resp = requests.get(url, headers=AUTH_HEADER, verify=False)
            print("ip " + resp.text + resp.status_code)

@app.post("/scheduler")
async def scheduler(request: list):
    find = request
    endPoint = "/ping/"
    AUTH_HEADER = {
        'accept': "application/json",
        'content-type': "application/json",
        'Connection': "keep-alive"    }
    for x in find:
        url = str(x) + endPoint 
        response = requests.get(url, headers=AUTH_HEADER, verify=False)
        print(response.text)
    return Response(response.text)
    