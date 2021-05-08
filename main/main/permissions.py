from rest_framework.permissions import BasePermission


class IsGoodAdder(BasePermission):
    """
    Allow add a good only for users who has main.add_good permission
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.has_perm('main.add_good'))


class IsGoodEditor(BasePermission):
    """
    Allow edit a good only for users who has main.change_good permission
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.has_perm('main.change_good'))
