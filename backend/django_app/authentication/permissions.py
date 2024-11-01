from rest_framework import permissions
from .models.team import TeamMembership

class IsTeamAdmin(permissions.BasePermission):
    """Custom permission to only allow team admins to perform certain actions"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
            
        try:
            membership = TeamMembership.objects.get(
                team=obj,
                user=request.user
            )
            return membership.has_permission('manage_team')
        except TeamMembership.DoesNotExist:
            return False

class IsTeamMember(permissions.BasePermission):
    """Permission to only allow team members to access"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
            
        try:
            membership = TeamMembership.objects.get(
                team=obj,
                user=request.user
            )
            
            if request.method in permissions.SAFE_METHODS:
                return membership.has_permission('view_workflows')
            return membership.has_permission('edit_workflows')
            
        except TeamMembership.DoesNotExist:
            return False

class IsAPIKeyOwner(permissions.BasePermission):
    """Permission to only allow owners of an API key to access it"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and obj.is_active