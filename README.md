# 📚 bookcol

**bookcol** é uma aplicação de linha de comando (CLI) para gerenciar uma coleção de livros.  
Permite adicionar, alterar, remover, pesquisar, exibir, filtrar, fazer backup e restaurar livros da coleção, com persistência em arquivos `.txt` e em um banco de dados **SQLite3**.

---

## 🚀 Funcionalidades

- Adicionar livros (com título, autor, número de páginas e status de leitura).
- Alterar informações de livros já cadastrados.
- Excluir livros da coleção.
- Pesquisar livros pelo título.
- Exibir toda a coleção cadastrada.
- Filtrar livros por autor, número de páginas ou status (lido/não lido).
- Criar backup da coleção.
- Restaurar coleção a partir de backup.
- Persistência de dados em:
  - Arquivo `book_collection.txt`
  - Banco de dados `book_collection.db` (SQLite3)

---

## 📦 Instalação

Você pode instalar o **bookcol** de duas formas: usando **pip** ou **Poetry**.

### Usando pip

```bash
git clone https://github.com/seu-usuario/bookcol.git
cd bookcol
pip install .
````

### Usando Poetry

```bash
git clone https://github.com/seu-usuario/bookcol.git
cd bookcol
poetry install
```

---

## 🖥️ Uso

Após a instalação, você poderá executar o comando principal diretamente pelo terminal:

```bash
bookcol
```

Isso abrirá o menu interativo, permitindo escolher entre as opções:

* Add a book
* Alter a book
* Delete a book
* Search for a book
* Display all books
* Filter books
* Backup collection
* Restore collection
* Exit

Também é possível chamar comandos diretamente. Exemplos:

```bash
bookcol add
bookcol search --title "Dom Casmurro"
bookcol display
bookcol delete --title "Dom Casmurro" --author "Machado de Assis"
```

---

## 📂 Estrutura do Projeto

```
bookcol/
│── __init__.py
│── __main__.py        # Ponto de entrada do CLI
│── commands.py        # Implementação dos comandos (add, alter, delete, etc.)
│── db.py              # Configuração e setup do banco SQLite
│
├── setup.py           # Configuração para instalação via setuptools
├── pyproject.toml     # Configuração para instalação via Poetry
├── book_collection.txt # Arquivo de persistência principal
├── book_backup.txt     # Arquivo de backup da coleção
└── book_collection.db  # Banco de dados SQLite3
```

---

## 🛠️ Testando no modo desenvolvimento

Se quiser testar o projeto sem instalar globalmente, use:

```bash
# Usando Poetry
poetry run bookcol

# Usando Python diretamente
python -m bookcol
```

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**.
Sinta-se livre para usar, modificar e compartilhar.

---
