from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .userforms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from users.models import InMessages, Profile
from .userforms import SendMessageForm, UserRegisterForm
from django.contrib.auth import authenticate, logout as user_logout # База для входа и выхода с учетной записи
from django.contrib.auth import login
from django.contrib.auth.models import User  # База для авторизации
from .userforms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('loginPage')
    else:
        form = UserRegisterForm()
    return render(request, 'userregister.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request,'profile.html', context)

def u_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, "Неверный пароль или пользователь.")
            return render(request, 'userlogin.html')

    return render(request, 'userlogin.html')



def logout(request):
    user_logout(request)
    return render(request,'userlogout.html')

def in_messages(request):
    send_message_form = SendMessageForm()

    if request.method == 'POST':
        send_message_form = SendMessageForm(request.POST)
        if send_message_form.is_valid():
            send_message_form.save()
            return redirect('home_page')
    context = {'send_message_form': send_message_form}
    return render(request, 'send_message.html', context)

def show_messages(request):
    show_messages = InMessages.objects.all()
    context = {'show_messages': show_messages}
    return render(request, 'message.html', context)

