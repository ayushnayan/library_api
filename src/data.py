from pymongo import MongoClient
from util import books_db
import json

print("Total documents before uploading data: {}".format(books_db.count_documents({})))


file_path = 'data.json'

def read_data(file_path):
    data = []
    f = open(file_path)
    myobj = json.load(f)
    data.append(myobj)
    f.close()
    return data

def insert_data(data):
    booklist =  data[0]['books']
    for book in booklist:
        try:
            books_db.insert_one(book)
        except:
            print("Error!")

data = read_data(file_path)
insert_data(data)



print("Total documents after uploading data: {}".format(books_db.count_documents({})))
