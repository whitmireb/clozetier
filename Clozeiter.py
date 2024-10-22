import sqlite3

# Database setup: Create a SQLite database to store clothing items
def setup_database():
    conn = sqlite3.connect('closet.db')
    cursor = conn.cursor()
    
    # Create a table for the digital closet (if it doesn't already exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS closet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        item_type TEXT NOT NULL,
        color TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Add clothing item to the closet
def add_clothing(item_name, item_type, color):
    conn = sqlite3.connect('closet.db')
    cursor = conn.cursor()
    
    # Insert new clothing item into the closet table
    cursor.execute('''
    INSERT INTO closet (item_name, item_type, color) VALUES (?, ?, ?)
    ''', (item_name, item_type, color))
    
    conn.commit()
    conn.close()

# Display all clothing items in the closet
def display_closet():
    conn = sqlite3.connect('closet.db')
    cursor = conn.cursor()
    
    # Retrieve all items from the closet table
    cursor.execute('SELECT * FROM closet')
    items = cursor.fetchall()
    
    # Display the closet's contents
    if items:
        print("Closet contains the following items:")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Type: {item[2]}, Color: {item[3]}")
    else:
        print("The closet is currently empty.")
    
    conn.close()

# Delete clothing item from the closet by ID
def delete_clothing(item_id):
    conn = sqlite3.connect('closet.db')
    cursor = conn.cursor()
    
    # Delete the item with the given ID
    cursor.execute('DELETE FROM closet WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    print(f"Item with ID {item_id} has been deleted.")

# Function to simulate user input for adding and displaying items
def run_closet_simulation():
    setup_database()
    
    while True:
        print("\n1. Add Clothing Item")
        print("2. Display Closet")
        print("3. Delete Clothing Item")
        print("4. Exit")
        
        choice = input("Choose an option: ").strip()  # Use .strip() to remove any leading/trailing spaces
        print(f"Debug: You entered '{choice}'")  # Debugging line to see the exact input
        
        if choice == '1':
            name = input("Enter the clothing item name: ")
            item_type = input("Enter the type of clothing (e.g., shirt, pants, jacket): ")
            color = input("Enter the color of the item: ")
            add_clothing(name, item_type, color)
            print(f"Added {name} ({item_type}, {color}) to your closet.")
        
        elif choice == '2':
            display_closet()
        
        elif choice == '3':
            item_id = input("Enter the ID of the clothing item to delete: ")
            delete_clothing(item_id)
        
        elif choice == '4':
            print("Exiting the closet management system.")
            break
        
        else:
            print("Invalid option. Please try again.")

# Run the closet simulation
if __name__ == "__main__":
    run_closet_simulation()
