# API de livros

# GET, POST, PUT, DELETE

# Get - Buscar os dados dos livros(CREATE)
# Post - Adicionar novos livros(Read)
# Put - Atualizar informações dos livros(Update)
# Delete - Deletar informações dos livros(Delete)

# CRUD

# Create
# Read
# Update
# Delete

# vamos acessar nosso Endpoint
# E vamos acessar os PATH's do nosso Endpoint

# Path ou Rota
# Query Strings

# 200 300 400 500

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI(
    title="API de Livros",
    description="API para gerenciamento de livros",
    version="1.0.0",
    contact={ 
        "name":"Afranio Spohr",
        "email":"afraniorogerio@gmail.com"
        }
)

MEU_USUARIO = "admin"
MEU_SENHA = "admin"

security = HTTPBasic()

livros = []

meus_livrozinhos = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MEU_SENHA)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials
 
@app.get("/")
def hello_world():
    return {"Hello": " World!"}

@app.get("/Livros")
def get_livros(page : int = 1, limit : int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos!")   
    
    if not meus_livrozinhos:
        return {"message": "Não existe nenhum livro!"}
    
    start = (page - 1) * limit
    end = start + limit
   
    livros_paginados = [
       {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]} for id_livro, livro_data in meus_livrozinhos.items() if start <= id_livro < end
       for id_livro, livro_data in list(meus_livrozinhos.items())[start:end]
    ]

    return {
        "page": page,
        "limit": limit,
        "total": len(meus_livrozinhos),
        "livros": livros_paginados
    }

# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro
@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message": "O livro foi criado com sucesso!"}
    
# Dicionario = HashMap
# Chave -> Valor
   
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado!")
    else:
        # eu jogo essa informação dentro do meu antigo dicionário (o que é meus_livrozinhos)
        # e Nãooo dentro da REFERENCIA do antigo dicionario
        # Antigo dicionario != Referencia do antigo dicionario
        meus_livrozinhos [id_livro] = livro.dict()
        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livros(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]
        return {"message": "O livro foi deletado com sucesso!"}
    
# ACID
    