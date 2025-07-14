from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate

class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        user = self.repo.get_user_by_email(user_login.email)
        if user and user.password == user_login.password:
            return user
        else:
            raise ValueError("Invalid email or password")
        
    def register_user(self, new_user: User) -> User:
        existing_user = self.repo.get_user_by_email(new_user.email)
        if existing_user:
            raise ValueError("User already exists")
        saved_user = self.repo.save_user(new_user)
        return saved_user

    def delete_user(self, email: str) -> User:
        user = self.repo.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        deleted_user = self.repo.delete_user(user)
        return deleted_user

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        user = self.repo.get_user_by_email(user_update.email)
        if not user:
            raise ValueError("User not found")
        user.password = user_update.new_password
        updated_user = self.repo.save_user(user)
        return updated_user
        