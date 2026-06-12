from functools import wraps
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"log in to continue")
        if not request.user.is_admin:
            raise PermissionDenied("you do not have admin access")
        return view_func(request,*args,**kwargs)
    return wrapper


class Policy:
    def __init__(self,user,record):
        self.user = user
        self.record = record

    def is_admin(self):
        return self.user and self.user.is_authenticated and self.user.is_admin
    
class OrderPolicy(Policy):
    def show(self):
        if self.user and self.user.is_authenticated:
            return True
        if self.user.is_admin:
            return True
        return self.record.user == self.user

class ItemPolicy(Policy):
    def create(self):
        return self.user and self.user.is_admin
    
    def update(self):
        return self.user and self.user.is_admin

    def delete(self):
        return self.user and self.user.is_admin




    