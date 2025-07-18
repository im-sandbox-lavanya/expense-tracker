#!/usr/bin/env python3
"""
Expense Tracker Application with Exception Handling
A simple command-line application to track and categorize expenses.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import sys


class ExpenseTrackerError(Exception):
    """Base exception class for expense tracker errors"""
    pass


class DataFileError(ExpenseTrackerError):
    """Exception raised for data file related errors"""
    pass


class ValidationError(ExpenseTrackerError):
    """Exception raised for data validation errors"""
    pass


class ExpenseTracker:
    """Main expense tracker class with comprehensive exception handling"""
    
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = data_file
        self.expenses = []
        self._load_expenses()
    
    def _load_expenses(self) -> None:
        """Load expenses from file with exception handling"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        self.expenses = json.loads(content)
                        self._validate_expense_data()
                    else:
                        self.expenses = []
                        print(f"Warning: {self.data_file} is empty. Starting with fresh data.")
            else:
                self.expenses = []
                print(f"Info: {self.data_file} not found. Creating new expense tracker.")
        except json.JSONDecodeError as e:
            raise DataFileError(f"Invalid JSON format in {self.data_file}: {e}")
        except PermissionError:
            raise DataFileError(f"Permission denied accessing {self.data_file}")
        except OSError as e:
            raise DataFileError(f"Error reading {self.data_file}: {e}")
    
    def _validate_expense_data(self) -> None:
        """Validate loaded expense data structure"""
        if not isinstance(self.expenses, list):
            raise ValidationError("Expense data must be a list")
        
        for i, expense in enumerate(self.expenses):
            if not isinstance(expense, dict):
                raise ValidationError(f"Expense {i} must be a dictionary")
            
            required_fields = ['amount', 'description', 'category', 'date']
            for field in required_fields:
                if field not in expense:
                    raise ValidationError(f"Expense {i} missing required field: {field}")
    
    def _save_expenses(self) -> None:
        """Save expenses to file with exception handling"""
        try:
            # Create backup if file exists
            if os.path.exists(self.data_file):
                backup_file = f"{self.data_file}.backup"
                with open(self.data_file, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
            
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.expenses, file, indent=2, ensure_ascii=False)
                
        except PermissionError:
            raise DataFileError(f"Permission denied writing to {self.data_file}")
        except OSError as e:
            raise DataFileError(f"Error writing to {self.data_file}: {e}")
    
    def _validate_amount(self, amount_str: str) -> float:
        """Validate and convert amount string to float"""
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValidationError("Amount must be positive")
            return amount
        except ValueError:
            raise ValidationError(f"Invalid amount format: {amount_str}")
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValidationError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")
    
    def _validate_category(self, category: str) -> str:
        """Validate category input"""
        if not category or not category.strip():
            raise ValidationError("Category cannot be empty")
        return category.strip()
    
    def _validate_description(self, description: str) -> str:
        """Validate description input"""
        if not description or not description.strip():
            raise ValidationError("Description cannot be empty")
        return description.strip()
    
    def add_expense(self, amount: str, description: str, category: str, date: str = None) -> None:
        """Add a new expense with validation and exception handling"""
        try:
            # Validate inputs
            validated_amount = self._validate_amount(amount)
            validated_description = self._validate_description(description)
            validated_category = self._validate_category(category)
            
            if date is None:
                validated_date = datetime.now().strftime("%Y-%m-%d")
            else:
                validated_date = self._validate_date(date)
            
            # Create expense record
            expense = {
                'amount': validated_amount,
                'description': validated_description,
                'category': validated_category,
                'date': validated_date,
                'timestamp': datetime.now().isoformat()
            }
            
            self.expenses.append(expense)
            self._save_expenses()
            print(f"✓ Expense added successfully: ${validated_amount:.2f} for {validated_description}")
            
        except (ValidationError, DataFileError) as e:
            print(f"Error adding expense: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error adding expense: {e}")
            raise ExpenseTrackerError(f"Unexpected error: {e}")
    
    def view_expenses(self, category: Optional[str] = None) -> None:
        """View expenses with optional category filter"""
        try:
            if not self.expenses:
                print("No expenses recorded yet.")
                return
            
            filtered_expenses = self.expenses
            if category:
                category = category.strip().lower()
                filtered_expenses = [
                    exp for exp in self.expenses 
                    if exp['category'].lower() == category
                ]
                
                if not filtered_expenses:
                    print(f"No expenses found for category: {category}")
                    return
            
            total = 0
            print("\n" + "="*60)
            print(f"{'Date':<12} {'Amount':<10} {'Category':<15} {'Description'}")
            print("="*60)
            
            for expense in filtered_expenses:
                print(f"{expense['date']:<12} ${expense['amount']:<9.2f} "
                      f"{expense['category']:<15} {expense['description']}")
                total += expense['amount']
            
            print("="*60)
            print(f"Total: ${total:.2f}")
            
        except Exception as e:
            print(f"Error viewing expenses: {e}")
            raise ExpenseTrackerError(f"Unexpected error viewing expenses: {e}")
    
    def get_categories(self) -> List[str]:
        """Get list of unique categories"""
        try:
            categories = list(set(expense['category'] for expense in self.expenses))
            return sorted(categories)
        except Exception as e:
            print(f"Error getting categories: {e}")
            raise ExpenseTrackerError(f"Unexpected error getting categories: {e}")
    
    def get_summary(self) -> Dict[str, float]:
        """Get expense summary by category"""
        try:
            summary = {}
            for expense in self.expenses:
                category = expense['category']
                summary[category] = summary.get(category, 0) + expense['amount']
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            raise ExpenseTrackerError(f"Unexpected error generating summary: {e}")


