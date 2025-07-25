import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Data file
DATA_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save contacts to file
def save_contacts():
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# Add new contact
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    if name and phone:
        contacts[name] = {"phone": phone, "email": email, "address": address}
        save_contacts()
        update_listbox()
        clear_fields()
        messagebox.showinfo("Success", "Contact added successfully!")
    else:
        messagebox.showwarning("Error", "Name and Phone are required.")

# Display all contacts
def update_listbox():
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        listbox.insert(tk.END, f"{name} - {info['phone']}")

# Search contact
def search_contact():
    query = entry_search.get().lower()
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        if query in name.lower() or query in info["phone"]:
            listbox.insert(tk.END, f"{name} - {info['phone']}")

# Show selected contact details
def on_select(event):
    if listbox.curselection():
        name = listbox.get(listbox.curselection())[0].split(" - ")[0]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, name)
        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, contacts[name]["phone"])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, contacts[name]["email"])
        entry_address.delete(0, tk.END)
        entry_address.insert(0, contacts[name]["address"])

# Update contact
def update_contact():
    name = entry_name.get()
    if name in contacts:
        contacts[name]["phone"] = entry_phone.get()
        contacts[name]["email"] = entry_email.get()
        contacts[name]["address"] = entry_address.get()
        save_contacts()
        update_listbox()
        messagebox.showinfo("Success", "Contact updated.")
    else:
        messagebox.showerror("Error", "Contact not found.")

# Delete contact
def delete_contact():
    name = entry_name.get()
    if name in contacts:
        confirm = messagebox.askyesno("Delete", f"Delete contact '{name}'?")
        if confirm:
            contacts.pop(name)
            save_contacts()
            update_listbox()
            clear_fields()
    else:
        messagebox.showerror("Error", "Contact not found.")

# Clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# ---------------------- GUI SETUP ---------------------- #

root = tk.Tk()
root.title("Contact Management App")
root.geometry("550x500")
root.resizable(False, False)

contacts = load_contacts()

# Labels and Entries
tk.Label(root, text="Name").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(root, text="Phone").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_phone = tk.Entry(root, width=30)
entry_phone.grid(row=1, column=1, pady=5)

tk.Label(root, text="Email").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=2, column=1, pady=5)

tk.Label(root, text="Address").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_address = tk.Entry(root, width=30)
entry_address.grid(row=3, column=1, pady=5)

# Buttons
tk.Button(root, text="Add Contact", width=15, command=add_contact).grid(row=4, column=0, pady=10)
tk.Button(root, text="Update Contact", width=15, command=update_contact).grid(row=4, column=1)
tk.Button(root, text="Delete Contact", width=15, command=delete_contact).grid(row=5, column=0)
tk.Button(root, text="Clear Fields", width=15, command=clear_fields).grid(row=5, column=1)

# Search
tk.Label(root, text="Search by Name/Phone").grid(row=6, column=0, padx=10, pady=10)
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=6, column=1)
tk.Button(root, text="Search", width=15, command=search_contact).grid(row=7, column=1, pady=5)

# Contact List
listbox = tk.Listbox(root, width=50)
listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
listbox.bind('<<ListboxSelect>>', on_select)

# Initialize contact list
update_listbox()

root.mainloop()
