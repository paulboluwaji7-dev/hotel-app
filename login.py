from tkinter import*
from tkinter import ttk
import connect
from tkinter import messagebox as msg
import os
#import sqlite3
def manager():
    os.system('python manager.py')

def recept():
    os.system('python rec.py')

def login():
    root.destroy()
    os.system('python intro.py') 


def log():
    username=entn.get()
    password=entp.get()
    role=user_role.get()  
    if username=="" and password==""and role=="":
       msg.showinfo("Alert", "Empty record not allowed, please fill the form!!!")
       return
    connect.con
    connect.cur
    connect.cur.execute(''' select * from users where username=? and password=? and role=?''',(username,password,role))
    result=connect.cur.fetchone()
    if result:
        msg.showinfo("success", "Record found!!!")
        root.destroy()
        if role.lower()=="hotel manager":
            manager()
        elif role.lower()=="receptionist":
            recept()
            return
    else:
        msg.showinfo("Alert", "Unauthorized Login")
    # connect.con.close()               
   
      

root=Tk()
root.title("Login page")
root.geometry('400x400+500+0')
root.configure(background="#0b1120")
root.resizable(0,0)

lblhead=Label(root,text="login Page", font=("verdana",20, "bold" ), bg="#0b1120", fg="#f8fafc")
lblhead.pack(pady=(60,20))

fr=Frame(root, width=200, height=100, bg="#0b1120")
lbln=Label(fr, text="Username:", font=("verdana", 14),bg="#0b1120",fg="#F5F5F5")
lbln.grid(row=0, column=0)
entn=Entry(fr,width=40,relief="flat")
entn.grid(row=0, column=1)

#password
lblp=Label(fr, text="Password:", font=("verdana",14,""), bg="#0b1120",fg="white")
lblp.grid(row=2,column=0)
entp=Entry(fr,width=40, relief="flat", show="*")
entp.grid(row=2, column=1)

#user role
lblr=Label(fr, text="Role:", font=("verdana,14"), bg="#0b1120", fg="white")
lblr.grid(row=3, column=0)
role=["hotel manager", "receptionist"]
user_role=ttk.Combobox(fr,width=38, values=role)
user_role.grid(row=3,column=1)


btnLog=Button(fr,width=15, bg="#22d3ee", fg="#000000", text="login", command=log)
btnLog.grid(row=7, column=1)

already= Button(fr, width=40, bg="#0b1120",fg="white",text="Don't have an account register!",command=login,relief="flat")
already.grid(row=8,column=1)

fr.pack()
root.mainloop()

#pyinstaller --onefile --windowed --add-data "images;images" login.py