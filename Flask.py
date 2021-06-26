from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('title',db.String(40), nullable=False)
    surname = db.Column('author',db.String(40), nullable=False)
    country = db.Column('price',db.String, nullable=False)

    def __str__(self):
        return f'{self.id})Name: {self.name}; Surname: {self.surname}; Country: {self.country}'

db.create_all()


@app.route('/')
def home():
    all_books = Books.query.all()
    return render_template('index.html', all_books = all_books)

@app.route('/about')
def about():
    return '<h1>About Us</h1>'

@app.route('/user')
def user():
    subjects = ['Python', 'Calculus', 'DB']
    return render_template('user.html', subjects=subjects)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user'))
    if 'username' in request.args:
        user = request.args['username']
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'You are logged out'

@app.route('/registration', methods=['GET','POST'])
def registration():
    if request.method =='POST':
        n = request.form['name']
        s = request.form['surname']
        c = request.form['city']
        if n=='' or s=='' or c=='':
            flash('შეიყვანეთ მონაცემები სრულად!', 'error')
        else:
            b1 = Books(name=n, surname=s, country=c)
            db.session.add(b1)
            db.session.commit()
            flash('მონაცემები წარმატებით დაემატა', 'info')

    return render_template('register.html')

if __name__=="__main__":
    app.run(debug=True)