from fastapi import APIRouter, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from typing import Optional
from fastapi.security import HTTPBearer
from user_jwt import validateToken
from bd.database import Session
from models.movie import Movie as MovieModel


routerMovie = APIRouter()

class Movie(BaseModel):
    id: Optional[int]= None
    title: str = Field(min_length=20, default="Titulo de la pelicula", max_length=100)
    director: str = Field(min_length=3, max_length=50)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director
        }

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data["email"] != 'johann@gmail.com':
            raise HTTPException(status_code=403, detail="Credencial invalid")


@routerMovie.get("/", tags=["inicio"])
def read_root():
    return HTMLResponse('<h2>Welcome to My FastAPI Application</h2><p>This is a simple FastAPI application.</p>')

@routerMovie.get("/movies", tags=["movies"], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    movies = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(movies))

@routerMovie.get("/movies/{id}", tags=["movies"], status_code=200)
def get_movie(id:int = Path(ge=1, le=5)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(data), status_code=200)

@routerMovie.get("/movies/", tags=["movies"])
def get_movies_by_director(director: str = Query(min_length=3, max_length=50)):
    db = Session()
    movies = db.query(MovieModel).filter(MovieModel.director == director).all()
    if not movies:
        return JSONResponse(content={"message": "No movies found for this director"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@routerMovie.post("/movies", tags=["movies"])
def create_movie(movie: Movie ):
    db = Session()
    movies = MovieModel(**movie.dict())
    db.add(movies)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)


@routerMovie.put("/movies/{id}", tags=["movies"])
def update_movie(id:int, movie: Movie):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    data.title = movie.title
    data.director = movie.director
    db.commit()
    db.refresh(data)
    
    return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)


@routerMovie.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)