from fastapi import FastAPI, Request, Response 
import requests 
import httpx
import asyncio
import logging
import os, json
from fastapi_utils.tasks import repeat_every

logger = logging.getLogger(__name__)
PING_INTERVAL = int(os.getenv('PING_INTERVAL', '30'))
NAME_STARTS_WITH = os.getenv('NAME_STARTS_WITH')
BASE_URL = os.getenv('BASE_URL')
NAMESPACE_NAME = os.getenv('NAMESPACE_NAME')
CLUSTER_ID = os.getenv('CLUSTER_ID')
APPLICATION_BEARER = os.getenv('BEARER')

AUTH_HEADER = {
    'accept': "application/json",
    'content-type': "application/json",
    'Connection': "keep-alive",
    'Authorization': "Bearer " + APPLICATION_BEARER
}


app = FastAPI()
@app.get("/")
async def first():
    return {"Hello": "World"}

@app.get("/ping/")
async def pong():
    resp = 'pong'
    return Response(resp)

async def get_data(url, AUTH_HEADER) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=AUTH_HEADER)
        return {'url': url, 'response' : response.text, 'status': response.status_code}


@app.on_event("startup")
@repeat_every(seconds=PING_INTERVAL, raise_exceptions = False)
async def pod():
    end_point = '/k8s/clusters/{cluster_id}/api/v1/namespaces/{namespace_name}/pods'
    end_point = end_point.format(
        cluster_id=CLUSTER_ID,
        namespace_name=NAMESPACE_NAME
    )
    namespaces_url = BASE_URL + end_point
    response = requests.get(namespaces_url, headers=AUTH_HEADER, verify=False)
    if response.status_code == 200:
        response_json = response.json()
        urls = []
        for item in response_json["items"]:
            if item['metadata']['name'].startswith(NAME_STARTS_WITH):
                urls.append(f"http://{item['status']['podIP']}/ping/")
        api_request_list = [get_data(url, AUTH_HEADER) for url in urls]
        responses = await asyncio.gather(*api_request_list)
        print(responses)
        logger.info(responses)