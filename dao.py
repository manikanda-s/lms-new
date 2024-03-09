from models import Book, Student, Requested, IssuedBook, db
from datetime import date, timedelta


class DB_Helper:
    # book List
    def add_book_db(self, name, author, total):
        book = Book(name, author, total)
        db.session.add(book)
        db.session.commit()

    def get_books(self):
        return Book.query.all()

    def get_book_by_id(self, id):
        return Book.query.filter_by(id = id).first()

    def update_book_db(self, id, book_name, author_name, total):
        book = Book.query.filter_by(id = id).first()
        book.name = book_name
        book.author = author_name
        book.total = total
        db.session.commit()

    # student list
    def add_student_db(self, student_name, roll_no, dob):
        student = Student(student_name, roll_no, dob, 0)
        db.session.add(student)
        db.session.commit()

    def get_students(self):
        return Student.query.all()
    
    def get_student_by_id(self, id):
        return Student.query.filter_by(id = id).first()

    def update_student_db(self, id, student_name, roll_no, dob):
        student = Student.query.filter_by(id = id).first()
        student.name = student_name
        student.rollno = roll_no
        student.dob = dob
        db.session.commit()

    def get_student_by_rollno(self, rollno):
        return Student.query.filter_by(rollno = rollno).first()

    def search_book_db(self, book_name):
        return Book.query.filter(Book.name.like('%' + book_name + '%')).all()

    def add_req(self, current_user_rollno, book_id):
        student = Student.query.filter_by(rollno = current_user_rollno).first()
        book = Book.query.filter_by(id = book_id).first()
        today_date = date.today()

        # add issued book list
        issued_book = IssuedBook(student.id, book.name, book.author, today_date, "-", "-", "requested")
        db.session.add(issued_book)
        db.session.commit()

        # print("rollno", current_user_rollno, "book_id", book_id)
        # print(student)
        # print(student.name, today_date, book.name, book.author, "no")
        req = Requested(student.rollno, student.name, today_date, book.name, book.author, "no", issued_book.id)
        db.session.add(req)
        db.session.commit()

        # decrease available book count
        book.available = book.available - 1
        db.session.commit()

        

    def get_requested_db(self):
        return Requested.query.filter_by(is_issued = 'no').all()

    def book_issued(self, id):
        req = Requested.query.filter_by(id = id).first()
        req.is_issued = 'yes'
        # db.session.commit()

        issued_id = req.issued_id
        issued_book = IssuedBook.query.filter_by(id = issued_id).first()
        print(issued_id)
        print(issued_book)
        issued_book.issued_date = str(date.today())
        delta = timedelta(days=7)
        issued_book.return_date = (date.today() + delta)
        issued_book.status = "issued"
        db.session.commit()






    def get_issued_books_db(self, current_user_rollno):
        print(current_user_rollno)
        student = Student.query.filter_by(rollno = current_user_rollno).first()
        print(student)
        id = student.id
        print(id)
        issued_list = IssuedBook.query.filter_by(student_id = id).all()
        return issued_list

        



