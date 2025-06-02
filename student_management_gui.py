import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f2f5")

        # Initialize data
        self.data_file = "data/students.json"
        self.students = []
        self.load_students()

        # Create main frames
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

        # Start with student list view
        self.show_student_list()

    def load_students(self):
        """Load students from JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.students = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading student data: {str(e)}")
            self.students = []

    def save_students(self):
        """Save students to JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.students, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving student data: {str(e)}")

    def create_header(self):
        """Create the header section"""
        header = tk.Frame(self.root, bg="#1a73e8", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Student Management System",
            font=("Helvetica", 20, "bold"),
            bg="#1a73e8",
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=20, pady=10)

    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = tk.Frame(self.root, bg="#ffffff", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Style for sidebar buttons
        style = ttk.Style()
        style.configure(
            "Sidebar.TButton",
            font=("Helvetica", 11),
            padding=10,
            width=20
        )

        # Navigation buttons
        ttk.Button(
            sidebar,
            text="Student List",
            style="Sidebar.TButton",
            command=self.show_student_list
        ).pack(pady=5, padx=10)

        ttk.Button(
            sidebar,
            text="Add Student",
            style="Sidebar.TButton",
            command=self.show_add_student
        ).pack(pady=5, padx=10)

        ttk.Button(
            sidebar,
            text="Search Students",
            style="Sidebar.TButton",
            command=self.show_search
        ).pack(pady=5, padx=10)

    def create_main_content(self):
        """Create the main content area"""
        self.main_content = tk.Frame(self.root, bg="#f0f2f5")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clear_main_content(self):
        """Clear all widgets from main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_student_list(self):
        """Display the list of all students"""
        self.clear_main_content()

        # Create tree view
        columns = ("Roll No.", "Name", "Age", "Class", "Section", "Address")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings")

        # Configure column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_content, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Insert data
        for student in self.students:
            tree.insert("", tk.END, values=(
                student["roll_number"],
                student["name"],
                student["age"],
                student["class"],
                student.get("section", ""),
                student.get("address", "")
            ))

        # Add action buttons
        action_frame = tk.Frame(self.main_content, bg="#f0f2f5")
        ttk.Button(
            action_frame,
            text="Edit",
            command=lambda: self.edit_student(tree.selection())
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            action_frame,
            text="Delete",
            command=lambda: self.delete_student(tree.selection())
        ).pack(side=tk.LEFT, padx=5)

        # Pack widgets
        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        action_frame.pack(pady=10)

    def show_add_student(self):
        """Show the add student form"""
        self.clear_main_content()

        # Create form frame
        form_frame = tk.Frame(self.main_content, bg="white", padx=20, pady=20)
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH)

        # Form fields
        tk.Label(form_frame, text="Roll Number:", bg="white").grid(row=0, column=0, pady=5, sticky=tk.W)
        roll_entry = ttk.Entry(form_frame)
        roll_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Name:", bg="white").grid(row=1, column=0, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Age:", bg="white").grid(row=2, column=0, pady=5, sticky=tk.W)
        age_entry = ttk.Entry(form_frame)
        age_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Class:", bg="white").grid(row=3, column=0, pady=5, sticky=tk.W)
        class_entry = ttk.Entry(form_frame)
        class_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Section:", bg="white").grid(row=4, column=0, pady=5, sticky=tk.W)
        section_entry = ttk.Entry(form_frame)
        section_entry.grid(row=4, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Address:", bg="white").grid(row=5, column=0, pady=5, sticky=tk.W)
        address_entry = ttk.Entry(form_frame)
        address_entry.grid(row=5, column=1, pady=5, padx=5)

        def save_student():
            # Validate inputs
            if not roll_entry.get() or not name_entry.get() or not age_entry.get():
                messagebox.showerror("Error", "Roll Number, Name, and Age are required!")
                return

            try:
                age = int(age_entry.get())
                if age < 5 or age > 30:
                    if not messagebox.askyesno("Confirm", "Age seems unusual. Continue anyway?"):
                        return
            except ValueError:
                messagebox.showerror("Error", "Age must be a number!")
                return

            # Create student record
            student = {
                "roll_number": roll_entry.get(),
                "name": name_entry.get(),
                "age": age,
                "class": class_entry.get(),
                "section": section_entry.get(),
                "address": address_entry.get()
            }

            # Check for duplicate roll number
            if any(s["roll_number"] == student["roll_number"] for s in self.students):
                messagebox.showerror("Error", "Roll Number already exists!")
                return

            self.students.append(student)
            self.save_students()
            messagebox.showinfo("Success", "Student added successfully!")
            self.show_student_list()

        ttk.Button(
            form_frame,
            text="Save Student",
            command=save_student
        ).grid(row=6, column=0, columnspan=2, pady=20)

    def show_search(self):
        """Show the search interface"""
        self.clear_main_content()

        # Create search frame
        search_frame = tk.Frame(self.main_content, bg="white", padx=20, pady=20)
        search_frame.pack(pady=20, padx=20, fill=tk.X)

        # Search fields
        tk.Label(search_frame, text="Search by:", bg="white").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar(value="roll")
        ttk.Radiobutton(
            search_frame,
            text="Roll Number",
            variable=search_var,
            value="roll"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            search_frame,
            text="Name",
            variable=search_var,
            value="name"
        ).pack(side=tk.LEFT, padx=5)

        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Results tree view
        columns = ("Roll No.", "Name", "Age", "Class", "Section", "Address")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        def perform_search():
            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)

            search_text = search_entry.get().lower()
            if not search_text:
                return

            # Filter students
            results = []
            if search_var.get() == "roll":
                results = [s for s in self.students if search_text in s["roll_number"].lower()]
            else:
                results = [s for s in self.students if search_text in s["name"].lower()]

            # Display results
            for student in results:
                tree.insert("", tk.END, values=(
                    student["roll_number"],
                    student["name"],
                    student["age"],
                    student["class"],
                    student.get("section", ""),
                    student.get("address", "")
                ))

        ttk.Button(
            search_frame,
            text="Search",
            command=perform_search
        ).pack(side=tk.LEFT, padx=5)

        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    def edit_student(self, selection):
        """Edit selected student"""
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to edit!")
            return

        item = selection[0]
        tree = self.main_content.winfo_children()[0]
        values = tree.item(item)['values']
        roll_number = values[0]

        # Find student in data
        student = next((s for s in self.students if s["roll_number"] == roll_number), None)
        if not student:
            messagebox.showerror("Error", "Student not found!")
            return

        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Student")
        edit_window.geometry("400x400")

        form_frame = tk.Frame(edit_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Form fields
        tk.Label(form_frame, text="Roll Number:").grid(row=0, column=0, pady=5, sticky=tk.W)
        roll_label = tk.Label(form_frame, text=student["roll_number"])
        roll_label.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Name:").grid(row=1, column=0, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, student["name"])
        name_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Age:").grid(row=2, column=0, pady=5, sticky=tk.W)
        age_entry = ttk.Entry(form_frame)
        age_entry.insert(0, student["age"])
        age_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Class:").grid(row=3, column=0, pady=5, sticky=tk.W)
        class_entry = ttk.Entry(form_frame)
        class_entry.insert(0, student["class"])
        class_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Section:").grid(row=4, column=0, pady=5, sticky=tk.W)
        section_entry = ttk.Entry(form_frame)
        section_entry.insert(0, student.get("section", ""))
        section_entry.grid(row=4, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Address:").grid(row=5, column=0, pady=5, sticky=tk.W)
        address_entry = ttk.Entry(form_frame)
        address_entry.insert(0, student.get("address", ""))
        address_entry.grid(row=5, column=1, pady=5, padx=5)

        def save_changes():
            try:
                age = int(age_entry.get())
                if age < 5 or age > 30:
                    if not messagebox.askyesno("Confirm", "Age seems unusual. Continue anyway?"):
                        return
            except ValueError:
                messagebox.showerror("Error", "Age must be a number!")
                return

            # Update student data
            student["name"] = name_entry.get()
            student["age"] = age
            student["class"] = class_entry.get()
            student["section"] = section_entry.get()
            student["address"] = address_entry.get()

            self.save_students()
            messagebox.showinfo("Success", "Student information updated!")
            edit_window.destroy()
            self.show_student_list()

        ttk.Button(
            form_frame,
            text="Save Changes",
            command=save_changes
        ).grid(row=6, column=0, columnspan=2, pady=20)

    def delete_student(self, selection):
        """Delete selected student"""
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return

        item = selection[0]
        tree = self.main_content.winfo_children()[0]
        values = tree.item(item)['values']
        roll_number = values[0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            self.students = [s for s in self.students if s["roll_number"] != roll_number]
            self.save_students()
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.show_student_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()