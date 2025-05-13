from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from user_jwt import crearToken
from bd.database import  engine, Base
from routers.movie import routerMovie
from routers.user import routerUser
import os
import uvicorn

app = FastAPI(
    title="My FastAPI Application",
    description="This is a simple FastAPI application.",
    version="1.0.0",
)
app.include_router(routerMovie)
app.include_router(routerUser)


Base.metadata.create_all(bind=engine)



####  endpoins para movies
@app.get("/", tags=["inicio"])
def read_root():
    return HTMLResponse('<h2>Welcome to My FastAPI Application</h2><p>This is a simple FastAPI application.</p>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0", port=port)