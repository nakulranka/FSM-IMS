# -- coding: utf-8 --
"""
Created on Sun Apr 14 01:48:29 2024

@author: nakul
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

# Define the state machine
class InventoryFSM:
    def __init__(self):
        self.state = "idle"
        self.inventory = []
        self.load_inventory()

    def transition(self, event):
        if event in ["add", "update", "show", "delete"]:
            self.state = event
        elif event == "idle":
            self.state = "idle"

    def load_inventory(self):
        # Load inventory data from a file
        file_path = "inventory_data.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.inventory = json.load(file)
        else:
            self.inventory = []

    def save_inventory(self):
        # Save inventory data to a file
        file_path = "inventory_data.json"
        with open(file_path, "w") as file:
            json.dump(self.inventory, file, indent=4)

# Define the Inventory GUI
class InventoryGUI:
    def __init__(self, master, fsm):
        self.master = master
        self.master.title("Inventory System")
        self.fsm = fsm
        self.create_widgets()
        
        # Save data when the program closes
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Create frames
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.pack(pady=10)

        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.pack(pady=10)

        # Create buttons
        self.add_button = ttk.Button(self.top_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ttk.Button(self.top_frame, text="Update Item", command=self.update_item)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.show_button = ttk.Button(self.top_frame, text="Show Inventory", command=self.show_inventory)
        self.show_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.top_frame, text="Delete Item", command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Create Treeview
        self.tree = ttk.Treeview(self.bottom_frame, columns=("Name", "Price(₹)", "Quantity"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price(₹)", text="Price(₹)")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.pack()

        # Create function calls for dialogs
        self.create_item_dialog()
        self.create_update_dialog()
        
        # Initially load the inventory into the Treeview
        self.show_inventory()

    def create_item_dialog(self):
        # Dialog for adding an item
        self.add_dialog = tk.Toplevel(self.master)
        self.add_dialog.title("Add Item")
        self.add_dialog.withdraw()  # Hide until needed

        tk.Label(self.add_dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.add_name_entry = tk.Entry(self.add_dialog)
        self.add_name_entry.grid(row=0, column=1)

        tk.Label(self.add_dialog, text="Price(₹):").grid(row=1, column=0, padx=10, pady=5)
        self.add_price_entry = tk.Entry(self.add_dialog)
        self.add_price_entry.grid(row=1, column=1)

        tk.Label(self.add_dialog, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
        self.add_quantity_entry = tk.Entry(self.add_dialog)
        self.add_quantity_entry.grid(row=2, column=1)

        self.add_save_button = ttk.Button(self.add_dialog, text="Save", command=self.save_item)
        self.add_save_button.grid(row=3, column=1, pady=10)

        self.add_cancel_button = ttk.Button(self.add_dialog, text="Cancel", command=self.add_dialog.withdraw)
        self.add_cancel_button.grid(row=3, column=2, pady=10)

    def create_update_dialog(self):
        # Dialog for updating an item
        self.update_dialog = tk.Toplevel(self.master)
        self.update_dialog.title("Update Item")
        self.update_dialog.withdraw()  # Hide until needed

        tk.Label(self.update_dialog, text="Select item to update:").grid(row=0, column=0, padx=10, pady=5)
        self.update_item_box = ttk.Combobox(self.update_dialog, state="readonly")
        self.update_item_box.grid(row=0, column=1)

        tk.Label(self.update_dialog, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.update_name_entry = tk.Entry(self.update_dialog)
        self.update_name_entry.grid(row=1, column=1)

        tk.Label(self.update_dialog, text="Price(₹):").grid(row=2, column=0, padx=10, pady=5)
        self.update_price_entry = tk.Entry(self.update_dialog)
        self.update_price_entry.grid(row=2, column=1)

        tk.Label(self.update_dialog, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
        self.update_quantity_entry = tk.Entry(self.update_dialog)
        self.update_quantity_entry.grid(row=3, column=1)

        self.update_save_button = ttk.Button(self.update_dialog, text="Save", command=self.save_update)
        self.update_save_button.grid(row=4, column=1, pady=10)

        self.update_cancel_button = ttk.Button(self.update_dialog, text="Cancel", command=self.update_dialog.withdraw)
        self.update_cancel_button.grid(row=4, column=2, pady=10)

    def add_item(self):
        self.fsm.transition("add")
        self.add_name_entry.delete(0, tk.END)
        self.add_price_entry.delete(0, tk.END)
        self.add_quantity_entry.delete(0, tk.END)
        self.add_dialog.deiconify()

    def save_item(self):
        # Save the added item
        name = self.add_name_entry.get()
        try:
            price = float(self.add_price_entry.get())
            quantity = int(self.add_quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be numeric values.")
            return
        
        if name and price > 0 and quantity > 0:
            item = {"name": name, "price(₹)": price, "quantity": quantity}
            self.fsm.inventory.append(item)
            self.fsm.save_inventory()
            messagebox.showinfo("Success", "Item added successfully!")
            self.add_dialog.withdraw()
        else:
            messagebox.showerror("Error", "All fields are required and must be valid!")

    def update_item(self):
        # Update item function
        if self.fsm.inventory:
            self.fsm.transition("update")
            self.update_item_box.config(values=[item["name"] for item in self.fsm.inventory])
            self.update_item_box.set("")
            self.update_name_entry.delete(0, tk.END)
            self.update_price_entry.delete(0, tk.END)
            self.update_quantity_entry.delete(0, tk.END)
            self.update_dialog.deiconify()
        else:
            messagebox.showinfo("Info", "No items in inventory to update.")

    def save_update(self):
        # Save the updated item
        selected_item = self.update_item_box.get()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to update.")
            return

        # Find the item by name
        item = next((item for item in self.fsm.inventory if item["name"] == selected_item), None)
        if not item:
            messagebox.showerror("Error", "Item not found.")
            return

        # Retrieve updated name, price, and quantity values
        name = self.update_name_entry.get()
        try:
            price_input = self.update_price_entry.get()
            price = float(price_input) if price_input else None

            quantity_input = self.update_quantity_entry.get()
            quantity = int(quantity_input) if quantity_input else None
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be numeric values.")
            return

        # Update the item's fields if the inputs are valid
        if name:
            item["name"] = name
        if price is not None:
            item["price(₹)"] = price
        if quantity is not None:
            item["quantity"] = quantity

        # Save the updated inventory and close the dialog
        self.fsm.save_inventory()
        messagebox.showinfo("Success", "Item updated successfully!")
        self.update_dialog.withdraw()

    def show_inventory(self):
        # Show the inventory in the Treeview
        self.fsm.transition("show")
        self.tree.delete(*self.tree.get_children())
        for index, item in enumerate(self.fsm.inventory, start=1):
            self.tree.insert("", index, text=index, values=(item["name"], item["price(₹)"], item["quantity"]))

    def delete_item(self):
        # Delete item function
        if self.fsm.inventory:
            self.fsm.transition("delete")
            
            # Get the selection from the tree
            selected_items = self.tree.selection()
            
            # If no item is selected, show an info message
            if not selected_items:
                messagebox.showinfo("Info", "Please select an item to delete.")
                return
            
            # Iterate over selected items (in case multiple rows are selected)
            for selected_item in selected_items:
                # Get the index of the selected item
                item_index = self.tree.index(selected_item)
                
                # Remove the item from the inventory list using the index
                del self.fsm.inventory[item_index]
                
                # Remove the item from the Treeview
                self.tree.delete(selected_item)
            
            # Refresh the Treeview to reflect the current inventory
            self.show_inventory()
            
            # Show success message
            messagebox.showinfo("Success", "Item(s) deleted successfully!")
            
            # Save inventory data after deletion
            self.fsm.save_inventory()
        else:
            # If there is no item in the inventory, show info message
            messagebox.showinfo("Info", "No items in inventory to delete.")

    def on_closing(self):
        # Save data before closing the GUI
        self.fsm.save_inventory()
        self.master.destroy()

# Main application
def main():
    fsm = InventoryFSM()
    root = tk.Tk()
    app = InventoryGUI(root, fsm)
    root.mainloop()

if __name__ == "__main__":
    main()
