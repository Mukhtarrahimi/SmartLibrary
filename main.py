import json

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

def menu():
    print("Welcome to the Smart Library")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Search Book")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice