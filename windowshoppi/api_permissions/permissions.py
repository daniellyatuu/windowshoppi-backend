from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from app.account.models import Account
from app.user.models import Contact

from app.bussiness.models import Bussiness


class IsExcAdminOrAdmin(BasePermission):
    message = "you don't have permission"

    def has_permission(self, request, view):

        allowed_groups = ['exc_admin', 'admin']

        user_group = request.user.group
        if user_group is not None:
            active_user_group = user_group.name

            if active_user_group in allowed_groups:
                return True


class IsAllowedToPost(BasePermission):  # will be removed
    message = "you don't have permission"

    def has_permission(self, request, view):

        allowed_groups = ['vendor']

        user_group = request.user.group
        if user_group is not None:
            active_user_group = user_group.name

            if active_user_group in allowed_groups:
                return True


class IsBussinessBelongToMe(BasePermission):  # will be removed
    message = "it seems like this bussiness account is not yours"

    def has_permission(self, request, view):
        bussinessid = int(request.data['bussiness'])

        # get bussiness instance
        try:
            bussiness = Bussiness.objects.get(id=bussinessid)
        except:
            return Response()

        return request.user == bussiness.user


class IsWindowshopperOrVendorAccount(BasePermission):
    message = "windowshopper_or_vendor_account_required"

    def has_permission(self, request, view):

        allowed_groups = ['windowshopper', 'vendor']

        user = request.user

        # get user accounts
        accounts = Account.objects.filter(user_id=user.id)

        user_groups = []
        for account in accounts:
            user_groups.append(account.group.name)

        result = any(group in user_groups for group in allowed_groups)

        if result:
            return True


class IsContactBelongToMe(BasePermission):
    message = "it seems like this contact is not yours"

    def has_permission(self, request, view):

        try:
            contact = Contact.objects.get(id=view.kwargs['contact_id'])
        except:
            return Response()

        return request.user == contact.user


class IsAccountBelongToMe(BasePermission):
    message = "it seems like this account is not yours"

    def has_permission(self, request, view):

        if 'account_id' in view.kwargs:
            pk = view.kwargs['account_id']
        else:
            pk = int(request.data['account'])

        try:
            account = Account.objects.get(id=pk)
        except:
            return Response()

        return request.user == account.user
