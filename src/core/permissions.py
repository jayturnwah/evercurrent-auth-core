from rest_framework.permissions import BasePermission, SAFE_METHODS

class HasRole(BasePermission):
    """
    Allow only users who possess ANY of the required roles.
    Use with view attributes: required_roles = ['creator', 'admin']
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False 
        required = getattr(view, 'required_roles', None)
        if not required:
            return True # no special role required
        user_roles = set(r.name for r in request.user.roles.all())
        return any(r in user_roles for r in required)
    
class IsOwnerOrAdmin(BasePermission):
    """
    Read for authenticated; write only if owner or admin role.
    """

def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
        return True
    if not request.user.is_authenticated:
        return False
    if obj.owner_id == request.user.id:
        return True
    # treat 'admin' role as elevated

    return request.user.roles.filter(name='admin').exists()