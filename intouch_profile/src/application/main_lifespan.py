import json
import pickle
from contextlib import asynccontextmanager

from aio_pika import IncomingMessage
from fastapi import FastAPI

from intouch_profile.src.infrastructure.broker.rabbit_handler import mq_handler, mq_rpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq_handler.mq_connect()
    mq_rpc.channel = mq_handler.channel
    await mq_handler.listen_queue(get, "registration")
    yield
    await mq_handler.mq_close_conn()


async def get(message: IncomingMessage):
    lst = []
    lst.append(message.body.decode("utf-8"))
    print(lst)
