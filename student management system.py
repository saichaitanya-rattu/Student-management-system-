import json

students = []

#----------------LOAD DATA-----------------------
def  load_data():
    global students
    try:
        with open("students.json","r") as file:
            students = json.load(file)
    except FileNotFoundError:
        students = []


#----------------SAVE DATA-----------------------
def save_data():
    print("saving data...")
    with open("students.json","w") as file:
        json.dump(students,file,indent=4)

#-------------------ADD STUDENT----------------------
def add_student():
    name = input("enter student name:")
    age = input("enter age:")
    course = input("enter course:")
    phone = input("enter phone number:")

    student ={
       "name" : name,
       "age": age,
       "course" : course,
       "phone" : phone
    }

    students.append(student)
    save_data()
    print("student added successfully! \n")


#-------------------VIEW STUDENTS----------------------
def view_students():
    if not students:
        print("No student found.\n")
        return

    print("\n {:<5} {:<15} {:<5} {:<10} {:<15}".format("No.", "Name", "Age", "Course", "Phone"))
    print("-" * 55)
    for i, student in enumerate(students,start=1):
        print("{:<5} {:<15} {:<5} {:<10} {:<15}".format(i, student["name"], student["age"], student["course"], student["phone"]))
    print()

#-------------------SEARCH STUDENT----------------------
def search_student():
    name = input("enter name to search:")

    found = False
    for student in students:
        if student["name"].lower() == name.lower():
            print(f"Found: Name: {student['name']}, Age: {student['age']}, Course: {student['course']}, Phone: {student['phone']}")
            found = True
            break

    if not found:
        print("student not found.\n")


#-------------------DELETE STUDENT----------------------
def delete_student():
    name = input("Enter name to delete:")

    for student in students:
        if student["name"].lower() == name.lower():
            students.remove(student)
            print("Student deleted successfully!\n")
            return  
        
    print("Student not found.\n")


#-----------------cleanup----------------------
def clear_data():
    global students
    confirm = input("Are you sure you want to clear all data? (yes/no):")
    
    if confirm.lower() == "yes":
        students = []
        save_data()
        print("All data cleared successfully!\n")
    else:
        print("operation cancelled.\n")

#-------------------MENU----------------------
def menu():
    while True:
        print("====== Student Management System ======")
        print("1. Add student")
        print("2. View student")
        print("3. Search student")
        print("4. Delete student")
        print("5. Clear all data")
        print("6. Exit")

        choice = input("enter your choice:")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            delete_student()
        elif choice == "5": 
            clear_data() 
        elif choice == "6":    
            print("exiting program...")
            break
        else:
            print("invalid choice. Try again.\n")

#--------------------RUN PROGRAM----------------------
load_data()
menu()
        
