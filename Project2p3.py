# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 16:18:09 2021

@author: capta
"""
from datetime import date
from tkinter import *
import sqlite3

root = Tk()


root.title('Group 15 Car Rental Service')

#we used a StringVar for text desplay for query returns
vartext = StringVar()
#adds a new customer, code is repurposed from our original project 2-2 code
#because we dont specify the CustID its set to 0
def custinsert(Name,Phone):

    conn = sqlite3.connect("Project2.db")
    c = conn.cursor()
    CustID = 0

    try:
        sqliteConnection = sqlite3.connect('Project2.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqliteInsert= """INSERT INTO CUSTOMER
                    (CustID, Name, Phone)
                    VALUES (?,?,?);"""

        data_tuple = (CustID, Name, Phone)
        cursor.execute(sqliteInsert, data_tuple)
        sqliteConnection.commit()
        print("Variables inserted succesfully rows altered 1")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert variable into sqlite table", error)
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
            print("Sqlite Connection is closed")

    print("rows altered = 1\n")
    custentry.destroy()
#adds a new vehicle, code is repurposed from our original project 2-2 code
def vehinsert(VehicleID, Description, Year, Type, Category):
    vehentry.destroy()
    try:
        sqliteConnection = sqlite3.connect('Project2.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqliteInsert= """INSERT INTO VEHICLE
                    (VehicleID, Description, Year, Type, Category)
                    VALUES (?,?,?,?,?);"""

        data_tuple = (VehicleID, Description, Year, Type, Category)
        cursor.execute(sqliteInsert, data_tuple)
        sqliteConnection.commit()
        print("Variables inserted succesfully")

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert variable into sqlite table", error)
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
            print("Sqlite Connection is closed")
    print("rows altered = 1\n")

#adds a rental task 2 query 3
def rentinsert(CustID,VehicleID,date,today,RentalType,Qty,payment,cat,Type):
    ndate = date.split()
    StartDate = ndate[0]
    ReturnDate = ndate[1]
    dayorweek = ''
    sqliteConnection = sqlite3.connect('Project2.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    print(RentalType)

    cursor.execute("SELECT * FROM RATE WHERE Type = ? AND Category = ?",(Type,cat,))
    output = cursor.fetchone()
    cursor.close()
    sqliteConnection.close()
    print("rows returned = 1\n")
    cost = 0

    if int(RentalType) == 1:
        cost = output[3]
    elif int(RentalType) == 7:
        cost = output[2]

    TotalAmount = cost*int(Qty)
    print(TotalAmount)

    PaymentDate = ''
    if payment == 'y':
        PaymentDate = today
    elif payment == 'n':
        PaymentDate = 'NULL'

    try:
        sqliteConnection = sqlite3.connect('Project2.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqliteInsert= """INSERT INTO RENTAL
                    (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate)
                    VALUES (?,?,?,?,?,?,?,?,?);"""

        data_tuple = (CustID, VehicleID, StartDate, today, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate)
        cursor.execute(sqliteInsert, data_tuple)
        sqliteConnection.commit()
        print("Variables inserted succesfully")

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert variable into sqlite table", error)
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
            print("Sqlite Connection is closed")
    blankout = ''
    print("rows altered = 1\n")
    vartext.set(blankout)
    rententry.destroy()
#Runs the search function for task 2 query 4
def rentsearch(Type, Category, Date):

    ndate = Date.split()
    StartDate = ndate[0]
    ReturnDate = ndate[1]

    sqliteConnection = sqlite3.connect('Project2.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    cursor.execute("SELECT v.VehicleID AS VIN, v.Description, v.year FROM VEHICLE v, RENTAL r WHERE v.VehicleID = r.VehicleID AND (v.Type = ? AND v.Category = ?) AND ((r.ReturnDate >= ?) OR (r.StartDate <= ?)) GROUP BY r.VehicleID", (Type, Category, StartDate, ReturnDate,))

    output = cursor.fetchall()
    cursor.close()
    sqliteConnection.close()
    #blank the output list for each call
    outputlist = ''
    #counter for rows returned and also selection for insert (maybe, hopefully)
    count = 0
    #just a diagnostic print to show the return from fetchall()
    print(output)
    #add the strings to an output list
    for text in output:
        count+=1
        outputlist += str(count)+" "+str(text)+"\n"
    #set the vartext as the output list
    print("rows returned = "+str(count)+"\n")
    vartext.set(outputlist)

#does the update for the rental table on a return task 2 query 4
def retinsert(VehicleID, ReturnDate, today):

    sqliteConnection = sqlite3.connect('Project2.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    #today is todays date from datetime, vehicleID is the vin, return date is the return date
    cursor.execute("UPDATE RENTAL SET PaymentDate = ? WHERE VehicleID = ? AND ReturnDate = ?", (today, VehicleID, ReturnDate,))
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
    print("rows altered = 1\n")
    retentry.destroy()
#does the search for a rental task2 query 4
def retsearch(VehicleID, Name, ReturnDate):
    sqliteConnection = sqlite3.connect('Project2.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    cursor.execute("SELECT TotalAmount FROM RENTAL r, CUSTOMER c WHERE r.CustID = c.CustID AND r.VehicleID = ? AND c.Name = ? AND ReturnDate = ?", (VehicleID, Name, ReturnDate,))
    print("rows returned = 1\n")
    output = cursor.fetchone()
    cursor.close()
    sqliteConnection.close()
    outputlist = ''
    print(output)
    print("rows returned = 1\n")
    outputlist = output[0]
    vartext.set(outputlist)

#does the customer balance check task2 query 5a
def balinsert(CustID, Name):
    sqliteConnection = sqlite3.connect('Project2.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    if CustID == "" and Name == "":
        cursor.execute("SELECT CustomerID, CustomerName, '$'||RentalBalance||'.00' RentalBalance FROM vRentalInfo ORDER BY RentalBalance ASC;")
    if CustID == "" and not len(Name)==0:
        Name = "%"+Name+"%"
        cursor.execute("SELECT CustomerID, CustomerName, '$'||RentalBalance||'.00' RentalBalance FROM vRentalInfo WHERE CustomerName LIKE ? ORDER BY RentalBalance ASC;",(Name,))
    if not len(CustID) == 0 and Name == "":
        cursor.execute("SELECT CustomerID, CustomerName, '$'||RentalBalance||'.00' RentalBalance FROM vRentalInfo WHERE CustomerID= ? ORDER BY RentalBalance ASC;",(CustID,))
    output = cursor.fetchall()
    outputlist = ''
    cursor.close()
    sqliteConnection.close()

    count = 0
    print(output)
    for text in output:
        count += 1
        outputlist += str(count) + " " + str(text)+"\n"
    print("rows returned = "+str(count)+"\n")
    vartext.set(outputlist)

#does the vehicle search task 2 query 5b
def searchinsert(Vin, Description):
    sqliteConnection = sqlite3.connect('Project2.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    if Vin == "" and not len(Description) == 0:
        Description = "%"+Description+"%"
        cursor.execute("SELECT vRentalInfo.VIN, vRentalInfo.Vehicle, '$'||RATE.Daily||'.00' FROM RATE, vRentalInfo, VEHICLE WHERE vRentalInfo.Vehicle LIKE ? AND RATE.Type = VEHICLE.Type AND RATE.Category = VEHICLE.Category AND VEHICLE.VehicleID = vRentalInfo.VIN;",(Description,))
    elif Description == "" and not len(Vin) == 0:
        cursor.execute("SELECT vRentalInfo.VIN, vRentalInfo.Vehicle, '$'||RATE.Daily||'.00' FROM RATE, vRentalInfo, VEHICLE WHERE vRentalInfo.VIN LIKE ? AND RATE.Type = VEHICLE.Type AND RATE.Category = VEHICLE.Category AND VEHICLE.VehicleID = vRentalInfo.VIN;",(Vin,))
    elif Vin != "" and Description != "":
        cursor.execute("SELECT vRentalInfo.VIN, vRentalInfo.Vehicle, '$'||RATE.Daily||'.00' FROM RATE, vRentalInfo, VEHICLE WHERE (vRentalInfo.VIN = ? AND vRentalInfo.Vehicle = ?) AND RATE.Type = VEHICLE.Type AND RATE.Category = VEHICLE.Category AND VEHICLE.VehicleID = vRentalInfo.VIN;",(Vin, Description,))
    elif Vin == "" and Description == "":
        cursor.execute("SELECT vRentalInfo.VIN, vRentalInfo.Vehicle, '$'||RATE.Daily||'.00' FROM RATE, vRentalInfo, VEHICLE WHERE RATE.Type = VEHICLE.Type AND RATE.Category = VEHICLE.Category AND VEHICLE.VehicleID = vRentalInfo.VIN ORDER BY RATE.Daily;")
    else:
        print("Not applicable")

    output = cursor.fetchall()
    cursor.close()

    sqliteConnection.close()
    outputlist = ''
    count = 0
    print(output)
    for text in output:
        count+=1
        outputlist += str(count)+" "+str(text)+"\n"
    print("rows returned = "+str(count)+"\n")
    vartext.set(outputlist)

#these are all pop ups from the main window with the individual entry fields for the various queries 1-5
def custbutton():
    global custentry
    #blanking out the display string
    vartext.set('')
    custentry = Toplevel(root)
    custentry.title("Customer entry screen")

    custlabel = Label(custentry, text = "Please enter customer information")
    custlabel.grid(row = 0, column = 1)

    fullname_label = Label(custentry, text = "enter the customers full name")
    fullname_label.grid(row = 1, column = 1)

    fullname = Entry(custentry, width = 30)
    fullname.grid(row = 2,column = 1)

    phonenum = Label(custentry, text = "enter the customers phone #")
    phonenum.grid(row = 3, column = 1)

    phoneentry = Entry(custentry, width = 30)
    phoneentry.grid(row = 4, column = 1)

    CustButton = Button(custentry, text = "submit", command=lambda: custinsert(fullname.get(),phoneentry.get()))
    CustButton.grid(row = 5, column = 1, columnspan = 3)

def vehbutton():
    global vehentry
    vartext.set('')
    vehentry = Toplevel(root)
    vehentry.title("Vehicle entry screen")

    vehlabel = Label(vehentry, text = "Please enter vehicle information")
    vehlabel.grid(row = 0, column = 1)

    VIN_label = Label(vehentry, text = "enter the VIN #")
    VIN_label.grid(row = 1, column = 1)

    VINentry = Entry(vehentry, width = 30)
    VINentry.grid(row = 2,column = 1)

    maketype = Label(vehentry, text = "enter the vehicles make")
    maketype.grid(row = 3, column = 1)

    makeent = Entry(vehentry, width = 30)
    makeent.grid(row = 4, column = 1)

    yearnum = Label(vehentry, text = "enter the year")
    yearnum.grid(row = 5, column = 1)

    yearent = Entry(vehentry, width = 30)
    yearent.grid(row = 6, column = 1)

    typelabel = Label(vehentry, text = "enter the type 1-6\n1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN ")#maybe change this to recognize the type
    typelabel.grid(row = 7, column = 1)

    typeent = Entry(vehentry, width = 30)
    typeent.grid(row = 8, column = 1)

    catlabel = Label(vehentry, text = "enter the category #\n0 = Basic, 1 = Luxury")
    catlabel.grid(row = 9, column = 1)

    catentry = Entry(vehentry, width = 30)
    catentry.grid(row = 10, column = 1)


    VehButton = Button(vehentry, text = "submit", command=lambda: vehinsert(
        VINentry.get(),makeent.get(), yearent.get(), typeent.get(), catentry.get()))
    VehButton.grid(row = 11, column = 1, columnspan = 3)

def rentbutton():
    global rententry
    vartext.set('')
    rententry = Toplevel(root)
    rententry.title("rental entry screen")

    vehlabel = Label(rententry, text = "Enter the type 1-6\n1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN")
    vehlabel.grid(row = 0, column = 1)

    vehentry = Entry(rententry, width = 30)
    vehentry.grid(row = 1,column = 1)

    typelabel = Label(rententry, text = "Enter the category #\n0 = Basic, 1 = Luxury")
    typelabel.grid(row = 2, column = 1)

    typeentry = Entry(rententry, width = 30)
    typeentry.grid(row = 3,column = 1)

    datelabel = Label(rententry, text = "Enter the rental period start and end \nyyyy-mm-dd(space)yyyy-mm-dd")
    datelabel.grid(row = 4, column = 1)

    dateentry = Entry(rententry, width = 30)
    dateentry.grid(row = 5,column = 1)
    #
    #feeds info to search function, need to find a way to clear the fields
    #
    searchButton = Button(rententry, text = "find available vehicles",
                          command =lambda: rentsearch(vehentry.get(),typeentry.get(),dateentry.get()))
    searchButton.grid(row = 6, column = 1, columnspan = 3)

    VINlabel = Label(rententry, text = "enter car VIN:")
    VINlabel.grid(row = 7, column = 1, columnspan = 3)

    rentinput = Entry(rententry, width = 30)
    rentinput.grid(row = 8, column = 1, columnspan =3)

    idlabel = Label(rententry, text = "enter customer id:")
    idlabel.grid(row = 9, column = 1, columnspan = 3)

    idinput = Entry(rententry, width = 30)
    idinput.grid(row = 10, column = 1, columnspan =3)

    renttypelabel = Label(rententry, text = "weekly or daily? 1 or 7:")
    renttypelabel.grid(row = 11, column = 1, columnspan = 3)

    renttypeinput = Entry(rententry, width = 30)
    renttypeinput.grid(row = 12, column = 1, columnspan =3)

    numlabel = Label(rententry, text = "how many weeks or days?:")
    numlabel.grid(row = 13, column = 1, columnspan = 3)

    numinput = Entry(rententry, width = 30)
    numinput.grid(row = 14, column = 1, columnspan =3)

    paylabel = Label(rententry, text = "Pay now? y/n:")
    paylabel.grid(row = 15, column = 1, columnspan = 3)

    payinput = Entry(rententry, width = 30)
    payinput.grid(row = 16, column = 1, columnspan =3)

    rentButton = Button(rententry, text = "rent vehicle", command =lambda: rentinsert(idinput.get(),
                                rentinput.get(),dateentry.get(),date.today(),renttypeinput.get(),
                                numinput.get(),payinput.get(),vehentry.get(),typeentry.get()))
    rentButton.grid(row = 17, column = 1, columnspan = 3)

    rentlabel = Label(rententry, text = "available vehicles:")
    rentlabel.grid(row = 18, column = 1, columnspan = 3)
    #textvariable = vartext is what allows the the updated text variable to be displayed
    listlabel = Label(rententry, textvariable = vartext)
    listlabel.grid(row = 19, column = 1, columnspan = 3)






def retbutton():
    global retentry
    vartext.set('')
    retentry = Toplevel(root)
    retentry.title("return screen")
    vehlabel = Label(retentry, text = "Enter car VIN")
    vehlabel.grid(row = 0, column = 1)

    vehentry = Entry(retentry, width = 30)
    vehentry.grid(row = 1,column = 1)

    typelabel = Label(retentry, text = "Enter first initial and last name")
    typelabel.grid(row = 2, column = 1)

    nameentry = Entry(retentry, width = 30)
    nameentry.grid(row = 3,column = 1)

    datelabel = Label(retentry, text = "Enter Return date")
    datelabel.grid(row = 4, column = 1)

    dateentry = Entry(retentry, width = 30)
    dateentry.grid(row = 5,column = 1)

    RetButton = Button(retentry, text = "submit", command =lambda: retsearch(vehentry.get(),nameentry.get(),dateentry.get()))
    RetButton.grid(row = 6, column = 1, columnspan = 3)

    costlabel = Label(retentry, text = "amount due:")
    costlabel.grid(row = 7, column = 1, columnspan = 3)
    #textvariable = vartext is what allows the the updated text variable to be displayed
    listlabel = Label(retentry, textvariable = vartext)
    listlabel.grid(row = 8, column = 1, columnspan = 3)

    RetButton = Button(retentry, text = "Pay now", command =lambda: retinsert(vehentry.get(),dateentry.get(),date.today()))
    RetButton.grid(row = 9, column = 1, columnspan = 3)



def balbutton():
    global balentry
    vartext.set('')
    balentry = Toplevel(root)
    balentry.title("balance screen")

    custlabel = Label(balentry, text = "Filter By Customer ID (Type Cust ID):")
    custlabel.grid(row = 0, column = 1)

    custentry = Entry(balentry, width = 30)
    custentry.grid(row = 1,column = 1)

    namelabel = Label(balentry, text = "Filter By Name(Type Name or part of name):")
    namelabel.grid(row = 2, column = 1)

    nameentry = Entry(balentry, width = 30)
    nameentry.grid(row = 3,column = 1)

    BalButton = Button(balentry, text = "submit",
                       command = lambda: balinsert(custentry.get(),nameentry.get()))
    BalButton.grid(row = 6, column = 1, columnspan = 3)

    listlabel = Label(balentry, textvariable = vartext)
    listlabel.grid(row = 19, column = 1, columnspan = 3)

def searchbutton():
    global searchentry
    vartext.set('')
    searchentry = Toplevel(root)
    searchentry.title("search screen")

    searchlabel = Label(searchentry, text = "Please search vehicle information")
    searchlabel.grid(row = 0, column = 1)

    VIN_label = Label(searchentry, text = "Search using VIN")
    VIN_label.grid(row = 1, column = 1)

    VINentry = Entry(searchentry, width = 30)
    VINentry.grid(row = 2,column = 1)

    descriptionlabel = Label(searchentry, text = "Search using vehicle Description")
    descriptionlabel.grid(row = 3, column = 1)

    descriptionentry = Entry(searchentry, width = 30)
    descriptionentry.grid(row = 4, column = 1)

    SearchButton = Button(searchentry, text = "submit", command = lambda: searchinsert(VINentry.get(),descriptionentry.get()))
    SearchButton.grid(row = 11, column = 1, columnspan = 3)

    listlabel = Label(searchentry, textvariable = vartext)
    listlabel.grid(row = 19, column = 1, columnspan = 3)

def closebutt():
    root.destroy()


toplabel = Label(root, text = "Please click on the action you would like to perform.")
toplabel.grid(row = 0, column = 2)

nCustButton = Button(root, text = "Add new customer", command = custbutton)
nCustButton.grid(row = 1, column = 1, columnspan = 3)

nVehicleButton = Button(root, text = "Add new vehicle", command = vehbutton)
nVehicleButton.grid(row = 2, column = 1, columnspan = 3)

nRentButton = Button(root, text = "New rental", command = rentbutton)
nRentButton.grid(row = 3, column = 1, columnspan = 3)

nRetButton = Button(root, text = "Return car", command = retbutton)
nRetButton.grid(row = 4, column = 1, columnspan = 3)

nBalButton = Button(root, text = "Customer balance", command = balbutton)
nBalButton.grid(row = 5, column = 1, columnspan = 3)

nSearchButton = Button(root, text = "Search vehicles", command = searchbutton)
nSearchButton.grid(row = 6, column = 1, columnspan = 3)

nClButton = Button(root, text = "Close", command = closebutt)
nClButton.grid(row = 7, column = 1, columnspan = 3)

root.mainloop()
