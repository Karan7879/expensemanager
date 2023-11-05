from pymongo import MongoClient


client = MongoClient("mongodb+srv://<username>:<password>@cluster0.jwi0z9m.mongodb.net/?retryWrites=true&w=majority")
db = client["expense_manager3"]
users_collection = db["users"]
expenses_collection = db["expenses"]