from flask import render_template, request, redirect, url_for, flash
from init import app
from dao import DB_Helper



dbh = DB_Helper()
current_user_rollno = 0

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# login routes

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/student-login')
def student_login():
    return render_template('student-login.html')

#############################################################################
#                                ADMIN INTERFACE                            #
#############################################################################

#  book list
@app.route('/book-list', methods=['GET', 'POST'])
def book_list():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if validate_admin(name, password):
            books = dbh.get_books()
            return render_template('book-list.html', books=books)
        else:
            flash('username or password is incorrect')
            return render_template('admin-login.html')
    books = dbh.get_books()
    return render_template('book-list.html', books=books)

# validate admin
def validate_admin(name, password):
    return (name == 'admin' and password == 'admin')     

# add book
@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        author_name = request.form.get('authorName')
        total = request.form.get('total')
        dbh.add_book_db(book_name, author_name, total)

        return redirect(url_for('add_book'))
    return render_template('add-book.html')

# edit book
@app.route('/editBook/<id>', methods=['GET', 'POST'])
def edit_book(id):
    id = int(id)
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        author_name = request.form.get('authorName')
        total = request.form.get('total')
        dbh.update_book_db(id, book_name, author_name, total)
        return redirect(url_for('book_list'))
  
    book = dbh.get_book_by_id(id)
    return render_template('edit-book.html', book=book)

# Student list
@app.route('/student-list')
def student_list():
    students = dbh.get_students()
    return render_template('student-list.html', students=students)

# add student
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form.get('studentName')
        roll_no = request.form.get('StudentRollNo')
        dob = request.form.get('dob')
        dbh.add_student_db(student_name, roll_no, dob)
        return redirect(url_for('add_student'))
    return render_template('add-student.html')

# edit student
@app.route('/editStudent/<id>', methods=['GET', 'POST'])
def edit_student(id):
    id = int(id)
    if request.method == 'POST':
        student_name = request.form.get('studentName')
        roll_no = request.form.get('StudentRollNo')
        dob = request.form.get('dob')
        dbh.update_student_db(id, student_name, roll_no, dob)
        return redirect(url_for('student_list'))
  
    student = dbh.get_student_by_id(id)
    return render_template('edit-student.html', student=student)

# request list
@app.route('/request-list')
def request_list():
    # students = dbh.get_students()
    requests = dbh.get_requested_db()
    return render_template('request-list.html', requests=requests)

@app.route('/issued', methods=['GET'])
def issued():
    id = request.args.get('id')
    dbh.book_issued(id)
    return redirect(url_for('request_list'))

@app.route('/logout')
def logout():
    current_user_rollno = None
    return redirect(url_for('home'))

@app.route('/returned-list')
def returned_list():
    # students = dbh.get_students()
    requests = dbh.get_returned_db()
    return render_template('returned-list.html', requests=requests)

@app.route('/returned', methods=['GET'])
def returned():
    id = request.args.get('id')
    dbh.book_returned(id)
    return redirect(url_for('returned_list'))

#############################################################################
#                               Student Interface                           #
#############################################################################


# student page
@app.route('/issued-books', methods=['GET', 'POST'])
def issued_books():
    
    if request.method == 'POST':
        rollno = request.form.get('rollno')
        password = request.form.get('password')
        global current_user_rollno
        current_user_rollno = rollno
        print("after login", current_user_rollno)
        if validate_student(rollno, password):
            issued_list = dbh.get_issued_books_db(current_user_rollno)
            student = dbh.get_student_by_rollno(current_user_rollno) 
            return render_template('issued-books.html', issued_list=issued_list, student=student)
        else:
            flash('Roll Number or Password is incorrect')
            return render_template('student-login.html')
    issued_list = dbh.get_issued_books_db(current_user_rollno)
    student = dbh.get_student_by_rollno(current_user_rollno) 
    return render_template('issued-books.html', issued_list=issued_list, student=student)

def validate_student(rollno, password):
    student = dbh.get_student_by_rollno(rollno)
    if student == None:
        return False
    return (student.rollno == rollno and student.dob == password)

@app.route('/search-book', methods=['GET', 'POST'])
def search_book():
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        books = dbh.search_book_db(book_name)
    return render_template('request-book.html', books=books)

@app.route('/request-book', methods=['GET', 'POST'])
def request_book():
    books = dbh.get_books()
    print(books)
    return render_template('request-book.html', books=books)

@app.route('/send-req', methods=['GET'])
def send_req():
    book_id = request.args.get('book_id')
    print("send_req", current_user_rollno)
    dbh.add_req(current_user_rollno, book_id)
    books = dbh.get_books()

    return render_template('request-book.html', books=books)

# @app.route('/select-book', methods=['GET', 'POST'])
# def select_book():
#     return "hello select book"


# this route only for testing...
@app.route('/test')
def test():
    req = dbh.get_requested_db()
    for r in req:
        print(r.student_rollno, r.student_name, r.date, r.book_name, r.author_name, r.is_issued)
    return "hi"

if __name__ == '__main__':
    app.run(debug=True)