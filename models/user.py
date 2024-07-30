from utils.database import Database

class UserModel:
    def __init__(self):
        self.collection = Database('todo_app').get_collection('users')

    def create_user(self, username, password, profile_picture=None):
        user = {"username": username, "password": password, "profile_picture": profile_picture}
        self.collection.insert_one(user)

    def find_user(self, username):
        return self.collection.find_one({"username": username})

    def validate_user(self, username, password):
        user = self.find_user(username)
        return user and user['password'] == password

    def update_profile(self, username, email=None, profile_picture=None):
        update_fields = {}
        if email:
            update_fields['email'] = email
        if profile_picture:
            update_fields['profile_picture'] = profile_picture
        if update_fields:
            self.collection.update_one({"username": username}, {"$set": update_fields})

    def get_all_users(self):
        return self.collection.find()
