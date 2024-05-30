import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

# Список для зберігання тасків
tasks = []

# Функція для зчитування завдань з файлу
def load_tasks(filename="tasks.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                tasks.append(line.strip())
    except FileNotFoundError:
        pass  # Якщо файл не знайдено, просто пропускаємо (список tasks залишиться порожнім)

# Функція для запису завдань у файл
def save_tasks(filename="tasks.txt"):
    with open(filename, "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Функція для додавання нового таску
def add_task(event=None):
    task = task_entry.get()
    if task:
        tasks.append(task)
        update_task_list()
        task_entry.delete(0, tk.END)
        save_tasks()  # Зберігаємо завдання після додавання
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

# Функція для видалення таску
def remove_task(event=None):
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = task_listbox.get(selected_task_index)
        tasks.remove(task)
        update_task_list()
        save_tasks()  # Зберігаємо завдання після видалення
    else:
        messagebox.showwarning("Warning", "You must select a task to remove.")

# Функція для оновлення відображення списку тасків
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Створення головного вікна
root = tk.Tk()
root.title("Task Tracker")
root.configure(bg='#1f201f')  # Задаємо колір фону

# Встановлення шрифту Nunito
default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="Nunito", size=12)
root.option_add("*Font", default_font)
root.option_add("*Foreground", "white")  # Задаємо білий колір шрифту
root.option_add("*Background", "#1f201f")  # Задаємо колір фону для всіх віджетів

# Елементи інтерфейсу
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)
task_entry.bind("<Return>", add_task)  # Додаємо завдання при натисканні Enter

task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(pady=10)
task_listbox.bind("<Double-Button-1>", remove_task)  # Видаляємо завдання при подвійному кліку

# Завантаження завдань з файлу при запуску програми
load_tasks()
update_task_list()

# Запуск головного циклу програми
root.mainloop()
