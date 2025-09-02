# 📚 bookcol  

[🇧🇷 Português](#-versão-em-português) | [🇺🇸 English](#-english-version)  

---

## 🇧🇷 Versão em português

O **bookcol** é uma aplicação de linha de comando (CLI) para gerenciar uma coleção de livros.  
Permite adicionar, alterar, remover, pesquisar, exibir, filtrar, fazer backup e restaurar livros da coleção, com persistência em arquivos `.txt` e em um banco de dados **SQLite3**.  

---

### 🚀 Funcionalidades  

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

### 📦 Instalação  

Você pode instalar o **bookcol** de duas formas: usando **pip** ou **Poetry**.  

#### Usando pip  

```bash
git clone https://github.com/seu-usuario/bookcol.git
cd bookcol
pip install .
````

#### Usando Poetry

```bash
git clone https://github.com/seu-usuario/bookcol.git
cd bookcol
poetry install
```

---

### 🖥️ Uso

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

### 📂 Estrutura do Projeto

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

### 🛠️ Testando no modo desenvolvimento

Se quiser testar o projeto sem instalar globalmente, use:

```bash
# Usando Poetry
poetry run bookcol

# Usando Python diretamente
python -m bookcol
```

---

### 📜 Licença

Este projeto foi desenvolvido apenas para fins acadêmicos e de estudo.
Sinta-se livre para usar, modificar e compartilhar.

---

## 🇺🇸 English Version

**Bookcol** is a command-line interface (CLI) application for managing a book collection.
It allows you to add, edit, remove, search, display, filter, back up, and restore books in the collection, with persistence in `.txt` files and an **SQLite3** database.

---

### 🚀 Features

* Add books (with title, author, number of pages, and reading status).
* Edit information of already registered books.
* Delete books from the collection.
* Search for books by title.
* Display the entire registered collection.
* Filter books by author, number of pages, or status (read/unread).
* Create a collection backup.
* Restore collection from backup.
* Data persistence in:

  * File `book_collection.txt`
  * Database `book_collection.db` (SQLite3)

---

### 📦 Installation

You can install **bookcol** in two ways: using **pip** or **Poetry**.

#### Using pip

```bash
git clone https://github.com/seu-usuario/bookcol.git
cd bookcol
pip install .
```

#### Using Poetry

```bash
git clone https://github.com/seu-usuario/bookcol.git
cd bookcol
poetry install
```

---

### 🖥️ Usage

After installation, you can run the main command directly from the terminal:

```bash
bookcol
```

This will open the interactive menu, allowing you to choose from the options:

* Add a book
* Alter a book
* Delete a book
* Search for a book
* Display all books
* Filter books
* Backup collection
* Restore collection
* Exit

You can also call commands directly. Examples:

```bash
bookcol add
bookcol search --title "Dom Casmurro"
bookcol display
bookcol delete --title "Dom Casmurro" --author "Machado de Assis"
```

---

### 📂 Project Structure

```
bookcol/
│── __init__.py
│── __main__.py        # CLI entry point
│── commands.py        # Commands implementation (add, alter, delete, etc.)
│── db.py              # SQLite setup
│
├── setup.py           # Setup for setuptools installation
├── pyproject.toml     # Poetry installation config
├── book_collection.txt # Main persistence file
├── book_backup.txt     # Backup file
└── book_collection.db  # SQLite3 database
```

---

### 🛠️ Testing in Development Mode

If you want to test the project without installing it globally, use:

```bash
# Using Poetry
poetry run bookcol

# Using Python directly
python -m bookcol
```

---

### 📜 License

This project was developed for academic and study purposes only.
Feel free to use, modify, and share it.

---
