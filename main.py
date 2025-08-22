import json
from random import choice

def add_book():
    book = {}
    book['title'] = input("Enter book title: ")
    book['author'] = input("Enter book author: ")
    book['year'] = input("Enter publication year: ")
    book['isbn'] = input("Enter ISBN number: ")
    
    with open('books.json', 'r+') as file:
        data = json.load(file)
        data['books'].append(book)
        file.seek(0)
        json.dump(data, file, indent=4)
    print("Book added successfully!")

def show_book():
    with open('books.json', 'r') as file:
        data = json.load(file)
        for book in data['books']:
            print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, ISBN: {book['isbn']}")
            
def search_book():
    def menu():
        print("How do you want to search the book?")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Year")
        print("4. Back to Main Menu")
        search_option = input("Enter your choice: ").lower()
        return search_option
    search_option = menu()
    with open('books.json', 'r') as file:
        data = json.load(file)
        if search_option == '1' or search_option == 'title':
            title = input("Enter book title: ")
            for book in data['books']:
                if book['title'].lower() == title.lower():
                    results = [book]
        elif search_option == '2' or search_option == 'author':
            author = input("Enter book author: ")
            for book in data['books']:
                if book['author'].lower() == author.lower():
                    results = [book]
        elif search_option == '3' or search_option == 'year':
            year = input("Enter publication year: ")
            for book in data['books']:
                if book['year'] == year:
                    results = [book]
        elif search_option == '4':
            return
        else:
            print("Invalid option.")
            return

        if results:
            for book in results:
                print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, ISBN: {book['isbn']}")
        else:
            print("No books found.")

def menu():
    print("Welcome to the Smart Library")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Search Book")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice