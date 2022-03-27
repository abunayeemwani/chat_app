from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Member, Thread


@login_required
def index(request):
    users = Member.objects.all()
    threads = Thread.objects.by_user(user = request.user).prefetch_related('message_thread').order_by('date')

    data = {
        'users': users,
        'threads': threads
    }
    return render(request, 'main/index.html', data)