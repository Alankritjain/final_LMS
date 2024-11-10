import tkinter as tk
from login.login_page import LoginPage  # Adjust path based on your folder structure
from checklist.to_do_list import ToDoPage  # Adjust path based on your folder structure
from Res_build.Reservation_page import ReservationPage  # Adjust path based on your folder structure
from database.database_setup import create_tables  # Import create_tables

class LaundryManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")  # Adjusted size for better layout
        self.title("Laundry Management System")

        # Ensure all database tables are created before any page loads
        create_tables()

        # Dictionary to hold all page frames
        self.frames = {}

        # Initialize each page and store it in the dictionary
        for Page in (LoginPage, ToDoPage, ReservationPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the LoginPage initially
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Bring a specified frame to the front"""
        frame = self.frames[page_name]
        frame.tkraise()

# Run the application
if __name__ == "__main__":
    app = LaundryManagementApp()
    app.mainloop()
