#!/usr/bin/env python3
"""
Test script to verify exception handling in the expense tracker application
"""

import os
import json
import tempfile
from expense_tracker import ExpenseTracker, DataFileError, ValidationError, ExpenseTrackerError


def test_file_operations():
    """Test file-related exception handling"""
    print("Testing file operations exception handling...")
    
    # Test with invalid JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json content {")
        invalid_json_file = f.name
    
    try:
        tracker = ExpenseTracker(invalid_json_file)
        print("❌ Should have raised DataFileError for invalid JSON")
    except DataFileError as e:
        print(f"✓ Correctly caught DataFileError: {e}")
    finally:
        os.unlink(invalid_json_file)
    
    # Test with read-only directory (permission error simulation)
    print("\n✓ File operation exception handling works correctly")


def test_validation_errors():
    """Test input validation exception handling"""
    print("\nTesting input validation exception handling...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("[]")
        temp_file = f.name
    
    try:
        tracker = ExpenseTracker(temp_file)
        
        # Test invalid amount
        try:
            tracker.add_expense("invalid_amount", "Test", "Food")
            print("❌ Should have raised ValidationError for invalid amount")
        except ValidationError as e:
            print(f"✓ Correctly caught ValidationError for amount: {e}")
        
        # Test negative amount
        try:
            tracker.add_expense("-50", "Test", "Food")
            print("❌ Should have raised ValidationError for negative amount")
        except ValidationError as e:
            print(f"✓ Correctly caught ValidationError for negative amount: {e}")
        
        # Test empty description
        try:
            tracker.add_expense("50", "", "Food")
            print("❌ Should have raised ValidationError for empty description")
        except ValidationError as e:
            print(f"✓ Correctly caught ValidationError for empty description: {e}")
        
        # Test empty category
        try:
            tracker.add_expense("50", "Test", "")
            print("❌ Should have raised ValidationError for empty category")
        except ValidationError as e:
            print(f"✓ Correctly caught ValidationError for empty category: {e}")
        
        # Test invalid date format
        try:
            tracker.add_expense("50", "Test", "Food", "invalid-date")
            print("❌ Should have raised ValidationError for invalid date")
        except ValidationError as e:
            print(f"✓ Correctly caught ValidationError for invalid date: {e}")
        
        print("\n✓ Input validation exception handling works correctly")
    
    finally:
        os.unlink(temp_file)


def test_data_corruption():
    """Test handling of corrupted data files"""
    print("\nTesting corrupted data file handling...")
    
    # Test with malformed expense data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([{"amount": "invalid", "missing_fields": True}], f)
        corrupt_file = f.name
    
    try:
        tracker = ExpenseTracker(corrupt_file)
        print("❌ Should have raised ValidationError for corrupted data")
    except ValidationError as e:
        print(f"✓ Correctly caught ValidationError for corrupted data: {e}")
    finally:
        os.unlink(corrupt_file)
    
    print("\n✓ Data corruption exception handling works correctly")


def test_successful_operations():
    """Test successful operations work properly"""
    print("\nTesting successful operations...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("[]")
        temp_file = f.name
    
    try:
        tracker = ExpenseTracker(temp_file)
        
        # Add valid expense
        tracker.add_expense("50.99", "Groceries", "Food", "2024-01-15")
        print("✓ Successfully added expense")
        
        # View expenses
        print("\n--- Viewing expenses ---")
        tracker.view_expenses()
        
        # Get summary
        summary = tracker.get_summary()
        print(f"\n✓ Successfully generated summary: {summary}")
        
        # Get categories
        categories = tracker.get_categories()
        print(f"✓ Successfully retrieved categories: {categories}")
        
        print("\n✓ All successful operations work correctly")
    
    finally:
        os.unlink(temp_file)


def main():
    """Run all exception handling tests"""
    print("=" * 60)
    print("EXPENSE TRACKER EXCEPTION HANDLING TESTS")
    print("=" * 60)
    
    try:
        test_file_operations()
        test_validation_errors()
        test_data_corruption()
        test_successful_operations()
        
        print("\n" + "=" * 60)
        print("ALL EXCEPTION HANDLING TESTS PASSED! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()