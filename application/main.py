from fastapi import FastAPI, Request, Response 
import requests 
import os, json


app = FastAPI()
@app.get("/")
async def first():
    return {"Hello": "World"}

@app.get("/ping/")
async def pong():
    resp = 'pong'
    return Response(resp) 
@app.get("/pods/")
async def pod():
    BASE_URL = os.getenv('BASE_URL')
    APPLICATION_DOMAIN = os.getenv('APPLICATION_DOMAIN')
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
            ips.insert(i,response_json['items'][i]['status']['podIP'])
        return(ips)

    return Response(ips)
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
    