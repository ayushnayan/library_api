from pymongo import ASCENDING, TEXT,DESCENDING
from util import books_db,transaction_db
from datetime import date





def getNdays(d1,d2):
    d1 = d1.split('-')
    d2 = d2.split('-')
    date1 = date(int(d1[0]),int(d1[1]),int(d1[2]))
    date2 = date(int(d2[0]),int(d2[1]),int(d2[2]))
    ndays = (date1 - date2).days
    return ndays


def issue_book(book_name,person_name,issue_date):
    book = books_db.find_one({"name":book_name})
    data = {
        "name" : book['name'],
        "person": person_name,
        "rent" : book['rent'],
        "date": issue_date,
        "t_type": "issue",
        "t_rent": 0
    }
    print(data)
    try:
        transaction_db.insert_one(data)
        message =  {
               "book name" : book['name'],
               "person name" : person_name,
               "rent": book['rent']
            }
        return message
    except:
        print("Error!")
        return "Error issuing the book!"



def return_book(book_name,person_name,return_date):
    try:
        data = transaction_db.find({'name':book_name,"person":person_name,"t_type":"issue"}).sort('date',DESCENDING)
    except:
        return "No such entry exists!"
    book = data[0]
    ndays = getNdays(return_date,book['date'])
    rent = book['rent'] * ndays 
    u_data = {
        "name" : book['name'],
        "person": person_name,
        "rent" : book['rent'],
        "date": return_date,
        "t_type": "return",
        "t_rent": rent
    }
    try:
        transaction_db.insert_one(u_data)
        #print(u_data)
        message = { 
            "Total Rent" : str(rent)+ "rupees", 
            "total no of days": ndays, 
            "book rent per day": book['rent']
            }
        return message
    except:
        #print("Error!")
        return "Error returning the book!"



def get_list_book(book_name):
    try:
        data = transaction_db.find({"name":book_name}).sort('date',DESCENDING)
    except:
        return "No such book exists!"
    curr = []
    prev = []
    if data is not None:
        for item in data:
            if item['t_type'] == 'return':
                prev.append(item['person'])
            else:
                if prev.count(item['person']) == 0:
                    curr.append(item['person'])
    message = {
        "Issued by " : len(prev),
        "Issued by (names) ": prev,
        "Issued to ": curr
    }
    return message


def get_list_person(person_name):
    try:
        data = transaction_db.find({"person":person_name}).sort('date',DESCENDING)
    except:
        return "No such person exists in database"
    booklist = []
    if data is not None:
        for item in data:
            booklist.append(item['name'])
    message = {
        "List of books": booklist
    }
    return message


def get_revenue(book_name):
    try:
        data = transaction_db.find({"name":book_name}).sort('date',DESCENDING)
    except:
        return "No such book exists in the database"
    revenue = 0
    if data is not None:
        for item in data:
            revenue += item['t_rent']
    message = {
        "Total revenue (in Rupees) " : revenue 
    }
    return message

def get_booklist(date_l,date_u):
    try:
        data = transaction_db.find({'date':{'$gte':date_u, '$lte':date_l}}).sort('date', DESCENDING)
    except:
        return "No such record exists"
    booklist = []    
    if data is not None:
        for item in data:
            booklist.append((item['name'], item['person']))
    message = {
        "list of book and people" : booklist
    }
    return message



