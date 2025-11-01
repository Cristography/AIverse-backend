"""
Custom permission classes for Django REST Framework.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit/delete it.
    Everyone can read (GET), but only the owner can modify (PUT, PATCH, DELETE).
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.author == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows:
    - Owner to edit/delete their own content
    - Admins/staff to edit/delete any content
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions for owner or admin
        return obj.author == request.user or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission for admin-only content (tags, news, blogs, tools).
    Anyone can read, but only admins can create/edit/delete.
    """

    def has_permission(self, request, view):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for admin/staff
        return request.user and request.user.is_staff


class IsCommentOwnerOrPromptAuthor(permissions.BasePermission):
    """
    Special permission for comments:
    - Comment owner can edit/delete their own comment
    - Prompt author can delete any comment on their prompt
    - Admins can delete any comment
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # For DELETE: comment owner, prompt author, or admin
        if request.method == 'DELETE':
            return (
                obj.author == request.user or
                obj.prompt.author == request.user or
                request.user.is_staff
            )

        # For PUT/PATCH: only comment owner
        return obj.author == request.user