from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, template_folder='template')

# Database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:root@localhost/todolist'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ToDo {self.task}>'

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = ToDo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo_text = request.form['todo']
    new_todo = ToDo(task=todo_text, done=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    todo = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        todo.task = request.form['todo']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', todo=todo)

@app.route('/check/<int:id>')
def check(id):
    todo = ToDo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)






