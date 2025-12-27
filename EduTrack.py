import tkinter as tk
from tkinter import messagebox
import csv
import os

FILE_NAME = "students.csv"

# ---------- File Setup ----------
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            csv.writer(file).writerow(["ID", "Name", "Department"])

# ---------- Helpers ----------
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_dept.delete(0, tk.END)
    status.set("🧹 Fields cleared")

def get_all_students():
    with open(FILE_NAME, "r") as file:
        return list(csv.reader(file))

def update_count():
    count = len(get_all_students()) - 1
    count_label.config(text=f"Total Students: {count}")

# ---------- Core Features ----------
def add_student():
    sid, name, dept = entry_id.get(), entry_name.get(), entry_dept.get()

    if not sid or not name or not dept:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    for row in get_all_students()[1:]:
        if row[0] == sid:
            messagebox.showerror("Duplicate ID", "Student ID already exists!")
            return

    with open(FILE_NAME, "a", newline="") as file:
        csv.writer(file).writerow([sid, name, dept])

    status.set("✅ Student added successfully")
    clear_fields()
    view_students()

def view_students():
    text_area.delete("1.0", tk.END)
    for row in get_all_students()[1:]:
        text_area.insert(tk.END, f"🆔 {row[0]}   👤 {row[1]}   🎓 {row[2]}\n")
    update_count()

def search_student():
    sid = entry_id.get()
    for row in get_all_students()[1:]:
        if row[0] == sid:
            entry_name.delete(0, tk.END)
            entry_dept.delete(0, tk.END)
            entry_name.insert(0, row[1])
            entry_dept.insert(0, row[2])
            status.set("🔍 Student found")
            return
    messagebox.showinfo("Not Found", "Student not found!")

def update_student():
    sid, name, dept = entry_id.get(), entry_name.get(), entry_dept.get()
    updated = False
    students = get_all_students()

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        for row in students:
            if row and row[0] == sid:
                writer.writerow([sid, name, dept])
                updated = True
            else:
                writer.writerow(row)

    if updated:
        status.set("✏️ Student updated successfully")
        view_students()
    else:
        messagebox.showerror("Error", "Student ID not found!")

def delete_student():
    sid = entry_id.get()
    if not sid:
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure to delete this student?"):
        return

    deleted = False
    students = get_all_students()

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        for row in students:
            if row and row[0] == sid:
                deleted = True
            else:
                writer.writerow(row)

    if deleted:
        status.set("🗑️ Student deleted")
        clear_fields()
        view_students()
    else:
        messagebox.showerror("Error", "Student ID not found!")

# ---------- UI ----------
create_file()
root = tk.Tk()
root.title("Student Management System")
root.geometry("720x580")
root.configure(bg="#0f172a")

tk.Label(root, text="🎓 Student Management System",
         font=("Segoe UI", 20, "bold"),
         bg="#0f172a", fg="white").pack(pady=10)

card = tk.Frame(root, bg="#1e293b", padx=25, pady=25)
card.pack(pady=10)

def label(txt, r):
    tk.Label(card, text=txt, bg="#1e293b", fg="white",
             font=("Segoe UI", 11)).grid(row=r, column=0, sticky="w", pady=8)

label("Student ID", 0)
entry_id = tk.Entry(card, width=32, font=("Segoe UI", 11))
entry_id.grid(row=0, column=1)

label("Name", 1)
entry_name = tk.Entry(card, width=32, font=("Segoe UI", 11))
entry_name.grid(row=1, column=1)

label("Department", 2)
entry_dept = tk.Entry(card, width=32, font=("Segoe UI", 11))
entry_dept.grid(row=2, column=1)

btn_frame = tk.Frame(root, bg="#0f172a")
btn_frame.pack(pady=12)

def button(txt, cmd, col, color):
    tk.Button(btn_frame, text=txt, width=13, command=cmd,
              bg=color, fg="white", cursor="hand2",
              font=("Segoe UI", 10, "bold")).grid(row=0, column=col, padx=6)

button("➕ Add", add_student, 0, "#22c55e")
button("🔍 Search", search_student, 1, "#3b82f6")
button("✏️ Update", update_student, 2, "#eab308")
button("🗑️ Delete", delete_student, 3, "#ef4444")
button("🧹 Clear", clear_fields, 4, "#64748b")

text_area = tk.Text(root, height=8, width=80,
                    bg="#f8fafc", font=("Consolas", 10))
text_area.pack(pady=10)

count_label = tk.Label(root, text="", bg="#0f172a",
                       fg="white", font=("Segoe UI", 10))
count_label.pack()

status = tk.StringVar(value="Ready")
tk.Label(root, textvariable=status,
         bg="#020617", fg="white", anchor="w").pack(fill="x", side="bottom")

view_students()
root.mainloop()
