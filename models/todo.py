from utils.database import Database
from bson.objectid import ObjectId
from datetime import datetime

class TodoModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('todos')

    def add_todo(self, user_id, title, description, status='active'):
        todo = {"user_id": user_id, "title": title, "description": description, 
                'status':status,'created_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),'updated_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
        self.collection.insert_one(todo)

    def add_many_todos(self, todos):
        self.collection.insert_many(todos)

    def get_todos(self, user_id):
        return self.collection.find({"user_id": user_id}).sort('created_at', -1)

    def update_todo(self, todo_id, title=None, description=None, status=None):
        update = {'updated_at': datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
        if title:
            update["title"] = title
        if description:
            update["description"] = description
        if status:
            update["status"] = status
        self.collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update})

    def delete_todo(self, todo_id):
        self.collection.delete_one({"_id": ObjectId(todo_id)})

    def get_total_todos(self, user_id):
        return self.collection.count_documents({"user_id": user_id})
    
    def get_completed_todos(self):
        return self.collection.count_documents({"status": 'completed'})
    
    def count_todos_by_status(self, status):
        return self.collection.count_documents({"status": status})

    def get_latest_todos(self, limit=10):
        return list(self.collection.find().sort('created_at', -1).limit(limit))