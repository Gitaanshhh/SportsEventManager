"""
Imports

Functions -> Pascal case -> Eg - ThisIsAFunction
Variables -> Camel case -> Eg - thisIsAVariable
Classes - Pascal
Objects - Camel case

"""
import mysql.connector as sql   # Database connectivity
from tkinter import *   # GUI
from PIL import ImageTk, Image  # Handling Images
from tkcalendar import DateEntry    # Calender widget for Date selection

ACCESS = False

"""
DATABASE CONNECTIVITY
"""
def ConnectToSQL():
    """
    Establish a connection to MySQL database
    Returns:
        connextion : Connection object
        cursor : Cursor object
    """
    global connection, cursor
    connection = sql.connect(host='localhost', user='root', passwd='rootpw')
    cursor = connection.cursor()
    cursor.execute("USE Git;")
    return connection, cursor

connection, cursor = ConnectToSQL()

# Creates Database if it doesn't exist
try:
    cursor.execute("CREATE DATABASE Git")
except sql.Error as err:
    print("Failed creating database: {}".format(err))

cursor.execute("USE Git;")
if connection.is_connected():
    print('connected.')

def CreateTable(x):
    """ 
    Creates a table for various age categories if not already existing. 
    Parameters : 
        x (str) : Table name (like U19M, U17F, etc.)
    """
    try:
        cursor.execute(f"CREATE TABLE {x} (Sport char(11) PRIMARY KEY, MainPL integer, SubPL integer, event date, FIRST char(5), SECOND char(5), THIRD char(5), FOURTH char(5));")
    except sql.Error as err:
        print("Table already exists: {}".format(err))

CreateTable('U19M')
CreateTable('U19F')
CreateTable('U17M')
CreateTable('U17F')
CreateTable('U14M')
CreateTable('U14F')
CreateTable('U12M')
CreateTable('U12F')

connection.commit()
connection.close()

# Passwords for access control
passwords = {'PT': 'pt', 'Maple': 'maple', 'Pine': 'pine', 'Oak': 'oak', 'Cedar': 'cedar'}

"""
GUI PART
"""
mainWindow = Tk()
mainWindow.title('Sports Event Manager')
mainWindow.minsize(800, 600)

def Forget(widget):
    """
    Removes a widget from the grid
    """
    widget.grid_forget()

def Submit1(category, gender, name, players, substitutes, calendar):
    """
    Inserts event details into selected category table
    """
    connection, cursor = ConnectToSQL()
    cursor.execute(f"INSERT INTO {category.get()+gender.get()} (Sport, MainPL, SubPL, event) VALUES ('{name.get()}', {int(players.get())}, {int(substitutes.get())}, '{calendar.get_date()}');")
    connection.commit()
    connection.close()
    
    # Clearing the input fields post submission
    name.delete(0, END)
    players.delete(0, END)
    substitutes.delete(0, END)
    calendar.delete(0, END)

def GetEvent():
    """
    Window for inputting event details from user
    """
    eventWindow = Toplevel()
    eventWindow.title('New Event')
    eventWindow.minsize(800, 600)

    labelTtile = Label(eventWindow, text='Enter the following details').grid(row=1, column=1)
    labelName = Label(eventWindow, text='Name:')
    entryName = Entry(eventWindow)
    labelNumOfPlayers = Label(eventWindow, text='Number of Players')
    entryNumOfPlayers = Entry(eventWindow)
    entryNumOfSubstitutes = Entry(eventWindow)
    CATEGORY = StringVar()
    GENDER = StringVar()

    calendar = DateEntry(eventWindow, selectmode='day')
    calendar.delete(0, END)

    dropCAT = OptionMenu(eventWindow, CATEGORY, 'U19', 'U17', 'U14', 'U12')
    dropGEN = OptionMenu(eventWindow, GENDER, 'M', 'F')

    labelName.grid(row=2, column=1)
    entryName.grid(row=2, column=2)
    labelNumOfPlayers.grid(row=3, column=1)
    entryNumOfPlayers.grid(row=3, column=2)
    entryNumOfSubstitutes.grid(row=3, column=4)
    dropCAT.grid(row=4, column=1)
    dropGEN.grid(row=4, column=3)
    calendar.grid(row=5, column=2)

    Button(eventWindow, text='Clear Date', padx=10, pady=6, command=lambda: calendar.delete(0, END)).grid(row=5, column=3)
    space = Label(text=' ').grid(row=6, columnspan=3)
    Button(eventWindow, text='Submit', padx=15, pady=10, command=lambda: Submit1(CATEGORY, GENDER, entryName, entryNumOfPlayers, entryNumOfSubstitutes, calendar)).grid(row=7, column=2)

