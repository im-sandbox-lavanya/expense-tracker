#!/usr/bin/env python3
"""
Test suite for the Expense Tracker application.
"""

import unittest
import os
import csv
import json
import tempfile
from expense_tracker import Expense, ExpenseTracker


class TestExpense(unittest.TestCase):
    """Test cases for the Expense class."""
    
    def test_expense_creation(self):
        """Test expense object creation."""
        expense = Expense("2024-01-15", "Food", 25.50, "Lunch at restaurant")
        self.assertEqual(expense.date, "2024-01-15")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.description, "Lunch at restaurant")
    
    def test_expense_to_dict(self):
        """Test expense to dictionary conversion."""
        expense = Expense("2024-01-15", "Food", 25.50, "Lunch at restaurant")
        expected = {
            'date': "2024-01-15",
            'category': "Food",
            'amount': 25.50,
            'description': "Lunch at restaurant"
        }
        self.assertEqual(expense.to_dict(), expected)
    
    def test_expense_from_dict(self):
        """Test expense creation from dictionary."""
        data = {
            'date': "2024-01-15",
            'category': "Food",
            'amount': 25.50,
            'description': "Lunch at restaurant"
        }
        expense = Expense.from_dict(data)
        self.assertEqual(expense.date, "2024-01-15")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.description, "Lunch at restaurant")


