from django.shortcuts import redirect, render
from django.http import HttpResponse
from userauth.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    page = 'register'
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hey {username}! You are successfully registed.")
            new_user = authenticate(username = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('index') 

        else:
            messages.error(request, 'User not registered.')

    return render(request, 'auth.html', {'form': form, 'page': page})

def loginView(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            messages.success(request, user)
        except Exception as e:
            messages.error(request, "No such user.")

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('index')
        
        else:
            messages.error(request, "No such user, create an account. ")

    return render(request, 'auth.html')


def logoutUser(request):
    logout(request)
    return redirect('index')