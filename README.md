# Expense Tracker

A Python command-line application to track your expenses and categorize them for better financial management.

## Features

- **Add Expenses**: Record expenses with date, category, amount, and description
- **List Expenses**: View all recorded expenses with totals
- **Edit Expenses**: Modify existing expenses with pre-populated current values
- **Delete Expenses**: Remove expenses with confirmation prompts
- **CSV Export**: Export all expense data to CSV files for analysis and record-keeping
- **Data Persistence**: Expenses are saved to JSON file for persistence between sessions
- **Special Character Support**: CSV export properly handles commas, quotes, and other special characters

## Installation

No external dependencies required. The application uses only Python standard library modules.

## Usage

### Running the Application

```bash
python3 expense_tracker.py
```

### Main Menu Options

1. **Add Expense**: Enter a new expense with date (YYYY-MM-DD), category, amount, and description
2. **List All Expenses**: View all recorded expenses with a summary total
3. **Export to CSV**: Export all expenses to a CSV file
4. **Edit Expense**: Modify existing expenses - displays indexed list for selection, shows current values for easy editing
5. **Delete Expense**: Remove expenses with confirmation - displays indexed list for selection and requires confirmation
6. **Exit**: Close the application

### CSV Export Feature

The CSV export functionality allows you to:

- Export all expense data to a CSV file
- Choose a custom filename or use auto-generated timestamps
- Handle special characters properly (commas, quotes, etc.)
- Create files suitable for import into spreadsheet applications

**Export Options:**
- **Custom filename**: Enter your preferred filename when prompted
- **Auto-generated**: Press Enter to use timestamp-based filename (e.g., `expenses_export_20240115_143022.csv`)

**CSV Format:**
The exported CSV includes the following columns:
- `date`: Expense date in YYYY-MM-DD format
- `category`: Expense category
- `amount`: Expense amount (numeric)
- `description`: Expense description

### Example CSV Output

```csv
date,category,amount,description
2024-01-15,Food,25.5,Lunch at restaurant
2024-01-16,Transport,15.0,Bus fare
2024-01-17,Entertainment,45.75,"Movie tickets, popcorn"
```

## Data Storage

Expenses are stored in a local JSON file (`expenses.json`) which is created automatically when you add your first expense. The file can be safely deleted to start fresh.

## Error Handling

The application includes robust error handling for:
- Invalid input formats
- File I/O operations
- CSV export failures
- Data corruption recovery

## Testing

Run the test suite to verify functionality:

```bash
python3 -m unittest test_expense_tracker.py -v
```

## Demo

Run the demo script to see the application in action:

```bash
python3 demo.py
```

This will create sample expenses and demonstrate the CSV export functionality.