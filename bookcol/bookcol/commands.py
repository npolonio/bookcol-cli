import click
import sqlite3
import json
import logging
import inquirer
import os
from .db import setup_database

logging.basicConfig(filename='books_collection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to save the collection to a .txt file
def save_to_txt(books, file_name):
    try:
        with open(file_name, 'w') as file:
            json.dump(books, file)
    except Exception as e:
        raise click.ClickException(f"Error saving to txt: {e}")


# Function to save the collection to the SQLite3 database
def save_to_db(books):
    setup_database()
    try:
        with sqlite3.connect('book_collection.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM books')
            for book in books:
                c.execute('INSERT INTO books (title, author, pages, read) VALUES (?, ?, ?, ?)',
                          (book['title'], book['author'], book['pages'], book['read']))
            conn.commit()
    except Exception as e:
        raise click.ClickException(f"Error saving to database: {e}")


# Click command group
@click.group()
def cli():
    pass


# Add command to add a book to the collection
@cli.command()
@click.option('-t', '--title', prompt='Title', type=str, help='Title of the book')
@click.option('-a', '--author', prompt='Author', type=str, help='Author of the book')
@click.option('-p', '--pages', prompt='Pages', type=int, help='Number of pages in the book')
@click.option('--read', is_flag=True, prompt='Have you finished reading this book?', help='Mark the book as read')
def add(title, author, pages, read):
    backup_collection()
    try:
        books = load_books()

        # Check if a book with the same title and author already exists
        existing_book = next((book for book in books if book['title'].lower() == title.lower() and book['author'].lower() == author.lower()), None)

        if existing_book:
            raise click.ClickException(f'A book with the title "{title}" and the same author already exists.')

        book = {'title': title, 'author': author, 'pages': pages, 'read': read}
        books.append(book)
        save_to_txt(books, 'book_collection.txt')
        save_to_db(books)

        message = f'Book "{title}" added successfully.'
        click.echo(message)
        logging.info(message)
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()



# Alter command to modify a book's attributes
@cli.command()
@click.option('-t', '--title', prompt='Title', type=str, help='Title of the book')
@click.option('-a', '--author', prompt='Author', type=str, help='Author of the book')
def alter(title, author):
    backup_collection()
    try:
        books = load_books()
        book_index = next((index for index, book in enumerate(books) if book['title'].lower() == title.lower() and book['author'].lower() == author.lower()), None)

        if book_index is not None:
            questions = [
                inquirer.Text('title', message='Title of the book', default=books[book_index]['title']),
                inquirer.Text('author', message='Author of the book', default=books[book_index]['author']),
                inquirer.Text('pages', message='Number of pages in the book', default=books[book_index]['pages']),
                inquirer.Confirm('read', message='Set the read status of the book', default=books[book_index]['read']),
            ]

            answers = inquirer.prompt(questions)

            if answers['title']:
                books[book_index]['title'] = answers['title']
            if answers['author']:
                books[book_index]['author'] = answers['author']
            if answers['pages']:
                books[book_index]['pages'] = answers['pages']
            if answers['read'] is not None:
                books[book_index]['read'] = answers['read']

            save_to_txt(books, 'book_collection.txt')
            save_to_db(books)

            message = f'Book "{title}" by {author} altered successfully.'
            click.echo(message)
            logging.info(message)
        else:
            click.echo(f'Book with title "{title}" and author "{author}" not found.')

    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()



# Delete command to remove a book from the collection
@cli.command()
@click.option('-t', '--title', prompt='Title', type=str, help='Title of the book')
@click.option('-a', '--author', prompt='Author', type=str, help='Author of the book')
def delete(title, author):
    backup_collection()
    try:
        books = load_books()
        matching_books = [book for book in books if book['title'].lower() == title.lower() and book['author'].lower() == author.lower()]

        if not matching_books:
            raise click.ClickException(f'Error: Book with title "{title}" and author "{author}" not found.')

        filtered_books = [book for book in books if book['title'].lower() != title.lower() or book['author'].lower() != author.lower()]
        save_to_txt(filtered_books, 'book_collection.txt')
        save_to_db(filtered_books)

        confirmation = click.confirm(f'Are you sure you want to delete the book with title "{title}" and author "{author}"?')

        if not confirmation:
            message = 'Deletion cancelled.'
            click.echo(message)
            logging.info(message)
            return

        message = f'Book "{title}" by {author} deleted successfully.'
        click.echo(message)
        logging.info(message)
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()


# Search command to find a book by title
@cli.command()
@click.option('-t', '--title', prompt='Title', help='Title of the book')
def search(title):
    try:
        books = load_books()
        matching_books = [book for book in books if title.lower() in book['title'].lower()]

        if not matching_books:
            raise click.ClickException(f'Error: Book with title "{title}" not found.')

        display_books(matching_books)
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()


# Display command to show all books in the collection
@cli.command()
def display():
    try:
        books = load_books()
        display_books(books)
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()


# Filter command to filter books by certain attributes
@cli.command()
def filter():
    try:
        books = load_books()
        filtered_books = books

        filter_choices = ['Author', 'Pages', 'Status']
        filter_question = inquirer.List('filter_by', message='Filter books by:', choices=filter_choices)
        filter_answer = inquirer.prompt([filter_question])

        if filter_answer['filter_by'] == 'Author':
            author = inquirer.Text('author', message='Enter author name:')
            author_answer = inquirer.prompt([author])
            filtered_books = [book for book in filtered_books if author_answer['author'].lower() in book['author'].lower()]

        elif filter_answer['filter_by'] == 'Pages':
            pages_options = ['Less than', 'Equal to', 'Greater than']
            pages_question = inquirer.List('pages_filter', message='Filter pages:', choices=pages_options)
            pages_answer = inquirer.prompt([pages_question])

            pages_value = click.prompt('Enter the number of pages:', type=int)

            if pages_answer['pages_filter'] == 'Less than':
                filtered_books = [book for book in filtered_books if book['pages'] < pages_value]
            elif pages_answer['pages_filter'] == 'Equal to':
                filtered_books = [book for book in filtered_books if book['pages'] == pages_value]
            elif pages_answer['pages_filter'] == 'Greater than':
                filtered_books = [book for book in filtered_books if book['pages'] > pages_value]

        elif filter_answer['filter_by'] == 'Status':
            status_options = ['Read', 'Not Read']
            status_question = inquirer.List('status_filter', message='Filter by status:', choices=status_options)
            status_answer = inquirer.prompt([status_question])

            if status_answer['status_filter'] == 'Read':
                filtered_books = [book for book in filtered_books if book['read']]
            elif status_answer['status_filter'] == 'Not Read':
                filtered_books = [book for book in filtered_books if not book['read']]

        display_books(filtered_books)

    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()


# Backup command to save the collection to a backup file
@cli.command()
def backup():
    backup_collection()
    message = 'Backup created successfully.'
    click.echo(message)
    menu()


# Restore command to restore the collection from a backup file
@cli.command()
def restore():
    try:
        if os.path.exists('book_backup.txt'):  # Check if the backup file exists
            backup_books = load_books('book_backup.txt')
            save_to_txt(backup_books, 'book_collection.txt')  # Save to the main collection file
            save_to_db(backup_books)

            message = 'Collection restored successfully.'
            click.echo(message)
            logging.info(message)
        else:
            raise click.ClickException('Backup file not found.')
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)

    menu()