def get_user_input(prompt: str) -> str:
    """Get user input with exception handling"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except EOFError:
        print("\n\nEnd of input reached.")
        sys.exit(0)


def main():
    """Main application loop with exception handling"""
    print("Welcome to Expense Tracker!")
    print("=" * 40)
    
    try:
        tracker = ExpenseTracker()
    except (DataFileError, ValidationError) as e:
        print(f"Error initializing expense tracker: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error initializing expense tracker: {e}")
        sys.exit(1)
    
    while True:
        try:
            print("\nOptions:")
            print("1. Add expense")
            print("2. View all expenses")
            print("3. View expenses by category")
            print("4. View summary")
            print("5. Exit")
            
            choice = get_user_input("\nSelect an option (1-5): ")
            
            if choice == '1':
                amount = get_user_input("Enter amount: $")
                description = get_user_input("Enter description: ")
                category = get_user_input("Enter category: ")
                date_input = get_user_input("Enter date (YYYY-MM-DD) or press Enter for today: ")
                
                date = date_input if date_input else None
                tracker.add_expense(amount, description, category, date)
                
            elif choice == '2':
                tracker.view_expenses()
                
            elif choice == '3':
                categories = tracker.get_categories()
                if categories:
                    print("Available categories:", ", ".join(categories))
                    category = get_user_input("Enter category: ")
                    tracker.view_expenses(category)
                else:
                    print("No categories available yet.")
                    
            elif choice == '4':
                summary = tracker.get_summary()
                if summary:
                    print("\nExpense Summary by Category:")
                    print("=" * 30)
                    for category, total in summary.items():
                        print(f"{category}: ${total:.2f}")
                else:
                    print("No expenses to summarize.")
                    
            elif choice == '5':
                print("Thank you for using Expense Tracker!")
                break
                
            else:
                print("Invalid option. Please select 1-5.")
                
        except (ValidationError, DataFileError) as e:
            print(f"Application error: {e}")
            continue
        except ExpenseTrackerError as e:
            print(f"Unexpected application error: {e}")
            continue
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Please try again or restart the application.")
            continue


if __name__ == "__main__":
    main()