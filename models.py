from flask_sqlalchemy import SQLAlchemy
from init import app
from flask_migrate import Migrate



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=True)

    def __init__(self, name, author, total):
        self.name = name
        self.author = author
        self.total = total
        self.available = total

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rollno = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    issued = db.Column(db.Integer, nullable=False)


    def __init__(self, name, rollno, dob, issued):
        self.name = name
        self.rollno = rollno
        self.dob = dob
        self.issued = issued

class Requested(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_rollno = db.Column(db.String(20), nullable=True)
    student_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(50), nullable=False)
    is_issued = db.Column(db.String(5), nullable=False)     # "yes"   or  "no"
    issued_id = db.Column(db.Integer, nullable=True)


    def __init__(self, student_rollno, student_name, date, book_name, author_name, is_issued, issued_id):
        self.student_rollno = student_rollno
        self.student_name = student_name
        self.date = date
        self.book_name = book_name
        self.author_name = author_name
        self.is_issued = is_issued
        self.issued_id = issued_id

class IssuedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    author = db.Column(db.String(50), nullable=True)
    req_date = db.Column(db.String(20), nullable=False)
    issued_date = db.Column(db.String(20), nullable=False)
    return_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)     # "requested" or "issued"


    def __init__(self, student_id, name, author, req_date, issued_date, return_date, status):
        self.student_id = student_id
        self.name = name
        self.author = author
        self.req_date = req_date
        self.issued_date = issued_date
        self.return_date = return_date
        self.status = status


with app.app_context():
    db.create_all()