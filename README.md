# Expense Tracker

Create a python script to track your expenses and categorize them for better financial management.

## Features

- Track expenses with categories and descriptions
- View all expenses with totals
- Export expenses to CSV format
- Persistent data storage
- Command-line interface and interactive mode

## Usage

### Interactive Mode
```bash
python expense_tracker.py
```

### Command-Line Mode
```bash
# Export to CSV
python expense_tracker.py export [filename]

# Add expense
python expense_tracker.py add <amount> <category> [description]

# View expenses
python expense_tracker.py view

# Show help
python expense_tracker.py help
```

### Examples
```bash
# Add expenses
python expense_tracker.py add 25.50 "Groceries" "Weekly shopping"
python expense_tracker.py add 12.00 "Transport" "Bus fare"

# View all expenses
python expense_tracker.py view

# Export to CSV
python expense_tracker.py export my_expenses.csv
```

## CSV Export Format

The CSV export includes the following fields:
- `date`: Date and time of the expense
- `amount`: Amount spent
- `category`: Expense category
- `description`: Optional description