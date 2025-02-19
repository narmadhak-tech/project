#Employee Management System using Python - Narmadha (Console application Project)
from os import system
import re

#importing mysql connector
import mysql.connector

#making connection
con = mysql.connector.connect(host="localhost",user="root",password="root",database="employee")

#function to check if employee with given name exist or not
def check_employee_name(emp_name):
    #query to select all rows from employee(empdata) table
    sql='select * from empdata where Name=%s'
    #making cursor buffered to make rowcount method work properly
    c=con.cursor(buffered=True)
    data=(emp_name,)

    #execute the sql query
    c.execute(sql,data)
    if c.fetchone() is not None:
        return True  # Employee exists
    else:
        return False
    
#function to check if employee with given id exist or not
def check_employee_id(emp_id):
    #query to select all rows from employee(empdata) table
    sql='select * from empdata where Id=%s'
    #making cursor buffered to make rowcount method work properly
    c=con.cursor(buffered=True)
    data=(emp_id,)

    #execute the sql query
    c.execute(sql,data)
    return c.fetchone() is not None
    
# Add_Employee function
def Add_Employee():
    print("{:>60}".format("-->> Add Employee Record <<--"))

    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if (check_employee_id(Id) == True):
        print("Employee ID Already Exists\nTry Again..")
        press = input("Press Any Key To Continue..")
        Add_Employee()
    
    Name = input("Enter Employee Name: ")
    # Checking if employee name exists or not
    if check_employee_name(Name) == True:
        print("Employee Already Exists\n Try Again..")
        press = input("Press Any Key To Continue..")
        return
    
    Email_id = input("Enter Employee Email Id: ")
    Phone_No = input("Enter Employee Phone Number: ")
    Address = input("Enter Employee Address: ")
    Post = input("Enter Employee Post: ")
    Salary = input("Enter Employee Salary: ")

    data = (Name, Email_id, Phone_No, Address, Post, Salary)
    sql = "INSERT INTO empdata (Name, Email_Id, Phone_No, Address, Post, Salary) VALUES (%s, %s, %s, %s, %s, %s)"
    
    try:
        # Create cursor and execute the insert statement
        c = con.cursor()
        c.execute(sql, data)
        
        # Commit the changes
        con.commit()
        
        print("Successfully Added Employee Record")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()  # In case of an error, rollback any changes
    finally:
        c.close()  # Ensure cursor is closed after the transaction
    press = input("Press Any Key To Continue..")

#display employee function
def Display_Employee():
    print("{:>60}".format("-->> Display Employee Record <<--"))
    # query to select all rows from Employee (empdata) Table
    sql = 'select * from empdata'
    c = con.cursor()

    # Executing the sql query
    c.execute(sql)
    # Fetching all details of all the Employees
    r = c.fetchall()
    for i in r:
        print("Employee Id: ", i[0])
        print("Employee Name: ", i[1])
        print("Employee Email Id: ", i[2])
        print("Employee Phone No.: ", i[3])
        print("Employee Address: ", i[4])
        print("Employee Post: ", i[5])
        print("Employee Salary: ", i[6])
        print("\n")
    press = input("Press Any key To Continue..")
    menu()

