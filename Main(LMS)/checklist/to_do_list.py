import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path

# to_do_list.py
import sqlite3

def create_table():
    conn = sqlite3.connect('laundry_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rest of your ToDoPage class code
# ...
def add_reservation(date):
    conn = sqlite3.connect('laundry_management.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reservations (reservation_date) VALUES (?)", (date,))
    reservation_id = cursor.lastrowid  # Get the ID of the new reservation
    conn.commit()
    conn.close()
    return reservation_id

def add_records(records, reservation_id):
    conn = sqlite3.connect('laundry_management.db')
    cursor = conn.cursor()
    for item_name, quantity in records:
        if quantity.isdigit() and int(quantity) > 0:
            cursor.execute('''
                INSERT INTO reservation_clothes (reservation_id, item_name, quantity)
                VALUES (?, ?, ?)
            ''', (reservation_id, item_name, int(quantity)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "All records added successfully!")
    
    
# Utility function to handle asset paths
def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / Path("assets")
    return ASSETS_PATH / Path(path)

# Function to create the database table


# Function to add multiple records to the database
def add_records(records):
    conn = sqlite3.connect('laundry_management.db')
    cursor = conn.cursor()
    for item_name, quantity in records:
        if quantity.isdigit() and int(quantity) > 0:  # Only add if quantity is greater than 0
            # Check if the item already exists in the table
            cursor.execute("SELECT quantity FROM clothes WHERE item_name = ?", (item_name,))
            result = cursor.fetchone()
            if result:
                # If item exists, update the quantity
                new_quantity = result[0] + int(quantity)
                cursor.execute("UPDATE clothes SET quantity = ? WHERE item_name = ?", (new_quantity, item_name))
            else:
                # If item does not exist, insert as a new row
                cursor.execute("INSERT INTO clothes (item_name, quantity) VALUES (?, ?)", (item_name, int(quantity)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "All records updated successfully!")


# ToDoPage class for multi-page setup
class ToDoPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller  # Main app controller for navigation if in multipage mode

        # Main frame for rounded corners
        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#718690")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title label
        title_label = ctk.CTkLabel(main_frame, text="CHECKLIST", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(pady=20)

        # Load and display the image
        try:
            image_path = relative_to_assets("Figma basics.png")
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            image_label = ctk.CTkLabel(main_frame, image=img, text="")
            image_label.pack(pady=10)
            self.image_label = img  # Keep a reference to avoid garbage collection
        except FileNotFoundError:
            print("Image file not found. Ensure the image is in the 'assets' folder.")

        # Frame for the checklist items
        checklist_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#8B9EA8")
        checklist_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Items and dropdowns
        items = ["Shirt", "T shirt", "Lower", "Jeans", "Shorts", "Dupatta", "Bedsheet", "Pillow cover", "Blanket", "Kurta"]
        self.item_entries = {}

        for i, item in enumerate(items):
            ctk.CTkLabel(checklist_frame, text=item, font=ctk.CTkFont(size=14)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            item_var = ctk.StringVar(value='0')
            dropdown = ctk.CTkComboBox(checklist_frame, variable=item_var, values=[str(x) for x in range(0, 21)], width=60)
            dropdown.grid(row=i, column=1, padx=10, pady=5)
            self.item_entries[item] = item_var

        # Submit button placed at the top-right corner
        submit_button = ctk.CTkButton(main_frame, text="Submit", command=self.submit_and_go_to_reservation, fg_color="#5E6F78", font=ctk.CTkFont(size=14, weight="bold"))
        submit_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Adjust x and y for precise positioning

    def submit_and_go_to_reservation(self):
        """Add records to the database and navigate to ReservationPage."""
        records_to_add = [(item, entry.get()) for item, entry in self.item_entries.items()]
        add_records(records_to_add)

        # Navigate to ReservationPage if in multipage mode
        if self.controller:
            self.controller.show_frame("ReservationPage")

# Initialize the database table (this should be done once at startup)
create_table()

# Standalone Mode
if __name__ == "__main__":
    # CustomTkinter Setup
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # GUI Setup
    root = ctk.CTk()
    root.title("Clothes Checklist")
    root.geometry("500x700")  # Adjusted height to fit the image

    # Instantiate and pack ToDoPage directly for standalone testing
    todo_page = ToDoPage(root)
    todo_page.pack(fill="both", expand=True)

    # Start the main event loop
    root.mainloop()
