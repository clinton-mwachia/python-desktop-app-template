from utils.database import Database

class TodoModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('todos')

    def add_todo(self, user_id, title, description):
        todo = {"user_id": user_id, "title": title, "description": description}
        self.collection.insert_one(todo)

    def get_todos(self, user_id):
        return self.collection.find({"user_id": user_id})

    def update_todo(self, todo_id, title=None, description=None):
        update = {}
        if title:
            update["title"] = title
        if description:
            update["description"] = description
        self.collection.update_one({"_id": todo_id}, {"$set": update})

    def delete_todo(self, todo_id):
        self.collection.delete_one({"_id": todo_id})
