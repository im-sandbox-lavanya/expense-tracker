#!/usr/bin/env python3
"""
Expense Tracker Application
A simple command-line expense tracking application with CSV export functionality.
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Expense:
    """Represents an expense entry."""
    
    def __init__(self, date: str, category: str, amount: float, description: str):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
    
    def to_dict(self) -> Dict:
        """Convert expense to dictionary."""
        return {
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        """Create expense from dictionary."""
        return cls(
            date=data['date'],
            category=data['category'],
            amount=data['amount'],
            description=data['description']
        )


class ExpenseTracker:
    """Main expense tracker application."""
    
    def __init__(self, data_file: str = 'expenses.json'):
        self.data_file = data_file
        self.expenses: List[Expense] = []
        self.load_expenses()
    
    def load_expenses(self) -> None:
        """Load expenses from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.expenses = [Expense.from_dict(expense_data) for expense_data in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading expenses: {e}")
                self.expenses = []
    
    def save_expenses(self) -> None:
        """Save expenses to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                data = [expense.to_dict() for expense in self.expenses]
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving expenses: {e}")
    
    def add_expense(self, date: str, category: str, amount: float, description: str) -> None:
        """Add a new expense."""
        expense = Expense(date, category, amount, description)
        self.expenses.append(expense)
        self.save_expenses()
        print(f"Added expense: {amount} for {description}")
    
    def list_expenses(self) -> None:
        """Display all expenses."""
        if not self.expenses:
            print("No expenses recorded.")
            return
        
        print("\nAll Expenses:")
        print("-" * 70)
        print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("-" * 70)
        
        for expense in self.expenses:
            print(f"{expense.date:<12} {expense.category:<15} {expense.amount:<10.2f} {expense.description}")
        
        total = sum(expense.amount for expense in self.expenses)
        print("-" * 70)
        print(f"Total: ${total:.2f}")
    
    def list_expenses_with_indices(self) -> None:
        """Display all expenses with indices for selection."""
        if not self.expenses:
            print("No expenses recorded.")
            return
        
        print("\nExpenses:")
        print("-" * 80)
        print(f"{'Index':<6} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("-" * 80)
        
        for index, expense in enumerate(self.expenses):
            print(f"{index:<6} {expense.date:<12} {expense.category:<15} {expense.amount:<10.2f} {expense.description}")
        
        print("-" * 80)
    
    def delete_expense(self, index: int) -> bool:
        """
        Delete an expense by index.
        
        Args:
            index: Index of the expense to delete (0-based).
        
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        if not self.expenses:
            print("No expenses to delete.")
            return False
        
        if index < 0 or index >= len(self.expenses):
            print(f"Invalid index. Please enter a number between 0 and {len(self.expenses) - 1}.")
            return False
        
        deleted_expense = self.expenses.pop(index)
        self.save_expenses()
        print(f"Deleted expense: {deleted_expense.amount} for {deleted_expense.description}")
        return True
    
    def edit_expense(self, index: int, date: str, category: str, amount: float, description: str) -> bool:
        """
        Edit an existing expense.
        
        Args:
            index: Index of the expense to edit (0-based).
            date: New date for the expense.
            category: New category for the expense.
            amount: New amount for the expense.
            description: New description for the expense.
        
        Returns:
            bool: True if edit successful, False otherwise.
        """
        if not self.expenses:
            print("No expenses to edit.")
            return False
        
        if index < 0 or index >= len(self.expenses):
            print(f"Invalid index. Please enter a number between 0 and {len(self.expenses) - 1}.")
            return False
        
        old_expense = self.expenses[index]
        self.expenses[index] = Expense(date, category, amount, description)
        self.save_expenses()
        print(f"Updated expense: {old_expense.amount} for {old_expense.description} -> {amount} for {description}")
        return True
    
    def export_to_csv(self, filename: Optional[str] = None) -> bool:
        """
        Export all expenses to a CSV file.
        
        Args:
            filename: Optional filename for the CSV. If None, uses timestamp.
        
        Returns:
            bool: True if export successful, False otherwise.
        """
        if not self.expenses:
            print("No expenses to export.")
            return False
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"expenses_export_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'category', 'amount', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write expense data
                for expense in self.expenses:
                    writer.writerow(expense.to_dict())
            
            print(f"Successfully exported {len(self.expenses)} expenses to {filename}")
            return True
            
        except IOError as e:
            print(f"Error exporting to CSV: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during export: {e}")
            return False


def get_user_input(prompt: str, input_type: type = str):
    """Get user input with type conversion and error handling."""
    while True:
        try:
            value = input(prompt)
            if input_type == float:
                return float(value)
            elif input_type == str:
                return value.strip()
            else:
                return input_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def main():
    """Main application loop."""
    tracker = ExpenseTracker()
    
    print("Welcome to Expense Tracker!")
    print("Track your expenses and export them to CSV for analysis.")
    
    while True:
        print("\n" + "="*50)
        print("Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. List All Expenses")
        print("3. Export to CSV")
        print("4. Edit Expense")
        print("5. Delete Expense")
        print("6. Exit")
        print("="*50)
        
        choice = get_user_input("Enter your choice (1-6): ")
        
        if choice == '1':
            print("\nAdd New Expense:")
            date = get_user_input("Enter date (YYYY-MM-DD): ")
            category = get_user_input("Enter category: ")
            amount = get_user_input("Enter amount: $", float)
            description = get_user_input("Enter description: ")
            
            tracker.add_expense(date, category, amount, description)
        
        elif choice == '2':
            tracker.list_expenses()
        
        elif choice == '3':
            print("\nExport to CSV:")
            custom_filename = get_user_input("Enter filename (or press Enter for auto-generated): ")
            filename = custom_filename if custom_filename else None
            tracker.export_to_csv(filename)
        
        elif choice == '4':
            print("\nEdit Expense:")
            tracker.list_expenses_with_indices()
            if tracker.expenses:
                try:
                    index = int(get_user_input("Enter the index of the expense to edit: "))
                    if 0 <= index < len(tracker.expenses):
                        current_expense = tracker.expenses[index]
                        print(f"\nCurrent expense: {current_expense.date} | {current_expense.category} | ${current_expense.amount} | {current_expense.description}")
                        
                        date = get_user_input(f"Enter new date (current: {current_expense.date}): ") or current_expense.date
                        category = get_user_input(f"Enter new category (current: {current_expense.category}): ") or current_expense.category
                        amount_input = get_user_input(f"Enter new amount (current: ${current_expense.amount}): ")
                        amount = float(amount_input) if amount_input else current_expense.amount
                        description = get_user_input(f"Enter new description (current: {current_expense.description}): ") or current_expense.description
                        
                        tracker.edit_expense(index, date, category, amount, description)
                    else:
                        print(f"Invalid index. Please enter a number between 0 and {len(tracker.expenses) - 1}.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        
        elif choice == '5':
            print("\nDelete Expense:")
            tracker.list_expenses_with_indices()
            if tracker.expenses:
                try:
                    index = int(get_user_input("Enter the index of the expense to delete: "))
                    if 0 <= index < len(tracker.expenses):
                        expense_to_delete = tracker.expenses[index]
                        confirm = get_user_input(f"Are you sure you want to delete expense: {expense_to_delete.amount} for {expense_to_delete.description}? (y/N): ")
                        if confirm.lower() in ['y', 'yes']:
                            tracker.delete_expense(index)
                        else:
                            print("Deletion cancelled.")
                    else:
                        print(f"Invalid index. Please enter a number between 0 and {len(tracker.expenses) - 1}.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        
        elif choice == '6':
            print("Thank you for using Expense Tracker!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main()