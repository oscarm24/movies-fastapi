from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.movie_model import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerMovie = APIRouter()

#Primero se importa lo siguiente from pydantic import BaseModel,from typing import Optional
# Se importa Field en pydantic para validación
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Título de la película',min_length=5, max_length=100)
    overview: str = Field(default='Descripción de la película',min_length=15, max_length=200)
    year: str = Field(default='2023')
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Categoría',min_length=3, max_length=100)
    
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'oscar@gmail.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db= Session()
    data = db.query(ModelMovie).all()
    #return movies
    return JSONResponse(content=jsonable_encoder(data)) # Se agrega la respuesta del del JSONResponse
    

# Parámetros de ruta, validación de parámetros de agrega el =path en este caso para un rango en el id
# Se agrega Path, HTTPException en la importacion de FastAPI
@routerMovie.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail='Película no encontrada')
    return JSONResponse(status_code=200, content=jsonable_encoder(data))  

# Param Query, validación de paran query de agrega el =Query y en rango de longitud en este caso
# Se agrega Query en la importancion de FastAPI
@routerMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron películas en esa categoría")
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


# Se crea esquema de validación, se crea la clase BaseModel y se recibe un objeto de tipo movie en la función 
@routerMovie.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.refresh(newMovie)
    return {"message": "Se ha cargado una nueva película", "movie": newMovie}

# Metodos PUT y DELETE
@routerMovie.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id:int, movie:Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail='Película no encontrada')
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    raise HTTPException(status_code=404, detail='Se ha modificado la película')
        
@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movies(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail='Película no encontrada')
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message':'Se ha eliminado la película', 'data': jsonable_encoder(data)})