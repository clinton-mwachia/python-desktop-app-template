from utils.database import Database
from bson.objectid import ObjectId

class UserModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('users')

    def create_user(self, username, password, email=None):
        user = {"username": username, "password": password}
        if email:
            user['email'] = email
        self.collection.insert_one(user)

    def find_user(self, username):
        return self.collection.find_one({"username": username})

    def validate_user(self, username, password):
        user = self.find_user(username)
        return user and user['password'] == password

    def get_all_users(self):
        return self.collection.find()

    def update_user(self, user_id, username, password, email=None):
        update_data = {"username": username, "password": password}
        if email:
            update_data['email'] = email
        self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    def delete_user(self, user_id):
        self.collection.delete_one({"_id": ObjectId(user_id)})
