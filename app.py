from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'expenses.json'

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

@app.route('/')
def index():
    expenses = load_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')
        expenses = load_expenses()
        expenses.append({'description': description, 'amount': amount, 'date': date})
        save_expenses(expenses)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:idx>', methods=['POST'])
def delete_expense(idx):
    expenses = load_expenses()
    if 0 <= idx < len(expenses):
        expenses.pop(idx)
        save_expenses(expenses)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
