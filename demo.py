#!/usr/bin/env python3
"""
Quick demo script to verify expense tracker functionality.
"""

import os
from expense_tracker import ExpenseTracker

def demo_expense_tracker():
    """Demonstrate the expense tracker functionality."""
    print("=== Expense Tracker Demo ===")
    
    # Create tracker instance
    tracker = ExpenseTracker('demo_expenses.json')
    
    # Add some sample expenses
    print("\n1. Adding sample expenses...")
    tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch at restaurant")
    tracker.add_expense("2024-01-16", "Transport", 15.00, "Bus fare")
    tracker.add_expense("2024-01-17", "Entertainment", 45.75, "Movie tickets, popcorn")
    tracker.add_expense("2024-01-18", "Food", 12.25, "Coffee and pastry")
    tracker.add_expense("2024-01-19", "Utilities", 85.00, "Electricity bill")
    tracker.add_expense("2024-01-20", "Food", 30.00, "Dinner with special chars: commas, \"quotes\"")
    
    # List all expenses
    print("\n2. Listing all expenses:")
    tracker.list_expenses()
    
    # Export to CSV
    print("\n3. Exporting to CSV...")
    success = tracker.export_to_csv("demo_export.csv")
    
    if success:
        print("\n4. Verifying CSV export...")
        if os.path.exists("demo_export.csv"):
            with open("demo_export.csv", 'r', encoding='utf-8') as f:
                content = f.read()
                print("CSV Content:")
                print("-" * 50)
                print(content)
                print("-" * 50)
        else:
            print("Error: CSV file was not created")
    else:
        print("Export failed!")
    
    # Export to Excel
    print("\n5. Exporting to Excel...")
    excel_success = tracker.export_to_excel("demo_export.xlsx")
    
    if excel_success:
        print("\n6. Verifying Excel export...")
        if os.path.exists("demo_export.xlsx"):
            file_size = os.path.getsize("demo_export.xlsx")
            print(f"Excel file created successfully: {file_size} bytes")
        else:
            print("Error: Excel file was not created")
    else:
        print("Excel export failed!")
    
    # Test auto-generated filename
    print("\n7. Testing auto-generated filename...")
    tracker.export_to_csv()
    tracker.export_to_excel()
    
    # List files created
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    print(f"\nCSV files created: {csv_files}")
    print(f"Excel files created: {xlsx_files}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_expense_tracker()