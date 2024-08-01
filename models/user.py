from utils.database import Database
from bson.objectid import ObjectId

class UserModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('users')

    def create_user(self, username, password, email=None, role=None):
        user = {"username": username, "password": password, "email": email, "active": True, "role": role}
        self.collection.insert_one(user)

    def find_user(self, username):
        return self.collection.find_one({"username": username})

    def validate_user(self, username, password):
        user = self.find_user(username)
        return user and user['password'] == password

    def update_user(self, user_id, username=None, email=None):
        update_fields = {}
        if username:
            update_fields['username'] = username
        if email:
            update_fields['email'] = email
        if update_fields:
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})

    def get_all_users(self):
        return self.collection.find()

    def get_total_users(self):
        return self.collection.count_documents({})

    def get_active_users(self):
        return self.collection.count_documents({"active": True})

    def get_inactive_users(self):
        return self.collection.count_documents({"active": False})