def DisplayEvent():
    """
    Window for displaying all events in the database
    """
    eventWindow = Toplevel()
    eventWindow.title('EVENTS : ')
    eventWindow.minsize(700, 500)
    connection, cursor = ConnectToSQL()

    def display(age, col):
        """
        Displays the events for a given age group
        """
        row = 1
        cursor.execute(f"SELECT * FROM {age}M")
        male = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {age}F")
        female = cursor.fetchall()

        Label(eventWindow, text=f'{age}M').grid(row=1, column=col)
        for x in range(len(male)):
            Label(eventWindow, text=male[x][:4]).grid(row=1+x+1, column=col)
            row = 1+x+1
        Label(eventWindow, text=' ').grid(row=row + 1, column=col)
        Label(eventWindow, text=f'{age}F').grid(row=row + 2, column=col)
        for x in range(len(female)):
            Label(eventWindow, text=female[x][:4]).grid(row=2 + row + 1 + x, column=col)
        Label(eventWindow, text=' ').grid(row=1, column=col+1)

    display('U19', 1)
    display('U17', 3)
    display('U14', 5)
    display('U12', 7)

    connection.commit()
    connection.close()

def Search(category, gender, window, task):
    """
    Function to search for an event in the database based on the age category and gender
    Allows updating and editing of the event details
    """
    connection, cursor = ConnectToSQL()
    cursor.execute(f"SELECT * FROM {category.get()+gender.get()};")
    
    data = cursor.fetchall()
    for a in range(len(data)):
        data[a] = data[a][0]

    x = StringVar()
    drop = OptionMenu(window, x, *data)
    drop.grid(row=6, column=4)
    cursor.close()

    def Update():
        """
        Updates event rankings
        """
        Label(window, text='First').grid(row=7, column=1)
        Label(window, text='Second').grid(row=7, column=2)
        Label(window, text='Third').grid(row=7, column=3)
        Label(window, text='Fourth').grid(row=7, column=4)
        global I, II, III, IV
        I = StringVar()
        II = StringVar()
        III = StringVar()
        IV = StringVar()
        houselist = ['Maple', 'Oak', 'Pine', 'Cedar']
        OptionMenu(window, I, *houselist).grid(row=8, column=1)
        OptionMenu(window, II, *houselist).grid(row=8, column=2)
        OptionMenu(window, III, *houselist).grid(row=8, column=3)
        OptionMenu(window, IV, *houselist).grid(row=8, column=4)

    def Edit(task):
        """
        Edits event details
        """
        Label(window, text='Name:').grid(row=9, column=1)
        name = Entry(window)
        Label(window, text='Number of Players').grid(row=10, column=1)
        players = Entry(window)
        substitutes = Entry(window)
        CAT = StringVar()
        GEN = StringVar()
        dropCAT = OptionMenu(window, CAT, 'U19', 'U17', 'U14', 'U12')
        dropGEN = OptionMenu(window, GEN, 'M', 'F')
        calendar = DateEntry(window, selectmode='day')
        calendar.delete(0, END)

        name.grid(row=9, column=2)
        players.grid(row=10, column=2)
        substitutes.grid(row=10, column=4)
        dropCAT.grid(row=11, column=1)
        dropGEN.grid(row=11, column=3)
        calendar.grid(row=12, column=2)

        def Submit2(CAT, GEN, name, players, substitute, iname, cal):
            connection, cursor = ConnectToSQL()
            cursor.execute(f"DELETE FROM {category.get()+gender.get()} WHERE Sport = '{x.get()}';")
            cursor.execute(f"INSERT INTO {CAT.get()+GEN.get()} (Sport, MainPL, SubPL, event) VALUES ('{name.get()}', {int(players.get())}, {int(substitute.get())}, '{cal.get_date()}');")
            name.delete(0, END)
            players.delete(0, END)
            substitute.delete(0, END)
            connection.commit()
            connection.close()

        Button(window, text='Clear Date', padx=10, pady=6, command=lambda: calendar.delete(0, END)).grid(row=12, column=4)
        Button(window, text='Submit', padx=6, pady=10, command=lambda: Submit2(CAT, GEN, name, players, substitutes, x, calendar)).grid(row=12, column=3)
        if task == 'Edit':
            Button(window, text='Remove', padx=6, pady=10, command=delete).grid(row=15, column=5)

    def Submit():
        """
        Updating the Results of the event in the database
        """
        connection, cursor = ConnectToSQL()
        cursor.execute(f"UPDATE {category.get()+gender.get()} SET FIRST = '{I.get()}', SECOND = '{II.get()}', THIRD = '{III.get()}', FOURTH = '{IV.get()}' WHERE Sport = '{x.get()}';")
        window.destroy()
        connection.commit()
        connection.close()

    def delete():
        """
        Deletes an event
        """
        connection, cursor = ConnectToSQL()
        cursor.execute(f"DELETE FROM {category.get()+gender.get()} WHERE Sport = '{x.get()}';")
        window.destroy()
        connection.commit()
        connection.close()

    if task == 'Update':
        Button(window, text='Go', padx=6, pady=10, command=Update).grid(row=6, column=5)
        Button(window, text='Submit', padx=6, pady=10, command=Submit).grid(row=8, column=5)
    if task == 'Edit':
        Button(window, text='Go', padx=6, pady=10, command=lambda: Edit('Edit')).grid(row=6, column=5)

