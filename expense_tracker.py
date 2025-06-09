import json
import os
import csv
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

DATA_FILE = 'expenses.json'

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

def add_expense():
    description = input('Description: ')
    amount = float(input('Amount: '))
    date = input('Date (YYYY-MM-DD, leave blank for today): ')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    expenses = load_expenses()
    expenses.append({'description': description, 'amount': amount, 'date': date})
    save_expenses(expenses)
    print('Expense added.')

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print('No expenses found.')
        return
    print(f"{'ID':<4} {'Date':<12} {'Amount':<10} Description")
    print('-'*40)
    for idx, exp in enumerate(expenses):
        print(f"{idx:<4} {exp['date']:<12} {exp['amount']:<10.2f} {exp['description']}")

def delete_expense():
    expenses = load_expenses()
    view_expenses()
    idx = int(input('Enter ID of expense to delete: '))
    if 0 <= idx < len(expenses):
        removed = expenses.pop(idx)
        save_expenses(expenses)
        print(f"Deleted: {removed['description']} ({removed['amount']})")
    else:
        print('Invalid ID.')

def export_expenses():
    expenses = load_expenses()
    if not expenses:
        print('No expenses to export.')
        return
    
    filename = f"expenses_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'description', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense)
        print(f'Expenses exported to {filename}')
    except Exception as e:
        print(f'Error exporting expenses: {e}')

def gui_add_expense():
    def save():
        desc = desc_entry.get()
        try:
            amt = float(amount_entry.get())
        except ValueError:
            messagebox.showerror('Error', 'Amount must be a number')
            return
        date = date_entry.get() or datetime.now().strftime('%Y-%m-%d')
        expenses = load_expenses()
        expenses.append({'description': desc, 'amount': amt, 'date': date})
        save_expenses(expenses)
        messagebox.showinfo('Success', 'Expense added!')
        add_win.destroy()
        gui_view_expenses()

    add_win = tk.Toplevel(root)
    add_win.title('Add Expense')
    tk.Label(add_win, text='Description:').grid(row=0, column=0)
    desc_entry = tk.Entry(add_win)
    desc_entry.grid(row=0, column=1)
    tk.Label(add_win, text='Amount:').grid(row=1, column=0)
    amount_entry = tk.Entry(add_win)
    amount_entry.grid(row=1, column=1)
    tk.Label(add_win, text='Date (YYYY-MM-DD):').grid(row=2, column=0)
    date_entry = tk.Entry(add_win)
    date_entry.grid(row=2, column=1)
    tk.Button(add_win, text='Save', command=save).grid(row=3, column=0, columnspan=2)

def gui_view_expenses():
    for widget in list_frame.winfo_children():
        widget.destroy()
    expenses = load_expenses()
    if not expenses:
        tk.Label(list_frame, text='No expenses found.').pack()
        return
    header = tk.Label(list_frame, text=f"{'ID':<4} {'Date':<12} {'Amount':<10} Description", font=('Arial', 10, 'bold'))
    header.pack()
    for idx, exp in enumerate(expenses):
        row = f"{idx:<4} {exp['date']:<12} {exp['amount']:<10.2f} {exp['description']}"
        tk.Label(list_frame, text=row, anchor='w', justify='left').pack(fill='x')

def gui_delete_expense():
    expenses = load_expenses()
    if not expenses:
        messagebox.showinfo('Info', 'No expenses to delete.')
        return
    idx = simpledialog.askinteger('Delete Expense', 'Enter ID of expense to delete:')
    if idx is None:
        return
    if 0 <= idx < len(expenses):
        removed = expenses.pop(idx)
        save_expenses(expenses)
        messagebox.showinfo('Deleted', f"Deleted: {removed['description']} ({removed['amount']})")
        gui_view_expenses()
    else:
        messagebox.showerror('Error', 'Invalid ID.')

def gui_export_expenses():
    expenses = load_expenses()
    if not expenses:
        messagebox.showinfo('Info', 'No expenses to export.')
        return
    
    filename = f"expenses_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'description', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense)
        messagebox.showinfo('Export Complete', f'Expenses exported to {filename}')
    except Exception as e:
        messagebox.showerror('Export Error', f'Error exporting expenses: {e}')

def run_gui():
    global root, list_frame
    root = tk.Tk()
    root.title('Expense Tracker')
    tk.Button(root, text='Add Expense', command=gui_add_expense).pack(fill='x')
    tk.Button(root, text='View Expenses', command=gui_view_expenses).pack(fill='x')
    tk.Button(root, text='Delete Expense', command=gui_delete_expense).pack(fill='x')
    tk.Button(root, text='Export Expenses', command=gui_export_expenses).pack(fill='x')
    list_frame = tk.Frame(root)
    list_frame.pack(fill='both', expand=True)
    gui_view_expenses()
    root.mainloop()

def main():
    while True:
        print('\nExpense Tracker')
        print('1. Add Expense')
        print('2. View Expenses')
        print('3. Delete Expense')
        print('4. Export Expenses')
        print('5. Exit')
        choice = input('Choose an option: ')
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            export_expenses()
        elif choice == '5':
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    mode = input('Type "gui" for graphical interface or press Enter for CLI: ')
    if mode.strip().lower() == 'gui':
        if TKINTER_AVAILABLE:
            run_gui()
        else:
            print('GUI mode not available. Tkinter is not installed. Running CLI mode instead.')
            main()
    else:
        main()
