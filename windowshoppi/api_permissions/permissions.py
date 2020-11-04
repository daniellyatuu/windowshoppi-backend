from rest_framework.permissions import BasePermission
from app.bussiness.models import Bussiness
from rest_framework.response import Response


class IsExcAdminOrAdmin(BasePermission):
    message = "you don't have permission"

    def has_permission(self, request, view):

        allowed_groups = ['exc_admin', 'admin']

        user_group = request.user.group
        if user_group is not None:
            active_user_group = user_group.name

            if active_user_group in allowed_groups:
                return True


class IsAllowedToPost(BasePermission):
    message = "you don't have permission"

    def has_permission(self, request, view):

        allowed_groups = ['vendor']

        user_group = request.user.group
        if user_group is not None:
            active_user_group = user_group.name

            if active_user_group in allowed_groups:
                return True


class IsBussinessBelongToMe(BasePermission):
    message = "it seems like this bussiness account is not yours"

    def has_permission(self, request, view):
        bussinessid = int(request.data['bussiness'])

        # get bussiness instance
        try:
            bussiness = Bussiness.objects.get(id=bussinessid)
        except:
            return Response()

        return request.user == bussiness.user
