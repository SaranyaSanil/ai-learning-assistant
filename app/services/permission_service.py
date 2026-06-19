
class PermissionService:

    def __init__(self, repo):
        self.repo = repo

    def has_permission(self,user_id: int,permission_name: str):
        result = self.repo.get_user_permissions(user_id)

        if not result:
            return False

        user, permissions = result

        for permission in permissions:
            if permission.name == permission_name:
                return True

        return False
