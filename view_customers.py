import sqlite3
from datetime import datetime

def view_all_customers():
    """View all customers in the database"""
    try:
        # Connect to database
        conn = sqlite3.connect('customer_data.db')
        cursor = conn.cursor()
        
        # Get all customers
        cursor.execute('SELECT * FROM customers ORDER BY id')
        customers = cursor.fetchall()
        
        if not customers:
            print("No customers found in the database.")
            return
        
        print(f"\n{'='*80}")
        print(f"CUSTOMER DATABASE - Total Records: {len(customers)}")
        print(f"{'='*80}\n")
        
        for customer in customers:
            print(f"ID: {customer[0]}")
            print(f"Name: {customer[1]}")
            print(f"Birthday: {customer[2]}")
            print(f"Email: {customer[3]}")
            print(f"Phone: {customer[4]}")
            print(f"Address: {customer[5]}")
            print(f"Preferred Contact: {customer[6]}")
            print(f"Date Added: {customer[7]}")
            print(f"{'-'*80}\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print("Database file 'customer_data.db' not found!")

def view_summary():
    """View summary statistics"""
    try:
        conn = sqlite3.connect('customer_data.db')
        cursor = conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM customers')
        total = cursor.fetchone()[0]
        
        # Contact method breakdown
        cursor.execute('SELECT preferred_contact, COUNT(*) FROM customers GROUP BY preferred_contact')
        contact_stats = cursor.fetchall()
        
        print(f"\n{'='*50}")
        print("DATABASE SUMMARY")
        print(f"{'='*50}")
        print(f"Total Customers: {total}")
        print(f"\nPreferred Contact Methods:")
        for method, count in contact_stats:
            print(f"  {method}: {count}")
        print(f"{'='*50}\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def search_customer(search_term):
    """Search for customers by name"""
    try:
        conn = sqlite3.connect('customer_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE name LIKE ?', (f'%{search_term}%',))
        results = cursor.fetchall()
        
        if not results:
            print(f"No customers found matching '{search_term}'")
            return
        
        print(f"\nFound {len(results)} customer(s):\n")
        for customer in results:
            print(f"ID: {customer[0]} | Name: {customer[1]} | Email: {customer[3]}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    print("\nCustomer Database Viewer")
    print("1. View all customers")
    print("2. View summary")
    print("3. Search by name")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        view_all_customers()
    elif choice == "2":
        view_summary()
    elif choice == "3":
        search_term = input("Enter name to search: ")
        search_customer(search_term)
    else:
        print("Invalid choice!")