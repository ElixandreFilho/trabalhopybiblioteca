from models.livro import Livro

livros_file = "data/livros.csv"


def carregar_livros() -> list[Livro]:
    try:
        with open(livros_file, mode="r", newline='', encoding="utf-8") as file:
            linhas = file.readlines()[1:]  # Ignorar o cabeçalho
            livros = []
            for linha in linhas:
                valores = linha.strip().split(",")
                livros.append(
                    Livro(
                        id=int(valores[0]),
                        titulo=valores[1],
                        autor=valores[2],
                        edicao=valores[3],
                        preco=float(valores[4]),
                        editora=valores[5],
                        ano=int(valores[6]),
                        genero=valores[7],
                    )
                )
            return livros
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        return []


def salvar_livros(livro: Livro):
    with open(livros_file, mode="a", encoding="utf-8") as file:
        linha = f"{livro.id},{livro.titulo},{livro.autor},{livro.edicao},{livro.preco},{livro.editora},{livro.ano},{livro.genero}\n"
        file.write(linha)


def reescreve_livros(livros: list[Livro]):
    with open(livros_file, mode="w", encoding="utf-8") as file:
        # Escreve o cabeçalho
        file.write("id,titulo,autor,edicao,preco,editora,ano,genero\n")
        
        # Escreve cada livro no formato CSV
        for livro in livros:
            linha = f"{livro.id},{livro.titulo},{livro.autor},{livro.edicao},{livro.preco},{livro.editora},{livro.ano},{livro.genero}\n"
            file.write(linha)