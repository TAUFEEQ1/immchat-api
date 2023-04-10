import sqlite3

# Connect to database
conn = sqlite3.connect('new_qa.db')

# Create table
conn.execute('''CREATE TABLE IF NOT EXISTS applications
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              applicationId TEXT,
              email_address TEXT,
              type TEXT,
              category TEXT,
              subcategory TEXT);''')

# Commit changes and close connection
conn.commit()
conn.close()
