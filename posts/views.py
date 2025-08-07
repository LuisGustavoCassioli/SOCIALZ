from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post

# VIEW DE REGISTRO
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # vai pra tela de login depois de registrar
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# VIEW DE LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

# VIEW DE LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

# VIEW DO FEED (só entra logado)
@login_required(login_url='login')
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})
