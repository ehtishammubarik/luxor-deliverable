from fastapi import FastAPI, Request, Response 
import requests


app = FastAPI()
@app.get("/")
async def first():
    return {"Hello": "World"}

@app.get("/ping/")
async def pong():
    resp = 'pong'
    return Response(resp) 
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


    kubectl get pods --selector=app.kubernetes.io/name=demo --output=jsonpath={.items[*].status.podIP}
    