import os
import zipfile
import hashlib
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from http import HTTPStatus
from models.livro import Livro
from services.livro_service import carregar_livros, salvar_livros, reescreve_livros

app = FastAPI()

livros: list[Livro] = carregar_livros()

livros_file = "data/livros.csv"
output_dir = "outputs"
Path(output_dir).mkdir(parents=True, exist_ok=True)

@app.get("/")
def home():
    return {"msg": "Bem vindo à API de Biblioteca"}

@app.get("/livros/comprimir", response_class=FileResponse)
def compactar_csv():
    
    if not os.path.exists(livros_file):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Arquivo livros.csv não encontrado.")
    
    zip_file_path = os.path.join(output_dir, "livros.zip")
    
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(livros_file, arcname=os.path.basename(livros_file))
    
    return FileResponse(zip_file_path, media_type="application/zip", filename="livros.zip")



@app.get("/livros/hash")
def hash_csv():

    if not os.path.exists(livros_file):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Arquivo livros.csv não encontrado.")
    
    sha256_hash = hashlib.sha256()
    
    with open(livros_file, "rb") as file:
        while chunk := file.read(8192):
            sha256_hash.update(chunk)
    
    return {"hash": sha256_hash.hexdigest()}


@app.get("/livros/quantidade")
def contar_livros():
    return {"quantidade": len(livros)}


@app.get("/livros/{livro_id}")
def ler_livro(livro_id: int) -> Livro:
    for livro in livros:
        if livro.id == livro_id:
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")


@app.get("/livros/")
def listar_livros() -> list[Livro]:
    return livros


@app.post("/livros/", status_code=HTTPStatus.CREATED)
def adicionar_livro(livro: Livro) -> Livro:
    if any(livro_atual.id == livro.id for livro_atual in livros):
        raise HTTPException(status_code=400, detail="ID já existe.")
    livros.append(livro)
    salvar_livros(livro)
    return livro


@app.put("/livro/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizado: Livro) -> Livro:
    for indice, livro_atual in enumerate(livros):
        if livro_atual.id == livro_id:
            if livro_atualizado.id != livro_id:
                livro_atualizado.id = livro_id
            livros[indice] = livro_atualizado
            reescreve_livros(livros)
            return livro_atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")


@app.delete("/livro/{livro_id}")
def remover_livro(livro_id: int):
    for livro in livros:
        if livro.id == livro_id:
            livros.remove(livro)
            reescreve_livros(livros)
            return {"msg": "Livro removido com sucesso!"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")
