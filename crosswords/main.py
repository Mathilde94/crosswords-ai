from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crosswords.controllers.routers import routers
from dotenv import load_dotenv

allowed_origins = [
    "*",  # webpack server
]

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
