from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Profile, User

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return(request.method in SAFE_METHODS)
        return False

class IsCoordOrDirecteur(BasePermission):
    def has_permission(self, request, view):
        user  = request.user
        if user.is_authenticated:             
            return bool(user.is_superuser 
                        or user.is_COORD or user.is_DG)
        return False
    
class IsSuperUserOrDeny(BasePermission):
    def has_permission(self, request, view):
        user  = request.user
        if user.is_authenticated:             
            return bool(user.is_superuser)
        return False

class IsCoordOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user  = request.user
        if user.is_authenticated:             
            return bool(user.is_superuser or
                        request.method in SAFE_METHODS or user.is_COORD)
        return False
          

# for profiles
class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser or obj.user == user:
                return True
        return False

class UpdateOrDeleteNotAllowed(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return bool(request.method in SAFE_METHODS or user.is_superuser)
        return False
   
    
# for user details 
class IsCurrentUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            instance = User.objects.get(phone_number=request.user.phone_number)
            if instance:
                return(instance == request.user)
        return False
        
# class BlockListPermission(permissions.DjangoModelPermission):
