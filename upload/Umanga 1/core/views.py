from django.contrib.auth import (
    authenticate, login as start_session, logout as stop_session
)
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from .utils import *




def login(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('core:dashboard'))

    login_form = AdminLoginForm(request.POST or None)
    errors = {}
    if login_form.is_valid():
        user = authenticate(
            request,
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is None:
            errors['authentication'] = 'Invalid Credentials. Please Try Again With Valid Credentials.'
        else:
            start_session(request, user)
            redirect_link = request.GET.get('next')
            if redirect_link is None:
                return HttpResponseRedirect(reverse_lazy('core:dashboard'))
            return HttpResponseRedirect(redirect_link)
    else:
        login_form_errors = login_form.errors.as_data()
        for key, value in login_form_errors.items():
            errors[key] = value[0].message

    context = {
        'form': login_form,
        'errors': errors
    }

    return render(request, 'core/auth/login.html', context)

def logout(request):
    redirect_link = request.GET.get('next')
    if redirect_link is None:
        redirect_link = reverse_lazy('core:login')
    stop_session(request)
    return redirect(redirect_link)


@login_required
def dashboard(request):
    return render(
        request, 'core/auth/dashboard.html', {}
    )
