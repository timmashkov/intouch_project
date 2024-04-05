from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.broker.rabbit_handler import mq_handler, mq_rpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq_handler.mq_connect()
    mq_rpc.channel = mq_handler.channel
    yield
    await mq_handler.mq_close_conn()
