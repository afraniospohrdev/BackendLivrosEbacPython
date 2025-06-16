# API de livros

# GET, POST, PUT, DELETE

# Get - Buscar os dados dos livros(CREATE)
# Post - Adicionar novos livros(Read)
# Put - Atualizar informações dos livros(Update)
# Delete - Deletar informações dos livros(Delete)

# CRUD

# vamos acessar nosso Endpoint
# E vamos acessar os PATH's do nosso Endpoint

# Path ou Rota
# Query Strings

# 200 300 400 500

from fastapi import FastAPI, HTTPException

app = FastAPI()

livros = []

meus_livrozinhos = {}

@app.get("/Livros")
def get_livros():
    if not meus_livrozinhos:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"Livros": meus_livrozinhos}

# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro
@app.post("/adiciona")
def post_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        meus_livrozinhos[id_livro] = {"nome_livro": nome_livro, "autor_livro": autor_livro, "ano_livro": ano_livro}
        return {"message": "O livro foi criado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado!")
    else:   
        if nome_livro:
            meu_livro["nome_livro"] = nome_livro
        if autor_livro:
            meu_livro["autor_livro"] = autor_livro
        if ano_livro:
            meu_livro["ano_livro"] = ano_livro

        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livros(id_livro: int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]
        return {"message": "O livro foi deletado com sucesso!"}
    