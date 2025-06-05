from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import os
from datetime import datetime
import io
import pandas as pd  # Requires 'pandas' and 'xlsxwriter' packages for Excel export

app = Flask(__name__)
DATA_FILE = 'expenses.json'

# Load expenses from file
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save expenses to file
def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']  # new field for user name
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')
        expense = {
            'name': name,  # include name in expense
            'amount': float(amount),
            'category': category,
            'description': description,
            'date': date
        }
        expenses = load_expenses()
        expenses.append(expense)
        save_expenses(expenses)
        return redirect(url_for('index'))
    expenses = load_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/export', methods=['GET'])
def export():
    """
    Exports the list of expenses to an Excel (.xlsx) file and sends it as a downloadable attachment.

    Returns:
        Response: A Flask response object containing the Excel file for download.

    Raises:
        Any exceptions raised by `load_expenses`, `pd.DataFrame`, or file operations will propagate.
    """
    expenses = load_expenses()
    df = pd.DataFrame(expenses)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Expenses')
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='expenses.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True)
