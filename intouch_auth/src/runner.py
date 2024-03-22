from fastapi import FastAPI

import uvicorn

from presentation import main_router

app = FastAPI()

app.include_router(router=main_router)


if __name__ == "__main__":
    uvicorn.run("runner:app", port=1222, reload=True)