#update employee function
def Update_Employee():
    print("{:>60}".format("-->> Update Employee Record <<--"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee_id(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
        return

    # Name update
    Name = input("Enter Employee Name: ")
    if not Name.strip():  # Check if name is not empty
        print("Name cannot be empty.")
        input("Press any key to continue...")
        return

    Email_Id = input("Enter Employee Email ID: ")
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if(re.fullmatch(regex, Email_Id)):
        print("Valid Email")
    else:
        print("Invalid Email")
        press = input("Press Any Key To Continue..")
        Update_Employee()
        return
    
    Phone_no = input("Enter Employee Phone No.: ")
    phone_regex = r'^[6-9]\d{9}$'  
    if re.fullmatch(phone_regex, Phone_no):
        print("Valid Phone Number")
    else:
        print("Invalid Phone Number")
        press = input("Press Any Key To Continue..")
        Update_Employee()
        return

    Address = input("Enter Employee Address: ")
    # Updating Employee details in empdata Table
    sql = 'UPDATE empdata set Email_Id = %s, Phone_no = %s, Address = %s where Id = %s'
    data = (Email_Id, Phone_no, Address, Id)
    c = con.cursor()

    # Executing the sql query
    c.execute(sql, data)

    # commit() method to make changes in the table
    con.commit()
    print("Updated Employee Record")
    press = input("Press Any Key To Continue..")
    menu()

#promote employee function
def Promote_Employee():
    print("{:>60}".format("-->> Promote Employee Record <<--"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee_id(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        Amount  = int(input("Enter Increase Salary: "))
        #query to fetch salary of Employee with given data
        sql = 'select Salary from empdata where Id=%s'
        data = (Id,)
        c = con.cursor()
        
        #executing the sql query
        c.execute(sql, data)

        #fetching salary of Employee with given Id
        r = c.fetchone()
        t = r[0]+Amount
        
        #query to update salary of Employee with given id
        sql = 'update empdata set Salary = %s where Id = %s'
        d = (t, Id)

        #executing the sql query
        c.execute(sql, d)

        #commit() method to make changes in the table 
        con.commit()
        print("Employee Promoted")
        press = input("Press Any key To Continue..")
        menu()

# Function to Remove_Employ
def Remove_Employee():
    print("{:>60}".format("-->> Remove Employee Record <<--\n"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee_id(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        #query to delete Employee from empdata table
        sql = 'delete from empdata where Id = %s'
        data = (Id,)
        c = con.cursor()

        #executing the sql query
        c.execute(sql, data)

        #commit() method to make changes in the empdata table
        con.commit()
        print("Employee Removed")
        press = input("Press Any key To Continue..")
        menu()

# Function to Search_Employ
def Search_Employ():
    print("{:>60}".format("-->> Search Employee Record <<--\n"))
    Id = input("Enter Employee Id: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee_id(Id) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        #query to search Employee from empdata table
        sql = 'select * from empdata where Id = %s'
        data = (Id,)
        c = con.cursor()
        
        #executing the sql query
        c.execute(sql, data)

        #fetching all details of all the employee
        r = c.fetchall()
        for i in r:
            print("Employee Id: ", i[0])
            print("Employee Name: ", i[1])
            print("Employee Email Id: ", i[2])
            print("Employee Phone No.: ", i[3])
            print("Employee Address: ", i[4])
            print("Employee Post: ", i[5])
            print("Employee Salary: ", i[6])
            print("\n")
        press = input("Press Any key To Continue..")
        menu()

#menu function to display menu
def menu():
    system("cls")
    print("{:>60}".format("**********************************"))
    print("{:>60}".format("-->> Employee Management System <<--"))
    print("{:>60}".format("**********************************"))
    print("1. Add Employee")
    print("2. Display Employee Record")
    print("3. Update Employee Record")
    print("4. Promote Employee Record")
    print("5. Remove Employee Record")
    print("6. Search Employee Record")
    print("7. Exit\n")
    print("{:>60}".format("-->> Choice Options: [1/2/3/4/5/6/7] <<--"))

    ch=int(input("Enter your Choice: "))
    if ch==1:
        system("cls")
        Add_Employee()
    elif ch==2:
        system("cls")
        Display_Employee()
    elif ch==3:
        system("cls")
        Update_Employee()
    elif ch==4:
        system("cls")
        Promote_Employee()
    elif ch==5:
        system("cls")
        Remove_Employee()
    elif ch==6:
        system("cls")
        Search_Employee()
    elif ch==7:
        system("cls")
        print("{:>60}".format("Have A Nice Day:)"))
        exit(0)
    else:
        print("Invalid Choice")
        press= input("Press Any Key To Continue..")
        menu()
    
#calling menu function
menu()