def Update(task):
    """
    Opens a window for updating events
    """
    w = Toplevel()
    w.title('Update')
    w.minsize(400, 400)
    CATEG = StringVar()
    GENDER = StringVar()

    dropCAT = OptionMenu(w, CATEG, 'U19', 'U17', 'U14', 'U12')
    dropGEN = OptionMenu(w, GENDER, 'M', 'F')

    dropCAT.grid(row=1, column=1)
    dropGEN.grid(row=2, column=1)

    Button(w, text='Search', padx=6, pady=10, command=lambda: Search(CATEG, GENDER, w, task)).grid(row=4, column=1)

def Event(ACCESS):
    """
    Displays a window for managing events based on access level
    """
    win2 = Toplevel()
    win2.title('Events')
    win2.minsize(800, 600)

    b = Button(win2, text='ADD Event', padx=6, pady=10, command=GetEvent)

    if ACCESS == 'PT':
        b.grid(row=0, column=0)

    b = Button(win2, text='Show Events', padx=6, pady=10, command=DisplayEvent).grid(row=1, column=0)
    b = Button(win2, text='Update Events', padx=6, pady=10, command=lambda: Update('Update'))

    if ACCESS == 'PT':
        b.grid(row=2, column=0)

    b = Button(win2, text='Edit Events', padx=6, pady=10, command=lambda: Update('Edit'))
    
    if ACCESS == 'PT':
        b.grid(row=3, column=0)

def Score():
    """
    Calculates and displays scores for each house (faction)
    """
    window = Toplevel()
    window.title('SCORE')
    window.minsize(400, 400)

    def Count(a):
        connection, cursor = ConnectToSQL()
        position = []
        points = 0

        for event in ('U19M', 'U19F', 'U17M', 'U17F', 'U14M', 'U14F', 'U12M', 'U12F'):
            cursor.execute(f"SELECT * FROM {event}")
            u19 = cursor.fetchall()
            for x in range(len(u19)):
                if a == u19[x][4]:
                    position.append(1)
                if a == u19[x][5]:
                    position.append(2)
                if a == u19[x][6]:
                    position.append(3)
                if a == u19[x][7]:
                    position.append(4)

        for x in position:
            if x == 1:
                points += 10
            if x == 2:
                points += 5
            if x == 3:
                points += 3
            if x == 4:
                points += 1

        return points

    maple = Count('Maple')
    oak = Count('Oak')
    pine = Count('Pine')
    cedar = Count('Cedar')

    Label(window, text='MAPLE').grid(row=1, column=1)
    Label(window, text=maple).grid(row=2, column=1)

    Label(window, text='OAK').grid(row=1, column=2)
    Label(window, text=oak).grid(row=2, column=2)

    Label(window, text='PINE').grid(row=1, column=3)
    Label(window, text=pine).grid(row=2, column=3)

    Label(window, text='CEDAR').grid(row=1, column=4)
    Label(window, text=cedar).grid(row=2, column=4)

