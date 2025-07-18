# Expense Tracker

A command-line expense tracking application with comprehensive exception handling for better financial management.

## Features

- Add expenses with amount, description, category, and date
- View all expenses or filter by category
- Generate expense summaries by category
- Robust exception handling for all operations
- Data persistence using JSON files
- Input validation and error recovery

## Usage

Run the application:
```bash
python3 expense_tracker.py
```

## Exception Handling

The application includes comprehensive exception handling for:

### File Operations
- **DataFileError**: Handles file read/write errors, permission issues, and invalid JSON
- Automatic backup creation before saving
- Graceful handling of missing or corrupted data files

### Input Validation
- **ValidationError**: Validates all user inputs including:
  - Amount format and positive values
  - Non-empty descriptions and categories
  - Date format (YYYY-MM-DD)
  - Data structure integrity

### User Experience
- **ExpenseTrackerError**: Catches unexpected errors with meaningful messages
- Keyboard interrupt handling (Ctrl+C)
- EOF handling for input streams
- Application continues running after recoverable errors

## Testing

Run the exception handling tests:
```bash
python3 test_exception_handling.py
```

## Data Storage

- Expenses are stored in `expenses.json`
- Automatic backup files created as `expenses.json.backup`
- Data validation ensures file integrity

## Error Recovery

The application is designed to recover gracefully from errors:
- Invalid inputs prompt for re-entry
- File corruption is detected and reported
- Missing files are automatically created
- Permission errors are clearly communicated