from rest_framework import permissions


class AccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        if request.method=='PATCH':
            return (request.user.is_authenticated and request.user == object)
        return True