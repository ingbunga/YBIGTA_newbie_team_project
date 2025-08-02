from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.user.user_schema import User

class UserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_user_by_email(self, email: str) -> Optional[User]:
        result = self.db_session.execute(
            text("SELECT email, password, username FROM users WHERE email = :email"),
            {"email": email}
        ).first()
        
        if result:
            return User(email=result.email, password=result.password, username=result.username)
        return None

    def save_user(self, user: User) -> User: 
        # 기존 사용자가 있는지 확인
        existing = self.db_session.execute(
            text("SELECT email FROM users WHERE email = :email"),
            {"email": user.email}
        ).first()
        
        if existing:
            # 업데이트
            self.db_session.execute(
                text("UPDATE users SET password = :password, username = :username WHERE email = :email"),
                {"email": user.email, "password": user.password, "username": user.username}
            )
        else:
            # 새 사용자 생성
            self.db_session.execute(
                text("INSERT INTO users (email, password, username) VALUES (:email, :password, :username)"),
                {"email": user.email, "password": user.password, "username": user.username}
            )
        
        self.db_session.commit()
        return user

    def delete_user(self, user: User) -> User:
        self.db_session.execute(
            text("DELETE FROM users WHERE email = :email"),
            {"email": user.email}
        )
        self.db_session.commit()
        return user