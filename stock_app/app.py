from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from alpha_api.summarizeOutput import *
import ast
import os
from flask_wtf.csrf import CsrfProtect


csrf = CsrfProtect()

app = Flask(__name__, template_folder='templates')
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



stock_list = {"Warren Buffett Top 10": ['AAPL', 'BAC', 'KO', 'AXP', 'KHC', 'WFC', 'BK', 'V', 'GM', 'KR'],
              "Famous Youtuber Top 15": ['XOM', 'DUK', 'INTC', 'O', 'SO', 'JNJ', 'MMM', 'IBM','VYM', 'PEP'],
              "Top Dividend ETFs": ['VIG', 'NOBL', 'SDY', 'SCHD', 'IDV', 'DGRO', 'DON', 'FVD', 'SPHD'],
              "Kiplinger Top": ['BAC', 'CMCSA', 'BA', 'JNJ', 'MRK', 'HD', 'C', 'JPM', 'KO', 'VZ']

              }


class Todo2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    stock_list = db.Column(db.String(2000), nullable=False)
    portfolio_amount = db.Column(db.Integer, default=100000)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
@csrf.exempt
def index():
    if request.method == 'GET' and len(Todo2.query.order_by(Todo2.portfolio_amount).all()) == 0:
        return render_template(
            'index.html',
            data=[{'name': 'Warren Buffett Top 10'}, {'name': 'Kiplinger Top'}, {'name': 'Famous Youtuber Top 15'},
                  {'name': 'Top Dividend ETFs'}])

    if request.method == 'POST':

        task_content = request.form['comp_select']

        allocation_percentage = round(100 / len(stock_list[task_content]), 2)

        st_ls = [(stock, f"{allocation_percentage}%") for stock in stock_list[task_content]]

        new_task = Todo2(content=task_content, stock_list=str(st_ls))

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo2.query.order_by(Todo2.portfolio_amount).all()
        stocks_to_trade = dict(ast.literal_eval(tasks[0].stock_list))
        print(stocks_to_trade)
        stock_allocation = (int(tasks[0].portfolio_amount))
        stock_data = stockListDividendOutput(stocks_to_trade, stock_allocation, '01-2018', 'maximum high')

        bar_labels = stock_data['month_year_stock']
        bar_values = stock_data['dividends_monthly']
        line_values = stock_data['value_monthly']

        dividends_received = round(stock_data['dividends_received'])
        portfolio_value = round(stock_data['portfolio_value'])

        return render_template('index.html', tasks=tasks, max=17000, labels=bar_labels, values_bar=bar_values,
                               values_line=line_values, dividends_received=dividends_received,
                               portfolio_value=portfolio_value)

@csrf.exempt
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo2.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@csrf.exempt
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo2.query.get_or_404(id)

    if request.method == 'POST':
        task.stock_list = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@csrf.exempt
@app.route('/update_allocation/<int:id>', methods=['GET', 'POST'])
def update_allocation(id):
    task = Todo2.query.get_or_404(id)

    if request.method == 'POST':
        task.portfolio_amount = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update_allocation.html', task=task)


def init_db():
    """For use on command line for setting up
    the database.
    """

    csrf.init_app(app)

    db.init_app(app)
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', debug=True)
