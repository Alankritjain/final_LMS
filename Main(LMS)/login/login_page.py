import tkinter as tk
from tkinter import messagebox

# Sample user data for login verification
user_data = {
    "admin": "adminpass"
}

# Main Application Class
class LaundryManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.title("Laundry Management System")

        # Dictionary to hold all page frames
        self.frames = {}

        # Initialize each page and store it in the dictionary
        for Page in (LoginPage, ToDoPage):
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

# Login Page Class
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure the frame's appearance
        self.configure(bg="#71878F")

        # Create Username label and entry
        tk.Label(self, text="Username:", bg="#71878F", fg="white", font=("Arial", 14)).pack(pady=(150, 5))
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack()

        # Create Password label and entry
        tk.Label(self, text="Password:", bg="#71878F", fg="white", font=("Arial", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack()

        # Login Button
        login_button = tk.Button(self, text="Login", command=lambda: self.login(controller), font=("Arial", 12), bg="#5E6F78", fg="white", relief="flat", borderwidth=0)
        login_button.pack(pady=20)

    def login(self, controller):
        """Check if login details are correct and navigate to ToDoPage if valid"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check for valid credentials
        if username in user_data and user_data[username] == password:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            controller.show_frame("ToDoPage")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

# To-Do List Page Class
class ToDoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#9AB0B8")

        # Title label
        tk.Label(self, text="To-Do List Page", font=("Arial", 24), bg="#9AB0B8", fg="black").pack(pady=20)

        # Back button to return to Login Page
        back_button = tk.Button(
            self, text="Back to Login",
            command=lambda: controller.show_frame("LoginPage"),
            bg="#5E6F78",
            fg="white",
            font=("Arial", 12),
            relief="flat",
            borderwidth=0
        )
        back_button.pack(pady=10)

# Run the application
if __name__ == "__main__":
    app = LaundryManagementApp()
    app.mainloop()
