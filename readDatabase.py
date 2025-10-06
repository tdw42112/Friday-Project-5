import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class CustomerDatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Database Viewer")
        self.root.geometry("1000x600")
        
        # Create GUI
        self.create_gui()
        
        # Load data on startup
        self.load_data()
    
    def create_gui(self):
        """Create the graphical user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title and controls frame
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Title
        title_label = ttk.Label(top_frame, text="Customer Database", 
                                font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = ttk.Button(top_frame, text="Refresh", command=self.load_data)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT, padx=20)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_data)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT)
        
        # Treeview frame with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create Treeview
        columns = ('ID', 'Name', 'Birthday', 'Email', 'Phone', 'Address', 'Contact', 'Date Added')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Define column headings and widths
        column_widths = {
            'ID': 40,
            'Name': 120,
            'Birthday': 90,
            'Email': 150,
            'Phone': 100,
            'Address': 180,
            'Contact': 80,
            'Date Added': 130
        }
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=column_widths[col], minwidth=50)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="View Details", 
                  command=self.view_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to Text", 
                  command=self.export_to_text).pack(side=tk.LEFT, padx=5)
        
        # Alternating row colors
        self.tree.tag_configure('oddrow', background='#E8E8E8')
        self.tree.tag_configure('evenrow', background='#FFFFFF')
    
    def load_data(self):
        """Load all customer data from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect('customer_data.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM customers ORDER BY id DESC')
            rows = cursor.fetchall()
            
            # Store all data for filtering
            self.all_data = rows
            
            # Insert data into treeview
            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert('', tk.END, values=row, tags=(tag,))
            
            # Update status
            self.status_label.config(text=f"Total records: {len(rows)}")
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading data: {str(e)}")
        except FileNotFoundError:
            messagebox.showwarning("Database Not Found", 
                                  "customer_data.db file not found. Please run the main application first.")
            self.status_label.config(text="Database file not found")
    
    def filter_data(self, *args):
        """Filter displayed data based on search term"""
        search_term = self.search_var.get().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not hasattr(self, 'all_data'):
            return
        
        # Filter and display data
        filtered_count = 0
        for idx, row in enumerate(self.all_data):
            # Search in name, email, and phone fields
            if (search_term in str(row[1]).lower() or 
                search_term in str(row[3]).lower() or 
                search_term in str(row[4]).lower()):
                
                tag = 'evenrow' if filtered_count % 2 == 0 else 'oddrow'
                self.tree.insert('', tk.END, values=row, tags=(tag,))
                filtered_count += 1
        
        self.status_label.config(text=f"Showing {filtered_count} of {len(self.all_data)} records")
    
    def sort_column(self, col):
        """Sort treeview by column"""
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Try to sort numerically if possible, otherwise alphabetically
        try:
            data.sort(key=lambda x: int(x[0]))
        except ValueError:
            data.sort(key=lambda x: x[0])
        
        for idx, (val, item) in enumerate(data):
            self.tree.move(item, '', idx)
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.item(item, tags=(tag,))
    
    def view_details(self):
        """Show detailed view of selected customer"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a customer to view details.")
            return
        
        # Get selected item values
        values = self.tree.item(selected[0])['values']
        
        # Create detail window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Customer Details - ID: {values[0]}")
        detail_window.geometry("400x350")
        detail_window.resizable(False, False)
        
        frame = ttk.Frame(detail_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        labels = ['ID:', 'Name:', 'Birthday:', 'Email:', 'Phone:', 
                 'Address:', 'Preferred Contact:', 'Date Added:']
        
        for i, (label, value) in enumerate(zip(labels, values)):
            ttk.Label(frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
            if label == 'Address:':
                text_widget = tk.Text(frame, height=3, width=30, wrap=tk.WORD)
                text_widget.insert('1.0', value)
                text_widget.config(state='disabled')
                text_widget.grid(row=i, column=1, sticky=tk.W, pady=5)
            else:
                ttk.Label(frame, text=str(value), font=('Arial', 10)).grid(
                    row=i, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(frame, text="Close", command=detail_window.destroy).grid(
            row=len(labels), column=0, columnspan=2, pady=(20, 0))
    
    def delete_record(self):
        """Delete selected customer record"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a customer to delete.")
            return
        
        values = self.tree.item(selected[0])['values']
        customer_id = values[0]
        customer_name = values[1]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete:\n\n{customer_name} (ID: {customer_id})?")
        
        if confirm:
            try:
                conn = sqlite3.connect('customer_data.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Customer record deleted successfully.")
                self.load_data()
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error deleting record: {str(e)}")
    
    def export_to_text(self):
        """Export all visible data to a text file"""
        try:
            with open('customer_export.txt', 'w') as f:
                f.write("CUSTOMER DATABASE EXPORT\n")
                f.write("=" * 80 + "\n\n")
                
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    f.write(f"ID: {values[0]}\n")
                    f.write(f"Name: {values[1]}\n")
                    f.write(f"Birthday: {values[2]}\n")
                    f.write(f"Email: {values[3]}\n")
                    f.write(f"Phone: {values[4]}\n")
                    f.write(f"Address: {values[5]}\n")
                    f.write(f"Preferred Contact: {values[6]}\n")
                    f.write(f"Date Added: {values[7]}\n")
                    f.write("-" * 80 + "\n\n")
            
            messagebox.showinfo("Export Successful", 
                              "Data exported to 'customer_export.txt'")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")

def main():
    root = tk.Tk()
    app = CustomerDatabaseViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()