import asyncio
from fastapi import FastAPI, Request, Header
import uvicorn
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Dict,Union
from pydantic import BaseModel

class Req(BaseModel):
    text : str

app = FastAPI()

def test(txt2imgreq: Req, sd_req_id: Union[str, None] = Header(default=None)) -> Dict:
    print(f'sd_req_id is {sd_req_id}')
    return {'sd_req_id':sd_req_id}


app.add_api_route('/test', test, methods=["POST"])


if __name__ == '__main__':
    # uvicorn.run(app=app,host='0.0.0.0',port=8111)
    d1 = {'a':1}
    d2 = d1.copy()
    d2['a'] = 2
    print(d2)