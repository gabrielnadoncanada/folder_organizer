import os
import shutil
import tkinter as tk
import datetime
import json
from tkinter import filedialog, messagebox, Checkbutton, IntVar, Listbox

def log_history(actions, folder_path):
    history_file = os.path.join(folder_path, 'organization_history.json')
    if not os.path.exists(history_file):
        with open(history_file, 'w') as file:
            json.dump([], file)

    with open(history_file, 'r+') as file:
        history_data = json.load(file)
        history_data.append(actions)
        file.seek(0)
        json.dump(history_data, file, indent=4)

def organize_files(folder_path, backup, exclude_files):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f not in exclude_files]
    actions = []
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(folder_path, 'backup', now)

    if backup:
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        for file in files:
            shutil.copy(os.path.join(folder_path, file), os.path.join(backup_path, file))
            actions.append({"action": "backup", "file": file, "src": os.path.join(folder_path, file), "dest": os.path.join(backup_path, file)})

    for file in files:
        extension = file.split('.')[-1]
        folder_path_ext = os.path.join(folder_path, extension)
        if not os.path.exists(folder_path_ext):
            os.mkdir(folder_path_ext)
        original_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path_ext, file)
        shutil.move(original_path, new_path)
        actions.append({"action": "move", "file": file, "src": original_path, "dest": new_path})

    log_history({"date": now, "actions": actions}, folder_path)
    messagebox.showinfo("Success", "Files have been organized!")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)
        update_history_listbox(folder_selected)

def update_history_listbox(folder_path):
    history_data = load_history(folder_path)
    lb.delete(0, tk.END)
    for item in history_data:
        lb.insert(tk.END, item['date'])

def load_history(folder_path):
    history_file = os.path.join(folder_path, 'organization_history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

def undo_specific_change(folder_path, date):
    history_data = load_history(folder_path)
    actions_to_undo = None
    for i, entry in enumerate(history_data):
        if entry["date"] == date:
            actions_to_undo = history_data.pop(i)
            break

    if actions_to_undo:
        for action in reversed(actions_to_undo["actions"]):
            if action["action"] == "move":
                shutil.move(action["dest"], action["src"])
        with open(os.path.join(folder_path, 'organization_history.json'), 'w') as file:
            json.dump(history_data, file, indent=4)
        messagebox.showinfo("Success", "Reverted to selected organization state!")
    else:
        messagebox.showinfo("Error", "No actions found for the selected date.")

def on_undo_button_click():
    folder_path = entry.get()
    if folder_path:
        selected_index = lb.curselection()
        if selected_index:
            selected_date = lb.get(selected_index)
            undo_specific_change(folder_path, selected_date)
        else:
            messagebox.showwarning("Warning", "Please select a date to undo.")
    else:
        messagebox.showwarning("Warning", "Please select a folder.")

def on_organize_button_click():
    folder_path = entry.get()
    if folder_path:
        exclude_files = ['folder_organizer_gui.py']
        organize_files(folder_path, backup_var.get(), exclude_files)
    else:
        messagebox.showwarning("Warning", "Please select a folder.")

app = tk.Tk()
app.title("Folder Organizer")

frame = tk.Frame(app)
frame.pack(pady=20, padx=20)

entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.RIGHT)

backup_var = IntVar()
backup_checkbox = Checkbutton(app, text="Backup files before organizing", variable=backup_var)
backup_checkbox.pack(pady=5)

organize_button = tk.Button(app, text="Organize", command=on_organize_button_click)
organize_button.pack(pady=10)

lb = Listbox(app, width=50, height=10)
lb.pack(pady=10)

undo_button = tk.Button(app, text="Undo Selected Organization", command=on_undo_button_click)
undo_button.pack(pady=10)

app.mainloop()
