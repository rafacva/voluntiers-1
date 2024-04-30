from profiles.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from vagas.models import Vaga


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'profiles/pages/register_view.html', {
        'form': form,
        'form_action': reverse('profiles:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])
        return redirect(reverse('profiles:login'))

    return redirect('profiles:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'profiles/pages/login.html', {
        'form': form,
        'form_action': reverse('profiles:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Senha ou usuário incorretos. Tente novamente.')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('profiles:dashboard'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('profiles:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('profiles:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('profiles:login'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def dashboard(request):
    vagas = Vaga.objects.filter(
        is_published=False,
        profile=request.user
    )
    return render(
        request,
        'profiles/pages/dashboard.html',
        context={
            'vagas': vagas,
        }
    )
