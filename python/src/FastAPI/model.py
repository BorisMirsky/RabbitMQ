#from fastapi import FastAPI
from pydantic import BaseModel
#import aio_pika
#import json



class EmailBody(BaseModel):
    subject: str
    user_email: str
    message: str
