from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.database import SessionLocal
from app.exceptions.custom_exception import (
    DuplicateResourceError,
    DatabaseError
)


class BaseRepository:

    def _handle_db_operation(self, operation, commit=False):

        db = SessionLocal()

        try:
            result = operation(db)

            if commit:
                db.commit()

            return result

        except IntegrityError:
            db.rollback()
            raise DuplicateResourceError("Resource already exists")

        except SQLAlchemyError as e:
            db.rollback()
            raise DatabaseError(f"Database error: {str(e)}")

        finally:
            db.close()