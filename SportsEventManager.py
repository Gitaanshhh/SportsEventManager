"""
Imports
"""
import mysql.connector as sql
from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry

ACCESS = False

"""
DATABASE PART
"""
def connectsql():
    global conn, c
    conn = sql.connect(host='localhost', user='root', passwd='rootpw')
    c = conn.cursor()
    c.execute("USE Git;")
    return conn, c

conn, c = connectsql()
try:
    c.execute("CREATE DATABASE Git")
except sql.Error as err:
    print("Failed creating database: {}".format(err))

c.execute("USE Git;")
if conn.is_connected():
    print('connected.')

def sqltable(x):
    try:
        c.execute(f"CREATE TABLE {x} (Sport char(11) PRIMARY KEY, MainPL integer, SubPL integer, event date, FIRST char(5), SECOND char(5), THIRD char(5), FOURTH char(5));")
    except sql.Error as err:
        print("Table already exists: {}".format(err))

sqltable('U19M')
sqltable('U19F')
sqltable('U17M')
sqltable('U17F')
sqltable('U14M')
sqltable('U14F')
sqltable('U12M')
sqltable('U12F')

conn.commit()
conn.close()

# PASSWORDS
pws = {'PT': 'pt', 'Maple': 'maple', 'Pine': 'pine', 'Oak': 'oak', 'Cedar': 'cedar'}

win = Tk()
win.title('Gitaansh is Great')
win.minsize(800, 600)

def forget(widget):
    widget.grid_forget()

def submit1(cat, gen, name, pl, sub, cal):
    conn, c = connectsql()
    c.execute(f"INSERT INTO {cat.get()+gen.get()} (Sport, MainPL, SubPL, event) VALUES ('{name.get()}', {int(pl.get())}, {int(sub.get())}, '{cal.get_date()}');")
    conn.commit()
    conn.close()
    name.delete(0, END)
    pl.delete(0, END)
    sub.delete(0, END)
    cal.delete(0, END)

def getevent():
    wine = Toplevel()
    wine.title('New Event')
    wine.minsize(800, 600)

    l = Label(wine, text='Enter the following details').grid(row=1, column=1)
    lname = Label(wine, text='Name:')
    ename = Entry(wine)
    lpl = Label(wine, text='Number of Players')
    epl = Entry(wine)
    esubs = Entry(wine)
    CAT = StringVar()
    GEN = StringVar()

    cal = DateEntry(wine, selectmode='day')
    cal.delete(0, END)

    dropCAT = OptionMenu(wine, CAT, 'U19', 'U17', 'U14', 'U12')
    dropGEN = OptionMenu(wine, GEN, 'M', 'F')

    lname.grid(row=2, column=1)
    ename.grid(row=2, column=2)
    lpl.grid(row=3, column=1)
    epl.grid(row=3, column=2)
    esubs.grid(row=3, column=4)
    dropCAT.grid(row=4, column=1)
    dropGEN.grid(row=4, column=3)
    cal.grid(row=5, column=2)

    Button(wine, text='Clear Date', padx=10, pady=6, command=lambda: cal.delete(0, END)).grid(row=5, column=3)
    space = Label(text=' ').grid(row=6, columnspan=3)
    Button(wine, text='Submit', padx=15, pady=10, command=lambda: submit1(CAT, GEN, ename, epl, esubs, cal)).grid(row=7, column=2)

def dispevent():
    w = Toplevel()
    w.title('EVENTS : ')
    w.minsize(700, 500)
    conn, c = connectsql()

    def display(age, col):
        row = 1
        c.execute(f"SELECT * FROM {age}M")
        m = c.fetchall()
        c.execute(f"SELECT * FROM {age}F")
        f = c.fetchall()

        Label(w, text=f'{age}M').grid(row=1, column=col)
        for x in range(len(m)):
            Label(w, text=m[x][:4]).grid(row=1+x+1, column=col)
            row = 1+x+1
        Label(w, text=' ').grid(row=row + 1, column=col)
        Label(w, text=f'{age}F').grid(row=row + 2, column=col)
        for x in range(len(f)):
            Label(w, text=f[x][:4]).grid(row=2 + row + 1 + x, column=col)
        Label(w, text=' ').grid(row=1, column=col+1)

    display('U19', 1)
    display('U17', 3)
    display('U14', 5)
    display('U12', 7)

    conn.commit()
    conn.close()

