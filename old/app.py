from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outcomes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Outcome Model
class Outcome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

# Create tables in the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    outcomes = Outcome.query.all()
    return render_template('index.html', outcomes=outcomes)

@app.route('/add', methods=['POST'])
def add_outcome():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date_str = request.form['date']

        # Convert the date string to a Python date object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        new_outcome = Outcome(description=description, amount=amount, date=date_obj)
        db.session.add(new_outcome)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_outcome(id):
    outcome_to_delete = Outcome.query.get(id)
    db.session.delete(outcome_to_delete)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