#Function to save the previous state to another file, to be used only internally
def backup_collection():
    try:
        books = load_books()
        save_to_txt(books, 'book_backup.txt')  # Save to a backup file

        message = 'Backup created successfully.'
        logging.info(message)
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)


# Function to load books from the .txt file
def load_books(file_name='book_collection.txt'):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            if not content:
                return []
            books = json.loads(content)
    except FileNotFoundError:
        books = []
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Error decoding JSON from file: {e}")
    return books


# Function to display books
def display_books(books):
    for book in books:
        read_status = 'Read' if book['read'] else 'Not Read'
        click.echo(f'Title: {book["title"]}, Author: {book["author"]}, Pages: {book["pages"]}, Status: {read_status}')


def menu():
    questions = [
        inquirer.List('menu_choice',
                      message='Choose an action:',
                      choices=[
                          'Add a book',
                          'Alter a book',
                          'Delete a book',
                          'Search for a book',
                          'Display all books',
                          'Filter books',
                          'Backup collection',
                          'Restore collection',
                          'Exit'
                      ]),
    ]

    answer = inquirer.prompt(questions)

    if answer['menu_choice'] == 'Add a book':
        cli(['add'])
    elif answer['menu_choice'] == 'Alter a book':
        cli(['alter'])
    elif answer['menu_choice'] == 'Delete a book':
        cli(['delete'])
    elif answer['menu_choice'] == 'Search for a book':
        cli(['search'])
    elif answer['menu_choice'] == 'Display all books':
        cli(['display'])
    elif answer['menu_choice'] == 'Filter books':
        cli(['filter'])
    elif answer['menu_choice'] == 'Backup collection':
        cli(['backup'])
    elif answer['menu_choice'] == 'Restore collection':
        cli(['restore'])
    elif answer['menu_choice'] == 'Exit':
        click.echo('Goodbye!')
        exit()
