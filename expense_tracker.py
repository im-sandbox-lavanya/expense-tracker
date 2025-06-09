#!/usr/bin/env python3
"""
Expense Tracker - Track your expenses and categorize them for better financial management.
Supports CSV export functionality.
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any


class ExpenseTracker:
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = data_file
        self.expenses = self._load_expenses()
    
    def _load_expenses(self) -> List[Dict[str, Any]]:
        """Load expenses from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_expenses(self) -> None:
        """Save expenses to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.expenses, f, indent=2)
        except IOError as e:
            print(f"Error saving expenses: {e}")
    
    def add_expense(self, amount: float, category: str, description: str = "") -> None:
        """Add a new expense."""
        expense = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "category": category,
            "description": description
        }
        self.expenses.append(expense)
        self._save_expenses()
        print(f"Added expense: ${amount:.2f} in {category}")
    
    def view_expenses(self) -> None:
        """Display all expenses."""
        if not self.expenses:
            print("No expenses recorded.")
            return
        
        print("\n=== EXPENSES ===")
        total = 0
        for expense in self.expenses:
            print(f"{expense['date']} | ${expense['amount']:.2f} | {expense['category']} | {expense['description']}")
            total += expense['amount']
        print(f"\nTotal expenses: ${total:.2f}")
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export expenses to CSV format."""
        if filename is None:
            filename = f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'amount', 'category', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow(expense)
            
            print(f"Expenses exported to {filename}")
            return filename
        except IOError as e:
            print(f"Error exporting to CSV: {e}")
            return ""
    
    def get_categories(self) -> List[str]:
        """Get list of unique categories."""
        categories = set()
        for expense in self.expenses:
            categories.add(expense['category'])
        return sorted(list(categories))
    
    def get_expenses_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get expenses filtered by category."""
        return [expense for expense in self.expenses if expense['category'].lower() == category.lower()]


def main():
    """Main CLI interface."""
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        tracker = ExpenseTracker()
        
        if sys.argv[1] == 'export':
            filename = sys.argv[2] if len(sys.argv) > 2 else None
            exported_file = tracker.export_to_csv(filename)
            if exported_file:
                sys.exit(0)
            else:
                sys.exit(1)
        
        elif sys.argv[1] == 'add' and len(sys.argv) >= 4:
            try:
                amount = float(sys.argv[2])
                category = sys.argv[3]
                description = sys.argv[4] if len(sys.argv) > 4 else ""
                tracker.add_expense(amount, category, description)
                sys.exit(0)
            except ValueError:
                print("Invalid amount. Please provide a valid number.")
                sys.exit(1)
        
        elif sys.argv[1] == 'view':
            tracker.view_expenses()
            sys.exit(0)
        
        elif sys.argv[1] == 'help':
            print("Usage:")
            print("  python expense_tracker.py                    # Interactive mode")
            print("  python expense_tracker.py export [filename]  # Export to CSV")
            print("  python expense_tracker.py add <amount> <category> [description]")
            print("  python expense_tracker.py view               # View all expenses")
            print("  python expense_tracker.py help               # Show this help")
            sys.exit(0)
        
        else:
            print("Invalid command. Use 'help' for usage information.")
            sys.exit(1)
    
    # Interactive mode
    tracker = ExpenseTracker()
    
    while True:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Export to CSV")
        print("4. View categories")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            try:
                amount = float(input("Enter amount: $"))
                category = input("Enter category: ").strip()
                description = input("Enter description (optional): ").strip()
                
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                if not category:
                    print("Category is required.")
                    continue
                
                tracker.add_expense(amount, category, description)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == '2':
            tracker.view_expenses()
        
        elif choice == '3':
            filename = input("Enter CSV filename (press Enter for default): ").strip()
            if filename:
                tracker.export_to_csv(filename)
            else:
                tracker.export_to_csv()
        
        elif choice == '4':
            categories = tracker.get_categories()
            if categories:
                print("\nCategories:")
                for cat in categories:
                    expenses = tracker.get_expenses_by_category(cat)
                    total = sum(exp['amount'] for exp in expenses)
                    print(f"  {cat}: ${total:.2f} ({len(expenses)} expenses)")
            else:
                print("No categories found.")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()