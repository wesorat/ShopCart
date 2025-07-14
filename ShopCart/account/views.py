from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email

from .forms import UserCreateForm, LoginForm, UserUpdateForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            user = User.objects.create_user(
                email=user_email, username=user_username, password=user_password
            )

            user.is_active = False

            send_email(user)

            return redirect('account:email-verification')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def email_verification(request):
    return render(request, 'account/email/email-verification.html')


def login_user(request):

    if request.user.is_authenticated:
        return redirect('shop:products')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        return redirect('account:login-user')

    context = {
        'form': LoginForm()
    }
    return render(request, 'account/login/login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('shop:products')


@login_required(login_url='account:login-user')
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login-user')
def profile_user(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:dashboard')

    context = {
        'form': UserUpdateForm(instance=request.user)
    }
    return render(request, 'account/dashboard/profile_manager.html', context=context)


@login_required(login_url='account:login-user')
def delete_user(request):

    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect('shop:products')

    return render(request, 'account/dashboard/account_delete.html')