def MainFrame(task):
    """
    Creates a login frame for access control.
    """
    frame = Toplevel()
    frame.minsize(400, 300)

    def Login(x):
        """
        Checks login credentials.
        """
        global ACCESS
        if x in passwords.keys() and epw.get() == passwords[x]:
            ACCESS = True
            if task == 'Update':
                Search(cat, gen, frame, 'Update')
            elif task == 'Edit':
                Search(cat, gen, frame, 'Edit')
            frame.destroy()

    Label(frame, text='Enter password to access').grid(row=1, column=2)
    epw = Entry(frame)
    epw.grid(row=2, column=2)

    house = StringVar()
    drop = OptionMenu(frame, house, *passwords.keys())
    drop.grid(row=2, column=3)
    Button(frame, text='Submit', padx=6, pady=10, command=lambda: Login(house.get())).grid(row=2, column=4)

def ResetAll():
    """
    Resets all events by deleting them from the database
    """
    window = Toplevel()
    window.title('RESET ALL : ')
    window.minsize(600, 500)

    def ClearTable(x):
        conn, c = ConnectToSQL()
        c.execute(f"DELETE FROM {x.get()};")
        conn.commit()
        conn.close()

    global I, II, III, IV
    I = StringVar()
    II = StringVar()
    III = StringVar()
    IV = StringVar()
    CAT = StringVar()
    GEN = StringVar()

    houselist = ['Maple', 'Oak', 'Pine', 'Cedar']

    OptionMenu(window, CAT, 'U19', 'U17', 'U14', 'U12').grid(row=2, column=2)
    OptionMenu(window, GEN, 'M', 'F').grid(row=2, column=3)

    Button(window, text='RESET ALL', padx=20, pady=10, command=lambda: ClearTable(CAT)).grid(row=2, column=5)

cat = StringVar()
gen = StringVar()
Button(mainWindow, text='New Event', padx=10, pady=6, command=GetEvent).grid(row=2, column=2)
Button(mainWindow, text='View Event', padx=10, pady=6, command=DisplayEvent).grid(row=2, column=3)
Button(mainWindow, text='Edit Event', padx=10, pady=6, command=lambda: MainFrame('Edit')).grid(row=2, column=5)
Button(mainWindow, text='Update Event', padx=10, pady=6, command=lambda: MainFrame('Update')).grid(row=2, column=7)
Button(mainWindow, text='RESET ALL', padx=10, pady=6, command=ResetAll).grid(row=2, column=9)

users = ['PT', 'Maple', 'Pine', 'Oak', 'Cedar']
user = StringVar()

drop = OptionMenu(mainWindow, user, *users)
drop.pack(padx=15, pady=8)
password = Label(mainWindow, text='Password').pack()
password = Entry(mainWindow)
password.pack(padx=15, pady=8)

def Start(win, ACCESS):
    win.destroy()
    win = Tk()
    win.title('Sports Event Manager')
    win.minsize(800, 600)
    b = Button(win, text='Events', padx=6, pady=10, command=lambda: Event(ACCESS))
    b.grid(row=0, column=0)
    b = Button(win, text='Score', padx=6, pady=10, command=Score)
    b.grid(row=1, column=0)

def CheckPassword(user):
    if password.get() == passwords[user]:
        ACCESS = user
        Start(mainWindow, ACCESS)

b = Button(mainWindow, text='Go', padx=6, pady=10, command=lambda: CheckPassword(user.get())).pack()

mainWindow.mainloop()