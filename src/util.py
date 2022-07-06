from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@scouto.bcfipnx.mongodb.net/?retryWrites=true&w=majority")
db = client.BOOKS
books_db = db.BOOKS_DB
transaction_db = db.TRANSACTIONS_DB
