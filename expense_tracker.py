import json
import os
from datetime import datetime

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
    amount = float(input('Amount: '))
    category = input('Category: ')
    description = input('Description: ')
    date = input('Date (YYYY-MM-DD, leave blank for today): ')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    expenses = load_expenses()
    expense = {
        'id': len(expenses) + 1,
        'amount': amount,
        'category': category,
        'description': description,
        'date': date
    }
    expenses.append(expense)
    save_expenses(expenses)
    print('Expense added!')

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print('No expenses found.')
        return
    print(f"{'ID':<4} {'Amount':<10} {'Category':<15} {'Description':<20} {'Date':<12}")
    print('-'*65)
    for exp in expenses:
        print(f"{exp['id']:<4} {exp['amount']:<10.2f} {exp['category']:<15} {exp['description']:<20} {exp['date']:<12}")

def delete_expense():
    expenses = load_expenses()
    if not expenses:
        print('No expenses to delete.')
        return
    view_expenses()
    try:
        exp_id = int(input('Enter the ID of the expense to delete: '))
    except ValueError:
        print('Invalid ID.')
        return
    new_expenses = [e for e in expenses if e['id'] != exp_id]
    if len(new_expenses) == len(expenses):
        print('Expense not found.')
        return
    # Reassign IDs
    for idx, exp in enumerate(new_expenses, 1):
        exp['id'] = idx
    save_expenses(new_expenses)
    print('Expense deleted!')

def main():
    while True:
        print('\nExpense Tracker')
        print('1. Add Expense')
        print('2. View Expenses')
        print('3. Delete Expense')
        print('4. Exit')
        choice = input('Choose an option: ')
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Try again.')

if __name__ == '__main__':
    main()
