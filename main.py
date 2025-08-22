import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "books.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"books": []}, f, indent=4)


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def next_id(books):
    ids = [int(b.get("id", 0)) for b in books if str(b.get("id", "")).isdigit()]
    return str(max(ids) + 1 if ids else 1)


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Library")
        self.geometry("900x560")
        self.minsize(820, 520)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure(bg="#0f172a")
        self._build_layout()
        self._build_table()
        self._load()

    def _build_layout(self):
        self.header = ttk.Frame(self)
        self.header.pack(side=tk.TOP, fill=tk.X, padx=16, pady=(16, 8))

        self.title_label = ttk.Label(
            self.header, text="Smart Library Manager", font=("Segoe UI", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT)

        self.search_frame = ttk.Frame(self.header)
        self.search_frame.pack(side=tk.RIGHT)
        self.search_by = ttk.Combobox(
            self.search_frame,
            state="readonly",
            values=["title", "author", "year", "isbn", "id"],
            width=10,
        )
        self.search_by.set("title")
        self.search_entry = ttk.Entry(self.search_frame, width=28)
        self.search_btn = ttk.Button(
            self.search_frame, text="Search", command=self.search
        )
        self.clear_btn = ttk.Button(
            self.search_frame, text="Clear", command=self.clear_search
        )
        self.search_by.grid(row=0, column=0, padx=(0, 6))
        self.search_entry.grid(row=0, column=1, padx=6)
        self.search_btn.grid(row=0, column=2, padx=6)
        self.clear_btn.grid(row=0, column=3)

        self.body = ttk.Frame(self)
        self.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))

        self.sidebar = ttk.Frame(self.body, width=180)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        self.sidebar.pack_propagate(False)

        self.btn_add = ttk.Button(
            self.sidebar, text="Add Book", command=self.open_add_dialog
        )
        self.btn_edit = ttk.Button(
            self.sidebar, text="Edit Selected", command=self.open_edit_dialog
        )
        self.btn_delete = ttk.Button(
            self.sidebar, text="Delete Selected", command=self.delete_selected
        )
        self.btn_refresh = ttk.Button(self.sidebar, text="Refresh", command=self._load)
        for i, w in enumerate(
            [self.btn_add, self.btn_edit, self.btn_delete, self.btn_refresh]
        ):
            w.pack(fill=tk.X, pady=6)

        self.table_frame = ttk.Frame(self.body)
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status = ttk.Label(self, anchor=tk.W, padding=(12, 6))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _build_table(self):
        cols = ("id", "title", "author", "year", "isbn")
        self.tree = ttk.Treeview(
            self.table_frame, columns=cols, show="headings", selectmode="extended"
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.heading("id", text="ID", command=lambda: self.sort_by("id", int))
        self.tree.heading(
            "title", text="Title", command=lambda: self.sort_by("title", str)
        )
        self.tree.heading(
            "author", text="Author", command=lambda: self.sort_by("author", str)
        )
        self.tree.heading(
            "year", text="Year", command=lambda: self.sort_by("year", int)
        )
        self.tree.heading(
            "isbn", text="ISBN", command=lambda: self.sort_by("isbn", str)
        )

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("title", width=260)
        self.tree.column("author", width=180)
        self.tree.column("year", width=80, anchor=tk.CENTER)
        self.tree.column("isbn", width=160, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        hsb = ttk.Scrollbar(
            self.table_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self._sort_state = {c: False for c in ("id", "title", "author", "year", "isbn")}

    def _load(self):
        data = load_data()
        self.books = data.get("books", [])
        for i in self.tree.get_children():
            self.tree.delete(i)
        for b in self.books:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    b.get("id", ""),
                    b.get("title", ""),
                    b.get("author", ""),
                    b.get("year", ""),
                    b.get("isbn", ""),
                ),
            )
        self.update_status()

    def update_status(self):
        total = len(self.books)
        sel = len(self.tree.selection())
        self.status.config(text=f"Total: {total}    Selected: {sel}")

    def sort_by(self, col, cast):
        rows = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            rows = [(cast(v) if v != "" else v, k) for v, k in rows]
        except Exception:
            rows = [(v, k) for v, k in rows]
        rev = self._sort_state[col] = not self._sort_state[col]
        rows.sort(reverse=rev)
        for index, (_, k) in enumerate(rows):
            self.tree.move(k, "", index)
        self.update_status()

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self._load()

    def search(self):
        key = self.search_entry.get().strip()
        field = self.search_by.get()
        if not key:
            self._load()
            return
        data = load_data()
        books = data.get("books", [])
        res = []
        for b in books:
            v = str(b.get(field, ""))
            if field in ("title", "author"):
                if key.lower() in v.lower():
                    res.append(b)
            else:
                if key == v:
                    res.append(b)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for b in res:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    b.get("id", ""),
                    b.get("title", ""),
                    b.get("author", ""),
                    b.get("year", ""),
                    b.get("isbn", ""),
                ),
            )
        self.books = res
        self.update_status()

    def open_add_dialog(self):
        BookDialog(self, title="Add Book", on_save=self.add_book).show()

    def add_book(self, payload):
        data = load_data()
        payload["id"] = next_id(data.get("books", []))
        data["books"].append(payload)
        save_data(data)
        self._load()

    def open_edit_dialog(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select a book to edit.")
            return
        item = self.tree.item(sel[0])
        current = {
            "id": item["values"][0],
            "title": item["values"][1],
            "author": item["values"][2],
            "year": item["values"][3],
            "isbn": item["values"][4],
        }
        BookDialog(
            self, title="Edit Book", initial=current, on_save=self.edit_book
        ).show()

    def edit_book(self, payload):
        data = load_data()
        for b in data.get("books", []):
            if str(b.get("id")) == str(payload.get("id")):
                b.update(
                    {
                        "title": payload.get("title", b.get("title")),
                        "author": payload.get("author", b.get("author")),
                        "year": payload.get("year", b.get("year")),
                        "isbn": payload.get("isbn", b.get("isbn")),
                    }
                )
                break
        save_data(data)
        self._load()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select one or more books to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected book(s)?"):
            return
        ids = {self.tree.item(i)["values"][0] for i in sel}
        data = load_data()
        data["books"] = [
            b for b in data.get("books", []) if str(b.get("id")) not in ids
        ]
        save_data(data)
        self._load()


class BookDialog(tk.Toplevel):
    def __init__(self, master, title, on_save, initial=None):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.on_save = on_save
        self.initial = initial or {}
        self._build()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build(self):
        pad = 10
        frm = ttk.Frame(self, padding=16)
        frm.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        ttk.Label(frm, text="Title").grid(
            row=0, column=0, sticky="w", padx=pad, pady=(0, 6)
        )
        ttk.Label(frm, text="Author").grid(
            row=1, column=0, sticky="w", padx=pad, pady=6
        )
        ttk.Label(frm, text="Year").grid(row=2, column=0, sticky="w", padx=pad, pady=6)
        ttk.Label(frm, text="ISBN").grid(row=3, column=0, sticky="w", padx=pad, pady=6)
        self.ent_title = ttk.Entry(frm, width=36)
        self.ent_author = ttk.Entry(frm, width=36)
        self.ent_year = ttk.Entry(frm, width=36)
        self.ent_isbn = ttk.Entry(frm, width=36)
        self.ent_title.grid(row=0, column=1, padx=pad, pady=(0, 6))
        self.ent_author.grid(row=1, column=1, padx=pad, pady=6)
        self.ent_year.grid(row=2, column=1, padx=pad, pady=6)
        self.ent_isbn.grid(row=3, column=1, padx=pad, pady=6)
        if self.initial:
            self.ent_title.insert(0, self.initial.get("title", ""))
            self.ent_author.insert(0, self.initial.get("author", ""))
            self.ent_year.insert(0, self.initial.get("year", ""))
            self.ent_isbn.insert(0, self.initial.get("isbn", ""))
        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(
            side=tk.RIGHT, padx=(0, 6)
        )
        ttk.Button(btns, text="Save", command=self._submit).pack(side=tk.RIGHT)

    def _submit(self):
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        year = self.ent_year.get().strip()
        isbn = self.ent_isbn.get().strip()
        if not title or not author or not year or not isbn:
            messagebox.showwarning("Warning", "All fields are required.")
            return
        if not year.isdigit():
            messagebox.showwarning("Warning", "Year must be numeric.")
            return
        payload = {"title": title, "author": author, "year": year, "isbn": isbn}
        if self.initial.get("id"):
            payload["id"] = self.initial["id"]
        self.on_save(payload)
        self.destroy()


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
