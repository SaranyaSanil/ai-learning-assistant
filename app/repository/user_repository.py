from operator import or_

from app.models.user import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def get_existing_user(self, email: str, username: str):

        def operation(db):
            return db.query(User).filter(
                or_(
                    User.email == email,
                    User.username == username
                )
            ).first()

        return self._handle_db_operation(operation)
    
    def get_by_username(self, username: str):

        def operation(db):

            return db.query(User).filter(
                User.username == username
            ).first()

        return self._handle_db_operation(operation)
    
    def get_by_id(self, user_id: int):

        def operation(db):

            return db.query(User).filter(
                User.id == user_id
            ).first()

        return self._handle_db_operation(operation)

    def create(self, user: User):

        def operation(db):
            db.add(user)
            db.flush()
            db.refresh(user)
            return user

        return self._handle_db_operation(operation, commit=True)