class TestExpenseTracker(unittest.TestCase):
    """Test cases for the ExpenseTracker class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, 'test_expenses.json')
        self.tracker = ExpenseTracker(self.test_data_file)
    
    def tearDown(self):
        """Clean up test environment."""
        # Clean up any created files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        
        # Clean up CSV files in temp directory
        for file in os.listdir(self.temp_dir):
            if file.endswith('.csv'):
                os.remove(os.path.join(self.temp_dir, file))
    
    def test_add_expense(self):
        """Test adding an expense."""
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch")
        self.assertEqual(len(self.tracker.expenses), 1)
        expense = self.tracker.expenses[0]
        self.assertEqual(expense.date, "2024-01-15")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.description, "Lunch")
    
    def test_save_and_load_expenses(self):
        """Test saving and loading expenses."""
        # Add expenses
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch")
        self.tracker.add_expense("2024-01-16", "Transport", 15.00, "Bus fare")
        
        # Create new tracker instance to test loading
        new_tracker = ExpenseTracker(self.test_data_file)
        self.assertEqual(len(new_tracker.expenses), 2)
        
        # Verify data integrity
        expenses = new_tracker.expenses
        self.assertEqual(expenses[0].date, "2024-01-15")
        self.assertEqual(expenses[0].category, "Food")
        self.assertEqual(expenses[1].date, "2024-01-16")
        self.assertEqual(expenses[1].category, "Transport")
    
    def test_delete_expense_valid_index(self):
        """Test deleting an expense with valid index."""
        # Add test expenses
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch")
        self.tracker.add_expense("2024-01-16", "Transport", 15.00, "Bus fare")
        self.assertEqual(len(self.tracker.expenses), 2)
        
        # Delete first expense
        result = self.tracker.delete_expense(0)
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.expenses), 1)
        
        # Verify remaining expense
        self.assertEqual(self.tracker.expenses[0].date, "2024-01-16")
        self.assertEqual(self.tracker.expenses[0].category, "Transport")
    
    def test_delete_expense_invalid_index(self):
        """Test deleting an expense with invalid index."""
        # Add test expense
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch")
        
        # Try to delete with invalid indices
        result1 = self.tracker.delete_expense(-1)
        self.assertFalse(result1)
        result2 = self.tracker.delete_expense(1)
        self.assertFalse(result2)
        
        # Verify expense still exists
        self.assertEqual(len(self.tracker.expenses), 1)
    
    def test_delete_expense_empty_list(self):
        """Test deleting from empty expense list."""
        result = self.tracker.delete_expense(0)
        self.assertFalse(result)
    
    def test_edit_expense_valid_index(self):
        """Test editing an expense with valid index."""
        # Add test expense
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch")
        
        # Edit the expense
        result = self.tracker.edit_expense(0, "2024-01-20", "Transport", 30.00, "Taxi ride")
        self.assertTrue(result)
        
        # Verify changes
        expense = self.tracker.expenses[0]
        self.assertEqual(expense.date, "2024-01-20")
        self.assertEqual(expense.category, "Transport")
        self.assertEqual(expense.amount, 30.00)
        self.assertEqual(expense.description, "Taxi ride")
    
    def test_edit_expense_invalid_index(self):
        """Test editing an expense with invalid index."""
        # Add test expense
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch")
        
        # Try to edit with invalid indices
        result1 = self.tracker.edit_expense(-1, "2024-01-20", "Transport", 30.00, "Taxi")
        self.assertFalse(result1)
        result2 = self.tracker.edit_expense(1, "2024-01-20", "Transport", 30.00, "Taxi")
        self.assertFalse(result2)
        
        # Verify expense unchanged
        expense = self.tracker.expenses[0]
        self.assertEqual(expense.date, "2024-01-15")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.description, "Lunch")
    
    def test_edit_expense_empty_list(self):
        """Test editing from empty expense list."""
        result = self.tracker.edit_expense(0, "2024-01-20", "Transport", 30.00, "Taxi")
        self.assertFalse(result)


class TestCSVExport(unittest.TestCase):
    """Test cases for CSV export functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, 'test_expenses.json')
        self.tracker = ExpenseTracker(self.test_data_file)
        
        # Add test data
        self.tracker.add_expense("2024-01-15", "Food", 25.50, "Lunch at restaurant")
        self.tracker.add_expense("2024-01-16", "Transport", 15.00, "Bus fare")
        self.tracker.add_expense("2024-01-17", "Entertainment", 45.75, "Movie, popcorn")
        self.tracker.add_expense("2024-01-18", "Food", 12.25, "Coffee, pastry")
    
    def tearDown(self):
        """Clean up test environment."""
        # Clean up files
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    def test_export_to_csv_basic(self):
        """Test basic CSV export functionality."""
        csv_file = os.path.join(self.temp_dir, 'test_export.csv')
        result = self.tracker.export_to_csv(csv_file)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(csv_file))
        
        # Verify CSV content
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            self.assertEqual(len(rows), 4)
            
            # Check first row
            self.assertEqual(rows[0]['date'], "2024-01-15")
            self.assertEqual(rows[0]['category'], "Food")
            self.assertEqual(rows[0]['amount'], "25.5")
            self.assertEqual(rows[0]['description'], "Lunch at restaurant")
            
            # Check that all expected columns are present
            expected_columns = {'date', 'category', 'amount', 'description'}
            self.assertEqual(set(rows[0].keys()), expected_columns)
    
    def test_export_to_csv_with_special_characters(self):
        """Test CSV export with special characters in descriptions."""
        # Add expense with special characters
        self.tracker.add_expense("2024-01-19", "Food", 30.00, "Lunch, \"quoted\", with commas")
        
        csv_file = os.path.join(self.temp_dir, 'test_special_chars.csv')
        result = self.tracker.export_to_csv(csv_file)
        
        self.assertTrue(result)
        
        # Verify CSV handles special characters correctly
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            # Find the row with special characters
            special_row = None
            for row in rows:
                if "quoted" in row['description']:
                    special_row = row
                    break
            
            self.assertIsNotNone(special_row)
            self.assertEqual(special_row['description'], "Lunch, \"quoted\", with commas")
    
    def test_export_empty_expenses(self):
        """Test CSV export with no expenses."""
        empty_tracker = ExpenseTracker(os.path.join(self.temp_dir, 'empty.json'))
        csv_file = os.path.join(self.temp_dir, 'empty_export.csv')
        
        result = empty_tracker.export_to_csv(csv_file)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(csv_file))
    
    def test_export_auto_filename(self):
        """Test CSV export with auto-generated filename."""
        # Change to temp directory to control where file is created
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            result = self.tracker.export_to_csv()
            self.assertTrue(result)
            
            # Check that a CSV file was created
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            self.assertEqual(len(csv_files), 1)
            
            # Verify the auto-generated file contains correct data
            csv_file = csv_files[0]
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 4)
        
        finally:
            os.chdir(original_cwd)
    
    def test_export_large_dataset(self):
        """Test CSV export with a larger dataset."""
        # Add more expenses to test with larger dataset
        categories = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare"]
        
        for i in range(100):
            date = f"2024-01-{(i % 28) + 1:02d}"
            category = categories[i % len(categories)]
            amount = round(10.0 + (i * 1.5), 2)
            description = f"Test expense {i} with description"
            self.tracker.add_expense(date, category, amount, description)
        
        csv_file = os.path.join(self.temp_dir, 'large_export.csv')
        result = self.tracker.export_to_csv(csv_file)
        
        self.assertTrue(result)
        
        # Verify all data is exported
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # Original 4 + 100 new expenses
            self.assertEqual(len(rows), 104)


if __name__ == '__main__':
    unittest.main()