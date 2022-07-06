from unicodedata import category
from pymongo import MongoClient,ASCENDING, TEXT
from util import books_db
import json


def get_books():
    data = books_db.find()
    return data

def get_books_name(text):
    if text is None or len(text) <= 0:
        return None
    try:
        books_db.create_index([("name",TEXT)],default_language="english")
        data = books_db.find({'$text':{'$search':text}}).sort('rent', ASCENDING)
    except:
        print("Error fetching data")
    return data


def get_books_rent(rent_l,rent_u):
    if rent_l > rent_u:
        rent_l, rent_u = rent_u, rent_l
    try:
        data = books_db.find({"rent":{"$gte":rent_l,"$lte":rent_u}})
    except:
        data = None
    return data

def get_books_query(category,name,rent_l,rent_u):
    if rent_l > rent_u:
        rent_l, rent_u = rent_u, rent_l
    if (category == None or len(category) <= 0) or (name == None or len(name) <= 0):
        return None
    try:
        #books_db.create_index([("name",TEXT),("category",TEXT)],default_language="english")
        data = books_db.find({'category': category,
            '$and': [
                    {'$text':{'$search':name}},
                    {"rent":{"$gte":rent_l,"$lte":rent_u}}
                ]
        }).sort('rent',ASCENDING)
    except:
        data = None
        print("Error!")
    return data




# books = get_books_rent(10,25)
# for book in books:
#     print(book)

# books = get_books_name("The Body")
# for book in books:
#     print(book)

# books = get_books_query("Finance","Grow",10,100)
# for book in books:
#     print(book)



