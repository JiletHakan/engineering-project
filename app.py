from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
db = SQLAlchemy(app)

class AddMedicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    piece = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class SellMedicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    piece = db.Column(db.Integer, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)  # Added column for selling price
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    add_medicines = AddMedicine.query.all()
    sell_medicines = SellMedicine.query.all()
    return render_template('index.html', add_medicines=add_medicines, sell_medicines=sell_medicines)

@app.route('/add_medicine', methods=['POST'])
def add_medicine_form():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        piece = int(request.form['piece'])
        price = float(request.form['price'])
        date_str = request.form['date']

        date = datetime.strptime(date_str, '%Y-%m-%d')

        new_medicine = AddMedicine(name=name, type=type, piece=piece, price=price, date=date)
        db.session.add(new_medicine)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/sell_medicine', methods=['POST'])
def sell_medicine_form():
    if request.method == 'POST':
        name = request.form['name']
        piece = int(request.form['piece'])
        sell_price = float(request.form['sell_price'])  # Added sell_price from the form
        date_str = request.form['date']

        date = datetime.strptime(date_str, '%Y-%m-%d')

        add_medicine = AddMedicine.query.filter_by(name=name).first()

        if add_medicine and add_medicine.piece >= piece:
            sold_medicine = SellMedicine(name=name, piece=piece, sell_price=sell_price, date=date)  # Added sell_price
            db.session.add(sold_medicine)

            add_medicine.piece -= piece

            if add_medicine.piece == 0:
                db.session.delete(add_medicine)

            db.session.commit()

        return redirect(url_for('index'))

@app.route('/delete_add_medicine/<string:table>/<int:id>', methods=['GET', 'POST'])
def delete_add_medicine(table, id):
    if table == 'add':
        medicine = AddMedicine.query.get(id)
        if medicine:
            db.session.delete(medicine)
            db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_sell_medicine/<string:table>/<int:id>', methods=['GET', 'POST'])
def delete_sell_medicine(table, id):
    if table == 'sell':
        medicine = SellMedicine.query.get(id)
        if medicine:
            db.session.delete(medicine)
            db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
