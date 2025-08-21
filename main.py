from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.users import login_user

app = FastAPI( 
    title='Aprendiendo FastAPI',
    description='API primeros pasos',
    version='0.0.1',
    
)

app.include_router(routerMovie)
app.include_router(login_user)

Base.metadata.create_all(bind=engine)



@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola Mundo!</h2>')

