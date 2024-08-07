from models.user import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def register(self, username, password, email):
        if self.user_model.find_user(username):
            return False
        self.user_model.create_user(username, password, email)
        return True

    def login(self, username, password):
        return self.user_model.validate_user(username, password)
