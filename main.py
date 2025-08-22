import json
import os

if not os.path.exists("books.json"):
    with open("books.json", "w") as f:
        json.dump({"books": []}, f, indent=4)


def load_data():
    with open("books.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open("books.json", "w") as f:
        json.dump(data, f, indent=4)


def add_book():
    data = load_data()
    book = {}
    book["id"] = str(len(data["books"]) + 1)  
    book["title"] = input("Enter book title: ")
    book["author"] = input("Enter book author: ")
    book["year"] = input("Enter publication year: ")
    book["isbn"] = input("Enter ISBN number: ")

    data["books"].append(book)
    save_data(data)

    print("Book added successfully!")


def show_books():
    data = load_data()
    if not data["books"]:
        print("No books found.")
        return
    print("\n--- All Books ---")
    for book in data["books"]:
        print(
            f"ID: {book['id']}, Title: {book['title']}, "
            f"Author: {book['author']}, Year: {book['year']}, ISBN: {book['isbn']}"
        )
    print("-----------------\n")


def search_book():
    print("How do you want to search the book?")
    print("1. By Title")
    print("2. By Author")
    print("3. By Year")
    print("4. Back to Main Menu")
    option = input("Enter choice: ")

    data = load_data()
    results = []

    if option == "1":
        title = input("Enter title: ")
        results = [b for b in data["books"] if b["title"].lower() == title.lower()]
    elif option == "2":
        author = input("Enter author: ")
        results = [b for b in data["books"] if b["author"].lower() == author.lower()]
    elif option == "3":
        year = input("Enter year: ")
        results = [b for b in data["books"] if b["year"] == year]
    elif option == "4":
        return
    else:
        print("Invalid option.")
        return

    if results:
        print("\n--- Search Results ---")
        for book in results:
            print(
                f"ID: {book['id']}, Title: {book['title']}, "
                f"Author: {book['author']}, Year: {book['year']}, ISBN: {book['isbn']}"
            )
        print("----------------------\n")
    else:
        print("No books found.")


def delete_book():
    show_books()
    book_id = input("Enter ID of the book to delete: ")

    data = load_data()
    new_books = [b for b in data["books"] if b["id"] != book_id]

    if len(new_books) != len(data["books"]):
        confirm = input("Are you sure to delete? (y/n): ").lower()
        if confirm == "y":
            data["books"] = new_books
            save_data(data)
            print("Book deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("No book found with this ID.")


def edit_book():
    show_books()
    book_id = input("Enter ID of the book to edit: ")

    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            print("\nWhat do you want to edit?")
            print("1. Title")
            print("2. Author")
            print("3. Year")
            print("4. ISBN")
            print("5. Cancel")
            choice = input("Enter choice: ")

            if choice == "1":
                book["title"] = input("Enter new title: ")
            elif choice == "2":
                book["author"] = input("Enter new author: ")
            elif choice == "3":
                book["year"] = input("Enter new year: ")
            elif choice == "4":
                book["isbn"] = input("Enter new ISBN: ")
            elif choice == "5":
                return
            else:
                print("Invalid option.")
                return

            save_data(data)
            print("Book updated successfully!")
            return

    print("No book found with this ID.")


def menu():
    while True:
        print("Welcome to the Smart Library")
        print("1. Add Book")
        print("2. Show All Books")
        print("3. Search Book")
        print("4. Delete Book")
        print("5. Edit Book")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            show_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            edit_book()
        elif choice == "6":
            print(" Exiting... Bye!")
            break
        else:
            print("Invalid choice, try again.")


menu()
