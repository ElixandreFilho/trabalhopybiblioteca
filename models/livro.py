from pydantic import BaseModel
from typing import Union

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    edicao: str
    preco: float
    editora: Union[str, None] = None
    ano: int
    genero: str