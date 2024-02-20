from fastapi import FastAPI
from crosswords.controllers.routers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
