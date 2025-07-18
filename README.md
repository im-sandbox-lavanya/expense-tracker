# Expense Tracker

A Python command-line application to track your expenses and categorize them for better financial management.

## Features

- **Add Expenses**: Record expenses with date, category, amount, and description
- **List Expenses**: View all recorded expenses with totals
- **CSV Export**: Export all expense data to CSV files for analysis and record-keeping
- **Excel Export**: Export all expense data to Excel files (.xlsx) with formatting and styling
- **Data Persistence**: Expenses are saved to JSON file for persistence between sessions
- **Special Character Support**: CSV and Excel export properly handle commas, quotes, and other special characters

## Installation

For basic functionality, no external dependencies are required. The application uses only Python standard library modules.

For Excel export functionality, install the required dependency:

```bash
pip install openpyxl
```

## Usage

### Running the Application

```bash
python3 expense_tracker.py
```

### Main Menu Options

1. **Add Expense**: Enter a new expense with date (YYYY-MM-DD), category, amount, and description
2. **List All Expenses**: View all recorded expenses with a summary total
3. **Export to CSV**: Export all expenses to a CSV file
4. **Export to Excel**: Export all expenses to an Excel file (.xlsx) with formatting
5. **Exit**: Close the application

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

### Excel Export Feature

The Excel export functionality provides enhanced formatting and professional appearance:

- Export all expense data to an Excel file (.xlsx format)
- Professional styling with colored headers and formatted columns
- Auto-adjusted column widths for optimal readability
- Bold summary total row for quick reference
- Handles special characters seamlessly
- Compatible with Microsoft Excel, LibreOffice Calc, and Google Sheets

**Export Options:**
- **Custom filename**: Enter your preferred filename when prompted (automatically adds .xlsx extension)
- **Auto-generated**: Press Enter to use timestamp-based filename (e.g., `expenses_export_20240115_143022.xlsx`)

**Excel Features:**
- Styled header row with blue background and white text
- Auto-adjusted column widths
- Bold formatting for the total amount
- Professional appearance suitable for reporting

### Example CSV Output

```csv
date,category,amount,description
2024-01-15,Food,25.5,Lunch at restaurant
2024-01-16,Transport,15.0,Bus fare
2024-01-17,Entertainment,45.75,"Movie tickets, popcorn"
```

### Example Excel Output

The Excel export creates a professionally formatted spreadsheet with:
- Blue header row with white text
- Auto-sized columns for easy reading
- Bold total row for summary information
- Compatible with all major spreadsheet applications

## Data Storage

Expenses are stored in a local JSON file (`expenses.json`) which is created automatically when you add your first expense. The file can be safely deleted to start fresh.

## Error Handling

The application includes robust error handling for:
- Invalid input formats
- File I/O operations
- CSV export failures
- Excel export failures (with graceful fallback if openpyxl is not installed)
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

This will create sample expenses and demonstrate both the CSV and Excel export functionality.