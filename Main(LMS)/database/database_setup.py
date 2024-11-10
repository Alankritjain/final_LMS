import sqlite3

def create_tables():
    conn = sqlite3.connect('laundry_management.db')
    cursor = conn.cursor()

    # Table for reservations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_date TEXT NOT NULL
        )
    ''')

    # Table for clothes linked to each reservation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservation_clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (reservation_id) REFERENCES reservations (reservation_id)
        )
    ''')
    conn.commit()
    conn.close()

# Call this function to initialize the tables
if __name__ == "__main__":
    create_tables()
