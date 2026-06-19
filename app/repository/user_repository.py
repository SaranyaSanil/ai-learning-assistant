from operator import or_
from sqlalchemy.orm import joinedload
from app.models.user import BlacklistedToken, Permission, Role, User
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

    def get_role_by_id(self, role_id: int):

        def operation(db):
            return db.query(Role).filter(
                Role.id == role_id
            ).first()

        return self._handle_db_operation(operation)
    
    def assign_role(self, user_id: int, role_id: int):

        def operation(db):

            user = db.query(User).filter(
                User.id == user_id
            ).first()

            if not user:
                return None
            user.role_id = role_id
            db.commit()
            db.refresh(user)
            return user

        return self._handle_db_operation(operation)
    
    def delete_user(self, user_id: int):

        def operation(db):

            user = db.query(User).filter(
                User.id == user_id
            ).first()

            if not user:
                return None

            db.delete(user)
            db.commit()
            return user
        
        return self._handle_db_operation(operation)
    
    def get_all_users(self):

        def operation(db):
            return db.query(User).all()

        return self._handle_db_operation(operation)
    
    def update_user(self, user):

        def operation(db):
            updated_user = db.merge(user)
            db.commit()
            db.refresh(updated_user)
            return updated_user

        return self._handle_db_operation(operation)
    
    def change_password(self,user,hashed_password: str):

        def operation(db):
            updated_password = db.merge(user)
            updated_password.password = hashed_password
            db.commit()
            db.refresh(updated_password)
            return updated_password

        return self._handle_db_operation(operation)
    
    def get_user_permissions(self, user_id: int):

        def operation(db):

            user = (
                db.query(User)
                .options(
                    joinedload(User.role)
                    .joinedload(Role.permissions)
                )
                .filter(User.id == user_id)
                .first()
            )

            if not user:
                return None

            if not user.role:
                return user, []

            return user, user.role.permissions

        return self._handle_db_operation(operation)
    
    def is_blacklisted(self, token: str):
        def operation(db):
            return (
                db.query(BlacklistedToken)
                .filter(BlacklistedToken.token == token)
                .first()
                is not None
            )
        return self._handle_db_operation(operation)
    
    def add_blacklisted_token(self, token: str, expires_at):
        def operation(db):
            blacklisted_token = BlacklistedToken(token=token, expires_at=expires_at)
            db.add(blacklisted_token)
            db.commit()
        return self._handle_db_operation(operation)

    def create(self, user: User):

        def operation(db):
            db.add(user)
            db.flush()
            db.refresh(user)
            return user

        return self._handle_db_operation(operation, commit=True) 
    
