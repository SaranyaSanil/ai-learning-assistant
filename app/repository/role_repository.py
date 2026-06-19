from app.exceptions.custom_exception import ResourceNotFoundError
from app.models.user import Permission, Role
from app.repository.base_repository import BaseRepository
from sqlalchemy.orm import joinedload

class RoleRepository(BaseRepository):

    def create_role(self, payload):

        def operation(db):
            role = Role(name=payload.name)
            db.add(role)
            db.commit()
            db.refresh(role)

            return role

        return self._handle_db_operation(operation)
    
    def get_all_roles(self, page: int, page_size: int, sort: str ):
    
        def operation(db):
            query = db.query(Role)

            # total count BEFORE pagination
            total = query.count()
            if sort.lower() == "desc":
                query = query.order_by(Role.name.desc())
            else:
                query = query.order_by(Role.name.asc())

            roles= query.offset((page - 1) * page_size).limit(page_size).all()
            return roles,total

        return self._handle_db_operation(operation)
    
    def get_role_by_id(self, role_id: int):

        def operation(db):
            return db.query(Role).filter(
                Role.id == role_id
            ).first()

        return self._handle_db_operation(operation)
    
    def delete_role(self, role_id: int):

        def operation(db):
            role = db.query(Role).filter(Role.id == role_id).first()

            if not role:
                return None

            db.delete(role)
            db.commit()
            return True

        return self._handle_db_operation(operation)
    
    def get_role_permissions(self, role_id: int):

        def operation(db):
            role = (
                db.query(Role)
                .options(joinedload(Role.permissions))
                .filter(Role.id == role_id)
                .first()
            )
            return role
        return self._handle_db_operation(operation)
    
    def assign_permissions(self, role_id: int, permission_ids: list[int]):

        def operation(db):

            role = (
                db.query(Role)
                .options(joinedload(Role.permissions))
                .filter(Role.id == role_id)
                .first()
            )

            if not role:
                return None

            permissions = db.query(Permission).filter(
                Permission.id.in_(permission_ids)
            ).all()

            # ⭐ VALIDATION (IMPORTANT)
            found_ids = {p.id for p in permissions}
            missing = set(permission_ids) - found_ids

            if missing:
                raise ResourceNotFoundError(
                    f"Permissions not found: {list(missing)}"
                )

            # Existing permissions
            existing_ids = {p.id for p in role.permissions}

            # New permissions only
            new_permissions = [
                p for p in permissions
                if p.id not in existing_ids
            ]

            role.permissions.extend(new_permissions)

            db.commit()
            db.refresh(role)

            return role, permissions, new_permissions

        return self._handle_db_operation(operation)


    def remove_permission(self, role_id: int, permission_id: int):

        def operation(db):
            role = db.query(Role).filter(Role.id == role_id).first()
            if not role:
                return None
            
            permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if not permission:
                return role,None
            
            if permission in role.permissions:
                role.permissions.remove(permission)
                db.commit()
                return role,permission
            return role, None
        return self._handle_db_operation(operation)
    
    