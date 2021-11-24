from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic.errors import DateTimeError
from typing import Text,Optional
from datetime import datetime
from uuid import uuid4 as uuid #Generar un identificador unico

app = FastAPI() #Creamos la app para correrla 

class Post(BaseModel):
    id:Optional[str]
    title:str
    autor:str
    contenido:Text
    create_at: datetime = datetime.now()
    publicado_at: Optional[datetime]
    publicado:bool =  False



posts = []

@app.get('/')
def leer_raiz():
        return {"Bienvenido": "Bienvenido a mis APIs"}

@app.get('/posts')
def get_publicaciones():
        return posts

@app.post('/posts')
def save_publicacion(publicacion:Post): #Le decimos que el tipo de dato a recibir es tipo Post
    publicacion.id = str(uuid())
    posts.append(publicacion.dict())# dict-convertirlo-Diccionario append-añadir-lista
    return posts[-1] #devolver el ultimo item de la listas

@app.get('/posts/{publicacion_id}')
def get_publicacion(publicacion_id:str):
    for publicacion in posts:
        if publicacion["id"] == publicacion_id:
            return publicacion
    raise HTTPException(status_code=404,detail="Post Not Found")

@app.delete('/post/{publicacion_id}')
def eliminar_post(publicacion_id:str):
    for index, publicacion in enumerate(posts):
        if publicacion["id"] == publicacion_id:
            posts.pop(index) #POP quita de la lista el elemento index
            return "Publicacion eliminada"
    raise HTTPException(status_code=404, detail="Post Not Found")

@app.put('/posts/{publicacion_id}')
def actualizar_publicacion(publicacion_id:str, newPublicacion:Post):
    for index, post in enumerate(posts):
        if post["id"] == publicacion_id:
            posts[index]["title"] = newPublicacion.title
            posts[index]["contenido"] = newPublicacion.contenido
            posts[index]["autor"] = newPublicacion.autor
            return {"message":"TODO SALIO BIEN"}
    raise HTTPException(status_code=404, detail="Post Not Found")




