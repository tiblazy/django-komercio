from rest_framework import permissions

class SellerPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method=='POST':
            return (request.user.is_authenticated and request.user.is_seller)
        return True
    
class SellerOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, _, obj):
        if request.method=='PATCH':
            return (request.user.is_authenticated and request.user == obj.seller) 
        return True