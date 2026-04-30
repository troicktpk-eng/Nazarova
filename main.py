import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

# Путь к файлу истории
HISTORY_FILE = 'history.json'

# Предопределённые задачи
predefined_tasks = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Закончить проект", "type": "работа"},
    {"name": "Позвонить другу", "type": "личное"},
    {"name": "Помыть посуду", "type": "быт"},
]

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение истории
def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title('Random Task Generator')

        self.history = load_history()

        # Виды задач для фильтрации
        self.types = ['Все'] + sorted(set(task['type'] for task in predefined_tasks))
        self.current_filter = 'Все'

        # Создаем виджеты
        self.create_widgets()

    def create_widgets(self):
        # Кнопка генерации
        self.btn_generate = tk.Button(self.root, text='Сгенерировать задачу', command=self.generate_task)
        self.btn_generate.pack(pady=10)

        # Метка для отображения выбранной задачи
        self.label_task = tk.Label(self.root, text='Задача появится здесь', font=('Arial', 14))
        self.label_task.pack(pady=10)

        # Фильтр по типу задач
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text='Фильтр по типу:').pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value='Все')
        self.combo_filter = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=self.types, state='readonly')
        self.combo_filter.pack(side=tk.LEFT)
        self.combo_filter.bind('<<ComboboxSelected>>', self.apply_filter)

        # История задач
        tk.Label(self.root, text='История задач:').pack()
        self.listbox_history = tk.Listbox(self.root, width=50, height=10)
        self.listbox_history.pack(pady=5)
        self.update_history_list()

        # Добавление новой задачи
        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=10)

        self.entry_new_task = tk.Entry(add_frame, width=30)
        self.entry_new_task.pack(side=tk.LEFT, padx=5)

        self.combo_type_task = ttk.Combobox(add_frame, values=[t for t in self.types if t != 'Все'], state='readonly')
        self.combo_type_task.pack(side=tk.LEFT, padx=5)
        self.combo_type_task.set('учёба')  # Значение по умолчанию

        self.btn_add = tk.Button(add_frame, text='Добавить задачу', command=self.add_task)
        self.btn_add.pack(side=tk.LEFT, padx=5)

    def generate_task(self):
        # Выбор задач по фильтру
        filtered_tasks = self.get_filtered_tasks()
        if not filtered_tasks:
            messagebox.showinfo('Нет задач', 'Нет задач для текущего фильтра.')
            return
        task = random.choice(filtered_tasks)
        task_text = f"{task['name']} ({task['type']})"
        self.label_task.config(text=task_text)
        # Добавляем в историю
        self.history.append(task)
        save_history(self.history)
        self.update_history_list()

    def get_filtered_tasks(self):
        if self.current_filter == 'Все':
            return predefined_tasks
        return [task for task in predefined_tasks if task['type'] == self.current_filter]

    def apply_filter(self, event=None):
        self.current_filter = self.filter_var.get()
        self.update_history_list()

    def update_history_list(self):
        self.listbox_history.delete(0, tk.END)
        for task in self.history:
            if self.current_filter == 'Все' or task['type'] == self.current_filter:
                self.listbox_history.insert(tk.END, f"{task['name']} ({task['type']})")

    def add_task(self):
        name = self.entry_new_task.get().strip()
        type_task = self.combo_type_task.get()
        if not name:
            messagebox.showwarning('Ошибка', 'Поле задачи не должно быть пустым.')
            return
        new_task = {"name": name, "type": type_task}
        predefined_tasks.append(new_task)
        # Обновляем список фильтров
        if type_task not in self.types:
            self.types.append(type_task)
            self.combo_filter['values'] = self.types
        self.entry_new_task.delete(0, tk.END)
        messagebox.showinfo('Успех', 'Задача добавлена.')

if __name__ == '__main__':
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
