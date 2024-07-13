class UserNotFoundException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User with ID {self.user_id} does not exist.")
