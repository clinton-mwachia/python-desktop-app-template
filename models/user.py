from utils.database import Database
from bson.objectid import ObjectId
import bcrypt

class UserModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('users')

    def create_user(self, username, password, email=None, role=None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {"username": username, "password": hashed_password, "email": email, "active": True, "role": role}
        self.collection.insert_one(user)

    def find_user(self, username):
        return self.collection.find_one({"username": username})

    def validate_user(self, username, password):
        user = self.find_user(username)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user['password'])
        return False

    def update_user(self, user_id, username=None, email=None, role=None):
        update_fields = {}
        if username:
            update_fields['username'] = username
        if email:
            update_fields['email'] = email
        if role:
            update_fields['role'] = role
        if update_fields:
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})

    def update_password(self, user_id, old_password, new_password):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user and bcrypt.checkpw(old_password.encode('utf-8'), user['password']):
            hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": hashed_new_password}}
            )
            return result.modified_count > 0
        return False

    def get_all_users(self):
        return self.collection.find()

    def get_total_users(self):
        return self.collection.count_documents({})

    def get_active_users(self):
        return self.collection.count_documents({"active": True})

    def get_inactive_users(self):
        return self.collection.count_documents({"active": False})
