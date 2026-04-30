import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Movie Library")

# Поля ввода
tk.Label(root, text="Название:").grid(row=0, column=0)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1)

tk.Label(root, text="Жанр:").grid(row=1, column=0)
genre_entry = tk.Entry(root)
genre_entry.grid(row=1, column=1)

tk.Label(root, text="Год выпуска:").grid(row=2, column=0)
year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1)

tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0)
rating_entry = tk.Entry(root)
rating_entry.grid(row=3, column=1)
tree = ttk.Treeview(root, columns=("title", "genre", "year", "rating"), show='headings')
tree.heading("title", text="Название")
tree.heading("genre", text="Жанр")
tree.heading("year", text="Год")
tree.heading("rating", text="Рейтинг")
tree.grid(row=4, columnspan=2)

def add_movie():
    title = title_entry.get()
    genre = genre_entry.get()
    year = year_entry.get()
    rating = rating_entry.get()
    tree.insert("", "end", values=(title, genre, year, rating))

add_btn = tk.Button(root, text="Добавить фильм", command=add_movie)
add_btn.grid(row=5, column=0, columnspan=2)
def filter_movies():
    filter_genre = filter_genre_entry.get()
    filter_year = filter_year_entry.get()
    for item in tree.get_children():
        values = tree.item(item, "values")
        if (not filter_genre or filter_genre in values[1]) and (not filter_year or filter_year in values[2]):
            tree.item(item, tags='show')
        else:
            tree.item(item, tags='hide')
    tree.tag_configure('hide', hide=True)

# Поля фильтрации
tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0)
filter_genre_entry = tk.Entry(root)
filter_genre_entry.grid(row=6, column=1)

tk.Label(root, text="Фильтр по году:").grid(row=7, column=0)
filter_year_entry = tk.Entry(root)
filter_year_entry.grid(row=7, column=1)

filter_btn = tk.Button(root, text="Фильтровать", command=filter_movies)
filter_btn.grid(row=8, column=0, columnspan=2)
import json

def save_to_json():
    data = [tree.item(i)['values'] for i in tree.get_children()]
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json():
    try:
        with open('movies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for row in data:
            tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

save_btn = tk.Button(root, text="Сохранить в JSON", command=save_to_json)
save_btn.grid(row=9, column=0)
load_btn = tk.Button(root, text="Загрузить из JSON", command=load_from_json)
load_btn.grid(row=9, column=1)
def validate_inputs():
    title = title_entry.get()
    genre = genre_entry.get()
    year = year_entry.get()
    rating = rating_entry.get()

    if not title or not genre:
        return False, "Название и жанр обязательны"
    if not year.isdigit():
        return False, "Год должен быть числом"
    if not (rating.isdigit() and 0 <= int(rating) <= 10):
        return False, "Рейтинг должен быть числом от 0 до 10"
    return True, ""
