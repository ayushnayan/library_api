from flask import Flask, jsonify, request, render_template
from books import get_books,get_books_name,get_books_query,get_books_rent
from transactions import issue_book,return_book,get_booklist,get_list_book,get_list_person,get_revenue
app = Flask(__name__)


@app.route('/')
def index():
    try:
        data = get_books()
    except:
        return "No records in the database"
    books = []
    for item in data:
        books.append({'name':item['name'],'rent':item['rent'],'category':item['category']})
    return jsonify(books)

@app.route('/api')
def home():
    return "Home Page"

@app.route('/api/books/book', methods=['GET','POST'])
def getName():
    if request.method == 'POST':
        name = request.form['book_name']
        booklist = []
        data = get_books_name(name)
        if data is not None:
            for book in data:
                booklist.append({"name":book['name'],"category":book['category'],"rent per day":book['rent']})
            return jsonify(booklist)
        else:
            return "No Matching Records Found!"
    return render_template("bookNameQuery.html")

@app.route('/api/books/rent', methods=['GET','POST'])
def getRent():
    if request.method == 'POST':
        rent_l = request.form['rent_l']
        rent_u = request.form['rent_u']
        booklist = []
        data = get_books_rent(int(rent_l),int(rent_u))
        if data is not None:
            for book in data:
                booklist.append({"name":book['name'],"category":book['category'],"rent per day":book['rent']})
            return jsonify(booklist)
        else:
            return "No Matching Records Found!"
    return render_template("rentRangeQuery.html")

@app.route('/api/books', methods=['GET','POST'])
def getQuery():
    if request.method == 'POST':
        booklist = []
        category = request.form['category']
        book_name = request.form['book_name']
        rent_l = request.form['rent_l']
        rent_u = request.form['rent_u']
        data = get_books_query(category,book_name,int(rent_l),int(rent_u))
        if data is not None:
            for book in data:
                booklist.append({"name":book['name'],"category":book['category'],"rent per day":book['rent']})
            return jsonify(booklist)
        else:
            return "No Matching Records Found!"
    return render_template("bookQuery.html")

@app.route('/api/transaction',methods=['GET','POST'])
def transaction():
    if request.method == 'POST':
        print(request)
        book_name = request.form['book_name']
        person_name = request.form['person_name']
        t_type = request.form['t_type']
        t_date = request.form['date']
        if t_type == 'issue':
            message = issue_book(book_name=book_name,person_name=person_name,issue_date=t_date)
        elif t_type == 'return':
            message = return_book(book_name=book_name,person_name=person_name,return_date=t_date)
        return message
    return render_template("base.html")    



@app.route('/api/transaction/list/book',methods=['GET','POST'])
def getListBook():
    if request.method == 'POST':
        book_name = request.form['book_name']
        message = get_list_book(book_name)
        return message
    return render_template("listByBook.html")

@app.route('/api/transaction/list/person',methods=['GET','POST'])
def getListPerson():
    if request.method == 'POST':
        person_name = request.form['person_name']
        message = get_list_person(person_name)
        return message
    return render_template("listByPerson.html")

@app.route('/api/transaction/rent/book',methods=['GET','POST'])
def getRentBook():
    if request.method == 'POST':
        book_name = request.form['book_name']
        message = get_revenue(book_name)
        return message
    return render_template("rentByBook.html")

@app.route('/api/transaction/list/date',methods=['GET','POST'])
def getListDate():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        message = get_booklist(start_date,end_date)
        return message
    return render_template("listByDate.html")


if __name__ == '__main__':
    app.debug = True
    app.run()    