def search(cat, gen, w, task):
    conn, c = connectsql()
    c.execute(f"SELECT * FROM {cat.get()+gen.get()};")
    data = c.fetchall()
    for a in range(len(data)):
        data[a] = data[a][0]
    x = StringVar()
    drop = OptionMenu(w, x, *data)
    drop.grid(row=6, column=4)
    c.close()

    def up():
        Label(w, text='First').grid(row=7, column=1)
        Label(w, text='Second').grid(row=7, column=2)
        Label(w, text='Third').grid(row=7, column=3)
        Label(w, text='Fourth').grid(row=7, column=4)
        global I, II, III, IV
        I = StringVar()
        II = StringVar()
        III = StringVar()
        IV = StringVar()
        houselist = ['Maple', 'Oak', 'Pine', 'Cedar']
        OptionMenu(w, I, *houselist).grid(row=8, column=1)
        OptionMenu(w, II, *houselist).grid(row=8, column=2)
        OptionMenu(w, III, *houselist).grid(row=8, column=3)
        OptionMenu(w, IV, *houselist).grid(row=8, column=4)

    def edit(task):
        Label(w, text='Name:').grid(row=9, column=1)
        name = Entry(w)
        Label(w, text='Number of Players').grid(row=10, column=1)
        pl = Entry(w)
        subs = Entry(w)
        CAT = StringVar()
        GEN = StringVar()
        dropCAT = OptionMenu(w, CAT, 'U19', 'U17', 'U14', 'U12')
        dropGEN = OptionMenu(w, GEN, 'M', 'F')
        cal = DateEntry(w, selectmode='day')
        cal.delete(0, END)

        name.grid(row=9, column=2)
        pl.grid(row=10, column=2)
        subs.grid(row=10, column=4)
        dropCAT.grid(row=11, column=1)
        dropGEN.grid(row=11, column=3)
        cal.grid(row=12, column=2)

        def submit2(CAT, GEN, name, pl, sub, iname, cal):
            conn, c = connectsql()
            c.execute(f"DELETE FROM {cat.get()+gen.get()} WHERE Sport = '{x.get()}';")
            c.execute(f"INSERT INTO {CAT.get()+GEN.get()} (Sport, MainPL, SubPL, event) VALUES ('{name.get()}', {int(pl.get())}, {int(sub.get())}, '{cal.get_date()}');")
            name.delete(0, END)
            pl.delete(0, END)
            sub.delete(0, END)
            conn.commit()
            conn.close()

        Button(w, text='Clear Date', padx=10, pady=6, command=lambda: cal.delete(0, END)).grid(row=12, column=4)
        Button(w, text='Submit', padx=6, pady=10, command=lambda: submit2(CAT, GEN, name, pl, subs, x, cal)).grid(row=12, column=3)
        if task == 'Edit':
            Button(w, text='Remove', padx=6, pady=10, command=delete).grid(row=15, column=5)

    def submit():
        conn, c = connectsql()
        c.execute(f"UPDATE {cat.get()+gen.get()} SET FIRST = '{I.get()}', SECOND = '{II.get()}', THIRD = '{III.get()}', FOURTH = '{IV.get()}' WHERE Sport = '{x.get()}';")
        w.destroy()
        conn.commit()
        conn.close()

    def delete():
        conn, c = connectsql()
        c.execute(f"DELETE FROM {cat.get()+gen.get()} WHERE Sport = '{x.get()}';")
        w.destroy()
        conn.commit()
        conn.close()

    if task == 'Update':
        Button(w, text='Go', padx=6, pady=10, command=up).grid(row=6, column=5)
        Button

(w, text='Submit', padx=6, pady=10, command=submit).grid(row=8, column=5)
    if task == 'Edit':
        Button(w, text='Go', padx=6, pady=10, command=lambda: edit('Edit')).grid(row=6, column=5)

    conn.close()

def mainframe(task):
    frame = Toplevel()
    frame.minsize(400, 300)

    def login(x):
        global ACCESS
        if x in pws.keys() and epw.get() == pws[x]:
            ACCESS = True
            if task == 'Update':
                search(cat, gen, frame, 'Update')
            elif task == 'Edit':
                search(cat, gen, frame, 'Edit')
            frame.destroy()

    Label(frame, text='Enter password to access').grid(row=1, column=2)
    epw = Entry(frame)
    epw.grid(row=2, column=2)

    house = StringVar()
    drop = OptionMenu(frame, house, *pws.keys())
    drop.grid(row=2, column=3)
    Button(frame, text='Submit', padx=6, pady=10, command=lambda: login(house.get())).grid(row=2, column=4)

    if ACCESS and task == 'Update':
        search(cat, gen, win, 'Update')
    elif ACCESS and task == 'Edit':
        search(cat, gen, win, 'Edit')

def resetall():
    w = Toplevel()
    w.title('RESET ALL : ')
    w.minsize(600, 500)

    def resetallf(x):
        conn, c = connectsql()
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

    OptionMenu(w, CAT, 'U19', 'U17', 'U14', 'U12').grid(row=2, column=2)
    OptionMenu(w, GEN, 'M', 'F').grid(row=2, column=3)

    Button(w, text='RESET ALL', padx=20, pady=10, command=lambda: resetallf(CAT)).grid(row=2, column=5)

Button(win, text='New Event', padx=10, pady=6, command=getevent).grid(row=2, column=2)
Button(win, text='View Event', padx=10, pady=6, command=dispevent).grid(row=2, column=3)
Button(win, text='Edit Event', padx=10, pady=6, command=lambda: mainframe('Edit')).grid(row=2, column=5)
Button(win, text='Update Event', padx=10, pady=6, command=lambda: mainframe('Update')).grid(row=2, column=7)
Button(win, text='RESET ALL', padx=10, pady=6, command=resetall).grid(row=2, column=9)

win.mainloop()