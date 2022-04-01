from django.shortcuts import redirect, render
from .models import Member, Thread
from django.contrib.auth import authenticate, login, logout



def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    users = Member.objects.exclude(username=request.user.username)
    threads = Thread.objects.by_user(user = request.user).prefetch_related('message_thread').order_by('-date')

    data = {
        'users': users,
        'threads': threads
    }
    return render(request, 'main/index.html', data)

def login_handle(request):
    err = ''
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        if "login" in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                err = 'Error: Invalid username or password'
        else:
            username = request.POST['username']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            password = request.POST['password']
            image = request.FILES.get('image')
            
            if image is None:
                image = "profile/profile.png"

            try:
                Member.objects.get(username = username)
                err = "Error: Username already exist!"
            except Member.DoesNotExist:
                addMember = Member.objects.create_user(username, email, password)
                addMember.first_name = fname
                addMember.last_name = lname
                addMember.image = image
                addMember.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    err = "Error: Something went wrong please try again!"

    data = {
        'err': err
    }

    return render(request, 'main/login.html', data)

def logout_handle(request):
    logout(request)
    return redirect('/login')