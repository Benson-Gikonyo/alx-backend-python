from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Message


# Create your views here.
@login_required
def delete_user(request):
    """view to delete the currently logged in user"""

    user = request.user
    user.delete()
    return redirect("/")
