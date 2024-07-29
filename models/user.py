from utils.database import Database

class UserModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('users')

    def create_user(self, username, password):
        user = {"username": username, "password": password}
        self.collection.insert_one(user)

    def find_user(self, username):
        return self.collection.find_one({"username": username})

    def validate_user(self, username, password):
        user = self.find_user(username)
        return user and user['password'] == password
