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


@login_required
def user_messages(request):
    """get messages sent by the logged in user"""
    messages = Message.objects.filter(sender=request.user).only(
        "id", "content", "timestamp"
    )
    return render(request, "messaging/user_messages.html", {"messages": messages})
