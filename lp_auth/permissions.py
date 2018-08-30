from rest_framework import exceptions, permissions


def is_authenticated(user):
    return user is not None


class IsAnonymous(permissions.BasePermission):
    """
    Allows access only to anonymous users.
    """

    def has_permission(self, request, view):
        if is_authenticated(request.user):
            raise exceptions.PermissionDenied('User is already authenticated')
        return True


class IsRegular(permissions.BasePermission):
    """
    Allows access only to regular user.

    For example user must be logged-in with a token(aud=access).
    """

    def has_permission(self, request, view):
        if is_authenticated(request.user):
            return True
        raise exceptions.PermissionDenied('Not enough privilages')
