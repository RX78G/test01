import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import List
import uuid

DATA_FILE = Path(__file__).with_name('todo_data.json')

@dataclass
class Task:
    id: str
    title: str
    desc: str = ''
    due: str = ''
    priority: int = 1
    completed: bool = False


def load_tasks() -> List[Task]:
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
        return [Task(**t) for t in data]
    return []


def save_tasks(tasks: List[Task]) -> None:
    DATA_FILE.write_text(
        json.dumps([asdict(t) for t in tasks], ensure_ascii=False, indent=2),
        encoding='utf-8')


class TodoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title('To-Do App')
        self.tasks: List[Task] = load_tasks()
        self.filter_var = tk.StringVar(value='All')
        self.search_var = tk.StringVar()
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        frm = ttk.Frame(self.root)
        frm.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        in_frame = ttk.LabelFrame(frm, text='Add Task')
        in_frame.pack(fill=tk.X)
        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.due_var = tk.StringVar()
        self.pri_var = tk.IntVar(value=1)
        ttk.Label(in_frame, text='Title').grid(row=0, column=0, sticky='w')
        ttk.Entry(in_frame, textvariable=self.title_var).grid(row=0, column=1, sticky='ew')
        ttk.Label(in_frame, text='Desc').grid(row=1, column=0, sticky='w')
        ttk.Entry(in_frame, textvariable=self.desc_var).grid(row=1, column=1, sticky='ew')
        ttk.Label(in_frame, text='Due').grid(row=2, column=0, sticky='w')
        ttk.Entry(in_frame, textvariable=self.due_var).grid(row=2, column=1, sticky='ew')
        ttk.Label(in_frame, text='Priority').grid(row=3, column=0, sticky='w')
        ttk.Spinbox(in_frame, from_=1, to=5, textvariable=self.pri_var, width=5).grid(row=3, column=1, sticky='w')
        ttk.Button(in_frame, text='Add', command=self.add_task).grid(row=4, column=1, sticky='e', pady=5)
        in_frame.columnconfigure(1, weight=1)
        search_frame = ttk.Frame(frm)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.OptionMenu(search_frame, self.filter_var, 'All', 'All', 'Active', 'Completed', command=lambda _e: self.refresh()).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text='Search', command=self.refresh).pack(side=tk.LEFT)
        self.tree = ttk.Treeview(frm, columns=('due', 'pri'), show='headings', selectmode='browse')
        self.tree.heading('due', text='Due')
        self.tree.heading('pri', text='Pri')
        self.tree.pack(fill=tk.BOTH, expand=True)
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text='Toggle Done', command=self.toggle_done).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text='Delete', command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='Save', command=self.save).pack(side=tk.RIGHT)

    def add_task(self) -> None:
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning('Validation', 'Title is required')
            return
        task = Task(id=str(uuid.uuid4()), title=title, desc=self.desc_var.get(), due=self.due_var.get(), priority=self.pri_var.get())
        self.tasks.append(task)
        self.clear_inputs()
        self.refresh()

    def clear_inputs(self) -> None:
        self.title_var.set('')
        self.desc_var.set('')
        self.due_var.set('')
        self.pri_var.set(1)

    def get_filtered(self) -> List[Task]:
        q = self.search_var.get().lower()
        flt = self.filter_var.get()
        tasks = self.tasks
        if flt == 'Active':
            tasks = [t for t in tasks if not t.completed]
        elif flt == 'Completed':
            tasks = [t for t in tasks if t.completed]
        if q:
            tasks = [t for t in tasks if q in t.title.lower() or q in t.desc.lower()]
        return tasks

    def refresh(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.get_filtered():
            mark = '✓' if t.completed else ''
            self.tree.insert('', 'end', iid=t.id, values=(t.due, t.priority), text=mark)
            self.tree.item(t.id, text=mark)
            self.tree.set(t.id, 'due', t.due)
            self.tree.set(t.id, 'pri', t.priority)
            self.tree.item(t.id, values=(t.due, t.priority))
            self.tree.item(t.id, open=True, tags=('done' if t.completed else ''))
        self.tree.tag_configure('done', foreground='gray')

    def get_selected(self) -> Task | None:
        sel = self.tree.selection()
        if not sel:
            return None
        id_ = sel[0]
        for t in self.tasks:
            if t.id == id_:
                return t
        return None

    def toggle_done(self) -> None:
        t = self.get_selected()
        if t:
            t.completed = not t.completed
            self.refresh()

    def delete_task(self) -> None:
        t = self.get_selected()
        if t:
            self.tasks.remove(t)
            self.refresh()

    def save(self) -> None:
        save_tasks(self.tasks)
        messagebox.showinfo('Saved', 'Tasks saved')


if __name__ == '__main__':
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()
