import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
from datetime import datetime

class CustomerManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Information Management System")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_gui()
    
    def init_database(self):
        """Initialize SQLite database and create table if it doesn't exist"""
        self.conn = sqlite3.connect('customer_data.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birthday TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                preferred_contact TEXT NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def create_gui(self):
        """Create the graphical user interface"""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Customer Information Form", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name
        ttk.Label(main_frame, text="Name:*", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=35)
        self.name_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Birthday
        ttk.Label(main_frame, text="Birthday:*", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        birthday_frame = ttk.Frame(main_frame)
        birthday_frame.grid(row=2, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        self.birthday_entry = ttk.Entry(birthday_frame, width=35)
        self.birthday_entry.pack(side=tk.LEFT)
        ttk.Label(birthday_frame, text="(MM/DD/YYYY)", 
                 font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=(5, 0))
        
        # Email
        ttk.Label(main_frame, text="Email:*", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame, width=35)
        self.email_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Phone
        ttk.Label(main_frame, text="Phone:*", font=('Arial', 10)).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        phone_frame = ttk.Frame(main_frame)
        phone_frame.grid(row=4, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        self.phone_entry = ttk.Entry(phone_frame, width=35)
        self.phone_entry.pack(side=tk.LEFT)
        ttk.Label(phone_frame, text="(xxx-xxx-xxxx)", 
                 font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=(5, 0))
        
        # Address
        ttk.Label(main_frame, text="Address:*", font=('Arial', 10)).grid(
            row=5, column=0, sticky=tk.W, pady=5)
        self.address_text = tk.Text(main_frame, width=27, height=4)
        self.address_text.grid(row=5, column=1, pady=5, padx=(10, 0))
        
        # Preferred Contact Method
        ttk.Label(main_frame, text="Preferred Contact:*", font=('Arial', 10)).grid(
            row=6, column=0, sticky=tk.W, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_dropdown = ttk.Combobox(main_frame, textvariable=self.contact_var,
                                            values=["Email", "Phone", "Mail"],
                                            state="readonly", width=32)
        self.contact_dropdown.grid(row=6, column=1, pady=5, padx=(10, 0))
        self.contact_dropdown.set("Email")  # Default value
        
        # Required fields note
        note_label = ttk.Label(main_frame, text="* Required fields", 
                              font=('Arial', 8), foreground='red')
        note_label.grid(row=7, column=0, columnspan=2, pady=(10, 5))
        
        # Submit button
        submit_btn = ttk.Button(main_frame, text="Submit", command=self.submit_data)
        submit_btn.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", font=('Arial', 9))
        self.status_label.grid(row=9, column=0, columnspan=2)
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_date(self, date_str):
        """Validate date format (MM/DD/YYYY)"""
        try:
            datetime.strptime(date_str, '%m/%d/%Y')
            return True
        except ValueError:
            return False
    
    def validate_phone(self, phone):
        """Validate phone format (accepts various formats)"""
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
        # Check if it's 10 digits
        return len(cleaned) == 10 and cleaned.isdigit()
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_text.delete('1.0', tk.END)
        self.contact_dropdown.set("Email")
    
    def submit_data(self):
        """Validate and submit customer data to database"""
        # Get all values
        name = self.name_entry.get().strip()
        birthday = self.birthday_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_text.get('1.0', tk.END).strip()
        preferred_contact = self.contact_var.get()
        
        # Validation
        if not all([name, birthday, email, phone, address, preferred_contact]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if not self.validate_date(birthday):
            messagebox.showerror("Error", "Invalid birthday format. Use MM/DD/YYYY")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return
        
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number. Use 10 digits (e.g., xxx-xxx-xxxx)")
            return
        
        # Insert into database
        try:
            self.cursor.execute('''
                INSERT INTO customers (name, birthday, email, phone, address, preferred_contact)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, birthday, email, phone, address, preferred_contact))
            
            self.conn.commit()
            
            # Show success message
            messagebox.showinfo("Success", "Customer information saved successfully!")
            
            # Clear the form
            self.clear_form()
            
            # Update status
            self.status_label.config(text="✓ Data submitted successfully", foreground='green')
            self.root.after(3000, lambda: self.status_label.config(text=""))
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error saving data: {str(e)}")
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = CustomerManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()