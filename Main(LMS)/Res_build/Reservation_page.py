import tkinter as tk
from tkinter import ttk, PhotoImage, Canvas, Button, Label, Frame
from tkcalendar import Calendar
from pathlib import Path
import sqlite3

# Utility function to handle asset paths
def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / Path(r"C:\Users\alankritjain\OneDrive - BENNETT UNIVERSITY\python project\build\assets\frame0")
    return ASSETS_PATH / Path(path)

# Function to initialize the database and create a reservations table if it doesn’t exist
def initialize_database():
    conn = sqlite3.connect("laundry_management.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            hour TEXT NOT NULL,
            minute TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Main Application Class to control navigation
class LaundryManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x900")
        self.configure(bg="#FFFFFF")
        self.title("Laundry Management System")
        
        # Dictionary to hold all page frames
        self.frames = {}

        # Initialize the database at the start
        initialize_database()

        # Initialize each page and store it in the dictionary
        for Page in (ReservationPage, TrackerPage):  # Add all pages here
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the ReservationPage initially
        self.show_frame("ReservationPage")

    def show_frame(self, page_name):
        """Raise a frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()

# Reservation Page Class with calendar and time selection widgets
class ReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Main app controller for navigation

        # Canvas setup for the Reservation Page
        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=900,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.pack(fill="both", expand=True)

        # Creating background rectangles and text
        canvas.create_rectangle(287.0, 21.0, 1153.0, 173.0, fill="#FFFFFF", outline="")
        canvas.create_text(431.0, 63.0, anchor="nw", text="RESERVATION PAGE", fill="#000000", font=("Roboto Bold", 64 * -1))

        # Button image setup and button creation
        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(
            self,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.submit_reservation,  # Update command to submit data
            relief="flat"
        )
        button_3.image = button_image_3  # Keep a reference to avoid garbage collection
        button_3.place(x=553.0, y=712.0, width=763.0, height=73.0)

        # Black box to contain the calendar and time selectors
        black_box = Frame(self, width=803, height=451, bg="black")
        black_box.place(x=533, y=224)

        # Center coordinates for positioning within the black box
        center_x = 803 // 2
        center_y = 451 // 2

        # Calendar widget for selecting a date
        self.calendar = Calendar(black_box, selectmode='day', year=2024, month=11, day=10)
        self.calendar.place(x=center_x - 125, y=center_y - 150)

        # Combobox for selecting hour and minute
        self.hour_combobox = ttk.Combobox(black_box, values=[f"{i:02}" for i in range(24)], width=5)
        self.hour_combobox.set("00")
        self.hour_combobox.place(x=center_x - 50, y=center_y + 20)

        self.minute_combobox = ttk.Combobox(black_box, values=[f"{i:02}" for i in range(0, 60, 5)], width=5)
        self.minute_combobox.set("00")
        self.minute_combobox.place(x=center_x + 30, y=center_y + 20)

        # Button to display selected date and time
        show_button = Button(black_box, text="Show Selected Date & Time", command=self.show_selected_datetime)
        show_button.place(x=center_x - 70, y=center_y + 70)

        # Label to display selected date and time
        self.date_time_label = Label(black_box, text="No date and time selected", font=("Arial", 12), bg="white", fg="black")
        self.date_time_label.place(x=center_x - 100, y=center_y + 120)

        # Button to go to Tracker Page
        go_to_tracker_button = Button(self, text="Go to Tracker Page", 
                                      command=lambda: controller.show_frame("TrackerPage"))
        go_to_tracker_button.place(x=1200, y=100)

    def submit_reservation(self):
        """Submit the selected date and time to the database."""
        # Get the selected date and time
        selected_date = self.calendar.get_date()
        selected_hour = self.hour_combobox.get()
        selected_minute = self.minute_combobox.get()

        # Connect to the SQLite database and save the reservation
        conn = sqlite3.connect("laundry_management.db")
        cursor = conn.cursor()
        
        # Insert data into the reservations table
        cursor.execute('''
            INSERT INTO reservations (date, hour, minute)
            VALUES (?, ?, ?)
        ''', (selected_date, selected_hour, selected_minute))

        # Commit and close the database connection
        conn.commit()
        conn.close()

        # Update the label to show that the reservation was saved
        self.date_time_label.config(text="Reservation saved successfully!")

    def show_selected_datetime(self):
        # Display the selected date and time
        selected_date = self.calendar.get_date()
        selected_hour = self.hour_combobox.get()
        selected_minute = self.minute_combobox.get()
        self.date_time_label.config(text=f"Selected Date and Time: {selected_date} {selected_hour}:{selected_minute}")
        
def fetch_clothes_for_reservation(reservation_id):
    conn = sqlite3.connect('laundry_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT item_name, quantity FROM reservation_clothes WHERE reservation_id = ?
    ''', (reservation_id,))
    items = cursor.fetchall()
    conn.close()
    return items

# Tracker Page Class
class TrackerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title for Tracker Page
        Label(self, text="Tracker Page", font=("Arial", 24)).pack(pady=20)

        # Button to go back to Reservation Page
        Button(self, text="Back to Reservation Page", 
               command=lambda: controller.show_frame("ReservationPage")).pack(pady=10)

# Run the application
if __name__ == "__main__":
    app = LaundryManagementApp()
    app.mainloop()
