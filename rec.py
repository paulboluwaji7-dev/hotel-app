import tkinter
from PIL import Image,ImageTk
from tkinter import ttk
import connect
from datetime import datetime
from tkinter import messagebox as msg
#import sqlite3

class hotel_app():
    def __init__(self,root):
        self.root=root

        self.root.title("Receptionist Account")
        self.root.geometry('1260x1200+0+0')
        self.root.configure(bg="#fff")
        self.style=ttk.Style()
        self.main_ui()

    def main_ui(self):
        img=Image.open('images/logo.jpg')
        img=img.resize((200,100))
        img_tk=ImageTk.PhotoImage(img)
        img=Image.open('images/logo.jpg')
        img=img.resize((200,100))
        img_tk=ImageTk.PhotoImage(img)

        self.head=ttk.Frame(self.root,padding=12)
        self.head.pack(fill="x")
                # Create a label and keep a reference to the image
        lbl=tkinter.Label(self.head, image=img_tk)
        lbl.image = img_tk  # Keep a reference to avoid garbage collection
        lbl.place(x=0, y=0)
        
        ttk.Label(
                    self.head,text="HOTEL MANAGEMENT SYSTEM",font=("verdana",20,"bold"),
                    foreground="#000"
                    ).pack(side="top")
        
        ttk.Label(self.head,text="logged in",font=("verdana",10,"bold"),
                ).pack(side="right", padx=10)
        ttk.Button(self.head,text="log out",command=self.logout).pack(side="right", padx=10)

        self.notebook=ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.guests_tab=ttk.Frame(self.notebook,padding=15)
        self.checkin_tab=ttk.Frame(self.notebook,padding=15)
        self.checkout_tab=ttk.Frame(self.notebook,padding=15)

        self.notebook.add(self.guests_tab,text="Guests")
        self.notebook.add(self.checkin_tab,text="Check-in/Allocation")
        self.notebook.add(self.checkout_tab,text="Check-out")

        self.build_guests()
        self.build_checkin()
        self.build_checkout()

    def refreshall(self): 
        self.build_guests()
        self.build_checkin()
        self.build_checkout()  

    def logout(self):
          if msg.askyesno("Logout", "Are you sure u want to log out?"):
              root.destroy()
              return

    def build_guests(self):
         form = ttk.LabelFrame(self.guests_tab, text="Guest Information", padding=12)
         form.pack(fill="x")
    
         labels = ["Full Name", "Phone", "Email", "Address"]
         self.guest_entries = []
    
         for i, label in enumerate(labels):
                ttk.Label(form, text=label).grid(row=0, column=i*2, padx=5)
                e = ttk.Entry(form, width=22)
                e.grid(row=0, column=i*2+1, padx=5)
                self.guest_entries.append(e)
    
         ttk.Button(
                form, text="Add Guest", command=self.add_guest ).grid(row=0, column=8, padx=10)
    
         cols = ("id", "name", "phone", "email", "address")
         self.guest_tree = ttk.Treeview(
                self.guests_tab, columns=cols, show="headings", height=18
            )
         for c, text, width in [
                ("id", "ID", 20), ("name", "Full Name", 60),
                ("phone", "Phone", 80), ("email", "Email", 60),
                ("address", "Address", 200)
            ]:
                   self.guest_tree.heading(c, text=text)
                   self.guest_tree.column(c, width=width)
                   self. refresh_guests()
                   self.guest_tree.pack(fill="both", expand=True, pady=12)

    def add_guest(self):
            values = [e.get().strip() for e in self.guest_entries]
    
            if not values[0]:
             msg.showwarning("Validation", "Guest name is required.")
             return
            if "@" not in values[2]:
                msg.showwarning("Validation", "Please enter a valid email address.")
                return
    
            
            connect.con
            connect.cur
            connect.cur.execute(
                   "INSERT INTO guests(full_name,phone,email,address) VALUES(?,?,?,?)",values
                    
            )
            connect.con.commit()
            # msg.showinfo("success","Submitted successfully")
            # connect.con.close()
    
            for e in self.guest_entries:
                 e.delete(0, "end")
    
            msg.showinfo("Success", "Guest registered.")
            self.refresh_guests()

    def refresh_guests(self):
            for item in self.guest_tree.get_children():
                 self.guest_tree.delete(item)
    
            connect.con 
            connect.cur 
            rows=connect.cur.execute("select * from guests order by id").fetchall()
                    
            
    
            # connect.con.close()
    
            for r in rows:
                 self.guest_tree.insert("", "end", values=(r[0],r[1], r[2], r[3], r[4]))

    def build_checkin(self):
            form = ttk.LabelFrame(
                self.checkin_tab,
                text="Room Allocation and Guest Check-In",
                padding=15
            )
            form.pack(fill="x")
    
            ttk.Label(form, text="Guest").grid(row=0, column=0, padx=5, pady=8)
            self.checkin_guest = ttk.Combobox(form, state="readonly", width=35)
            self.checkin_guest.grid(row=0, column=1, padx=5)
    
            ttk.Label(form, text="available Room").grid(row=0, column=2, padx=5)
            self.checkin_room = ttk.Combobox(form, state="readonly", width=40)
            self.checkin_room.grid(row=0, column=3, padx=5)
    
            ttk.Label(form, text="Adults").grid(row=1, column=0, padx=5)
            self.adults = ttk.Spinbox(form, from_=1, to=20, width=8)
            self.adults.grid(row=1, column=1, sticky="w", padx=5)
            self.adults.set(1)
    
            ttk.Label(form, text="Children").grid(row=1, column=2, padx=5)
            self.children = ttk.Spinbox(form, from_=0, to=20, width=8)
            self.children.grid(row=1, column=3, sticky="w", padx=5)
            self.children.set(0)
    
            ttk.Button(
                form, text="CHECK IN / ALLOCATE ROOM",
                command=self.check_in
            ).grid(row=2, column=0, columnspan=4, pady=15)
    
            ttk.Button(
                form, text="Refresh available Rooms",
                command=self.refresh_checkin_options
            ).grid(row=2, column=4, padx=10)
    
            cols = (
                "id", "guest", "room", "type",
                "checkin", "adults", "children", "total", "status"
            )
            self.booking_tree = ttk.Treeview(
                self.checkin_tab, columns=cols, show="headings", height=15
            )
    
            for c, text, width in [
                ("id", "ID", 50), ("guest", "Guest", 180),
                ("room", "Room", 80), ("type", "Type", 100),
                ("checkin", "Check-In", 150), ("adults", "Adults", 70),
                ("children", "Children", 80), ("total", "Total", 100),
                ("status", "Status", 100)
            ]:
                self.booking_tree.heading(c, text=text)
                self.booking_tree.column(c, width=width)
    
            self.refresh_checkin_options()
            self.refreshcheckin()
            self.booking_tree.pack(fill="both", expand=True, pady=12)

    def check_in(self):   
            guest_value = self.checkin_guest.get()
            room_value = self.checkin_room.get()
    
            if not guest_value or not room_value:
                msg.showwarning(
                    "Validation", "Select a guest and an available room."
                )
                return
    
            guest_id = int(guest_value.split("|")[0])
            room_id = int(room_value.split("|")[0])
    
            try:
                adults = int(self.adults.get())
                children = int(self.children.get())
            except ValueError:
                msg.showerror("Validation", "Adults and children must be numbers.")
                return
    
            connect.con
            connect.cur
            room = connect.cur.execute(
                "SELECT * FROM rooms WHERE id=? AND status='available'",
                (room_id,)
            ).fetchone()
    
            if not room:
                # connect.con.close()
                msg.showerror("Error", "Room is no longer available.")
                # self.refreshall()
                return
    
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
            connect.cur.execute("""
                INSERT INTO bookings
                (guest_id,room_id,checkin,adults,children,status,total,created_at)
                VALUES(?,?,?,?,?,'Checked In',?,?)
            """, (guest_id, room_id, now, adults, children, room[3], now))
    
            connect.cur.execute(
                "UPDATE rooms SET status='Occupied' WHERE id=?",
                (room_id,)
            )
    
            connect.con.commit()
    
    
            msg.showinfo(
                "Check-In Successful",
                f"Guest checked in.\nRoom: {room[1]}\n"
                f"Rate: ₦{room[3]:,.2f} per night"
            )
            # self.refreshall()
            
    def refreshcheckin(self):
            for item in self.booking_tree.get_children():
                        self.booking_tree.delete(item)
            
            connect.con
            connect.cur
            rows = connect.cur.execute("""
                        SELECT b.*, g.full_name, r.room_no, r.room_type, r.price,b.children
                        FROM bookings b
                        JOIN guests g ON g.id=b.guest_id
                        JOIN rooms r ON r.id=b.room_id
                        WHERE b.status='Checked In'
                        ORDER BY b.id DESC
                    """).fetchall()
                    # conn.close()
            
            today = datetime.now().date()
            
            for b in rows:
                        checkin_date = datetime.strptime(
                            b["checkin"], "%Y-%m-%d %H:%M:%S"
                        ).date()
                        nights = max(1, (today - checkin_date).days)
                        estimated = nights * b["price"]
            
                        self.booking_tree.insert(
                            "", "end",
                            values=(
                                b["id"], b["full_name"], b["room_no"],
                                b["room_type"], b["checkin"], nights,
                                b['children'],
                                f"₦{estimated:,.2f}",
                                b["status"]
                            )
                        )

    def refresh_checkin_options(self):
            connect.con
            connect.cur
    
            guests = connect.cur.execute(
                "SELECT id,full_name,phone,email,address FROM guests ORDER BY full_name"
            ).fetchall()
    
            rooms = connect.cur.execute("""
                SELECT id,room_no,room_type,price
                FROM rooms
                WHERE status='available'
                ORDER BY room_no
            """).fetchall()
    
            # conn.close()
    
            self.checkin_guest["values"] = [
                f"{g[0]} | {g[1]} | {g[2]}| {g[3]}| {g[4]}"
                for g in guests
            ]
    
            self.checkin_room["values"] = [
                f"{r[0]} | Room {r[1]} | {r[2]} | ₦{r[3]:,.2f}"
                for r in rooms
            ]
    
            if self.checkin_guest["values"] and not self.checkin_guest.get():
                self.checkin_guest.current(0)
    
            if self.checkin_room["values"] and not self.checkin_room.get():
                self.checkin_room.current(0)

    def build_checkout(self):
            ttk.Label(
                self.checkout_tab,
                text="Active Guests /check-out",
                font=("Arial", 18, "bold")
            ).pack(anchor="w")
    
            cols=(
                "id", "guest", "room", "type", "checkin",
                "nights", "rate", "total", "status"
            )
            self.checkout_tree=ttk.Treeview(
                self.checkout_tab, columns=cols, show="headings", height=15
            )
            for c, text, width in[
                  ("id", "Booking", 70), ("guest", "Guest", 190),
                ("room", "Room", 80), ("type", "Type", 100),
                ("checkin", "Check-In", 150), ("nights", "Nights", 80),
                ("rate", "Rate", 100), ("total", "Estimated Total", 130),
                ("status", "Status", 100)
            ]:
             self.checkout_tree.heading(c, text=text)
             self.checkout_tree.column(c, width=width)
    
             self.checkout_tree.pack(fill="both", pady=15)
    
    
            ttk.Button(
                self.checkout_tab,
                text="CHECK OUT SELECTED GUEST",
                command=self.check_out
            ).pack(anchor="e")
    
            self.refresh_checkout()

    def refresh_checkout(self):
            for item in self.checkout_tree.get_children():
                self.checkout_tree.delete(item)
    
            connect.con
            connect.cur
            rows = connect.cur.execute("""
                SELECT b.*, g.full_name, r.room_no, r.room_type, r.price
                FROM bookings b
                JOIN guests g ON g.id=b.guest_id
                JOIN rooms r ON r.id=b.room_id
                WHERE b.status='Checked In'
                ORDER BY b.id DESC
            """).fetchall()
            # conn.close()
    
            today = datetime.now().date()
    
            for b in rows:
                checkin_date = datetime.strptime(
                    b["checkin"], "%Y-%m-%d %H:%M:%S"
                ).date()
                nights = max(1, (today - checkin_date).days)
                estimated = nights * b["price"]
    
                self.checkout_tree.insert(
                    "", "end",
                    values=(
                        b["id"], b["full_name"], b["room_no"],
                        b["room_type"], b["checkin"], nights,
                        f"₦{b['price']:,.2f}",
                        f"{estimated:,.2f}",
                        b["status"]
                    )
                )

    def check_out(self):
            selected = self.checkout_tree.selection()
    
            if not selected:
                msg.showwarning("Select", "Select at least one booking to check out.")
                return
    
            # Collect selected bookings
            bookings_selected = []
    
            for item in selected:
                values = self.checkout_tree.item(item)["values"]
    
                bookings_selected.append({
                    "id": values[0],
                    "guest": values[1],
                    "room_no": values[2],
                    "total": values[7]
                })
    
            # Confirmation message
            details = "\n".join(
                f"• {b['guest']} - Room {b['room_no']}"
                for b in bookings_selected
            )
    
            if not msg.askyesno(
                "Confirm Check-Out",
                f"Check out the following {len(bookings_selected)} booking(s)?\n\n"
                f"{details}"
            ):
                return
    
            try:
                checkout = datetime.now()
                checkout_str = checkout.strftime("%Y-%m-%d %H:%M:%S")
    
                checkout_results = []
    
                for b in bookings_selected:
    
                    booking = connect.cur.execute(
                        """
                        SELECT room_id, checkin
                        FROM bookings
                        WHERE id=? AND status='Checked In'
                        """,
                        (b["id"],)
                    ).fetchone()
    
                    # Booking may have already been checked out
                    if not booking:
                        continue
    
                    checkin_dt = datetime.strptime(
                        booking["checkin"],
                        "%Y-%m-%d %H:%M:%S"
                    )
    
                    # Calculate number of nights
                    nights = max(
                        1,
                        (checkout.date() - checkin_dt.date()).days
                    )
    
                    # Get room price
                    room = connect.cur.execute(
                        """
                        SELECT price
                        FROM rooms
                        WHERE id=?
                        """,
                        (booking["room_id"],)
                    ).fetchone()
    
                    if not room:
                        continue
    
                    final_total = nights * room["price"]
    
                    # Update booking
                    connect.cur.execute(
                        """
                        UPDATE bookings
                        SET checkout=?,
                            status='Checked Out',
                            total=?
                        WHERE id=?
                        """,
                        (
                            checkout_str,
                            final_total,
                            b["id"]
                        )
                    )
    
                    # Make room available
                    connect.cur.execute(
                        """
                        UPDATE rooms
                        SET status='available'
                        WHERE id=?
                        """,
                        (booking["room_id"],)
                    )
    
                    checkout_results.append({
                        "guest": b["guest"],
                        "room_no": b["room_no"],
                        "nights": nights,
                        "total": final_total
                    })
    
                # Save all changes at once
                connect.con.commit()
    
                if not checkout_results:
                    msg.showerror(
                        "Error",
                        "None of the selected bookings are still active."
                    )
                    # self.refresh_all()
                    return
    
                # Calculate grand total
                grand_total = sum(
                    item["total"] for item in checkout_results
                )
    
                # Create result message
                result = ""
    
                for item in checkout_results:
                    result += (
                        f"Guest: {item['guest']}\n"
                        f"Room: {item['room_no']}\n"
                        f"Nights: {item['nights']}\n"
                        f"Bill: ₦{item['total']:,.2f}\n"
                        f"{'-' * 35}\n"
                    )
    
                result += f"\nGRAND TOTAL: ₦{grand_total:,.2f}"
    
                msg.showinfo(
                    "Check-Out Complete",
                    f"{len(checkout_results)} booking(s) checked out successfully.\n\n"
                    f"{result}"
                )
    
                # Refresh Treeview
                # self.refresh_all()
    
            except Exception as e:
                connect.con.rollback()
    
                msg.showerror(
                    "Check-Out Error",
                    f"An error occurred during check-out:\n\n{e}"
                )
            # Collect selected bookings
                bookings_selected = []
    
                for item in selected:
                    values = self.checkout_tree.item(item)["values"]
    
                    bookings_selected.append({
                        "id": values[0],
                        "guest": values[1],
                        "room_no": values[2],
                        "total": values[7]
                    })
    
                    # Confirmation message
                    details = "\n".join(
                        f"• {b['guest']} - Room {b['room_no']}"
                        for b in bookings_selected
                    )
    
                    if not msg.askyesno(
                        "Confirm Check-Out",
                        f"Check out the following {len(bookings_selected)} booking(s)?\n\n"
                        f"{details}"
                    ):
                        return
    
                try:
                    connect.cur.execute(
                        """
                        UPDATE rooms
                        SET status='available'
                        WHERE id=?
                        """,
                        (booking["room_id"],)
                    )
    
                    checkout_results.append({
                        "guest": b["guest"],
                        "room_no": b["room_no"],
                        "nights": nights,
                        "total": final_total
                    })
    
                # Save all changes at once
                    connect.con.commit()
    
                    if not checkout_results:
                        msg.showerror(
                            "Error",
                            "None of the selected bookings are still active."
                        )
                        self.refresh_all()
                        return
    
                    # Calculate grand total
                    grand_total = sum(
                        item["total"] for item in checkout_results
                    )
    
                    # Create result message
                    result = ""
    
                    for item in checkout_results:
                        result += (
                            f"Guest: {item['guest']}\n"
                            f"Room: {item['room_no']}\n"
                            f"Nights: {item['nights']}\n"
                            f"Bill: ₦{item['total']:,.2f}\n"
                            f"{'-' * 35}\n"
                        )
    
                    result += f"\nGRAND TOTAL: ₦{grand_total:,.2f}"
    
                    msg.showinfo(
                        "Check-Out Complete",
                        f"{len(checkout_results)} booking(s) checked out successfully.\n\n"
                        f"{result}"
                    )
    
                    # Refresh Treeview
                    self.refresh_all()
    
                except Exception as e:
                    connect.con.rollback()
    
                msg.showerror(
                    "Check-Out Error",
                    f"An error occurred during check-out:\n\n{e}"
                )                                                     
             
                                                        
               
             





#root.resizable(0,0)
__name__=="__main__"
root=tkinter.Tk()
hotel_app(root)
root.mainloop()