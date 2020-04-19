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


@login_required
def unauthorized(request):
    return render(request, 'core/unauthorized.html')

@login_required
def change_my_password(request):
    form = MyPasswordChangeForm(request.POST or None)
    if form.is_valid():
        valid_user = authenticate(
            request,
            email=request.user.email,
            password=form.cleaned_data['old_password']
        )
        if valid_user is None:
            messages.error(request, 'Old Password Doesnot Match.')
        else:
            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()
            return HttpResponseRedirect(reverse_lazy('core:dashboard'))
    return render(request, 'core/users/change_password.html', {'form': form})


@login_required
def list_groups(request):
    if not check_permission(request, 'view_group'):
        return redirect(reverse_lazy('core:unauthorized'))
    groups = Group.objects.all()
    return render(request, 'core/groups/list.html', {'groups': groups})

@login_required
def add_group(request):
    if not check_permission(request, 'add_group'):
        return redirect(reverse_lazy('core:unauthorized'))
    form = GroupModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('core:list_groups'))
    return render(request, 'core/groups/form.html', {'form': form})


@login_required
def update_group(request, pk):
    if not check_permission(request, 'change_group'):
        return redirect(reverse_lazy('core:unauthorized'))
    group = Group.objects.get(pk=pk)
    form = GroupModelForm(request.POST or None, instance=group)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('core:list_groups'))
    return render(request, 'core/groups/form.html', {'form': form})

@login_required
def list_users(request):
    if not check_permission(request, 'view_adminuser'):
        return redirect(reverse_lazy('core:unauthorized'))
    users = AdminUser.object.exclude(pk=1)
    return render(request, 'core/users/list.html', {'users': users})


@login_required
def create_user(request):
    if not check_permission(request, 'add_adminuser'):
        return HttpResponseRedirect(reverse_lazy('core:unauthorized'))
    form = UserCreateModelForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        is_admin = form.cleaned_data['is_admin']
        if is_admin is True:
            user.group_id = None
            user.save()
            messages.success(request, 'User With Super Admin Prviliges Cretaed Succesfully.')
            return HttpResponseRedirect(reverse_lazy('core:list_users'))
        else:
            if form.cleaned_data['group_id'] is None:
                messages.error(request, 'Please Select Group Or Is Admin Field')
                return render(request, 'users/form.html', {'form': form})
            else:
                user.is_admin = False
                user.save()
                messages.success(request, 'User In Group ' + str(form.cleaned_data['group_id']) + 'Cretaed Succesfully.')
                return HttpResponseRedirect(reverse_lazy('core:list_users'))
    return render(request, 'core/users/form.html', {'form': form})


@login_required
def update_user(request, id):
    if not check_permission(request, 'change_adminuser'):
        return HttpResponseRedirect(reverse_lazy('core:unauthorized'))
    admin_user = AdminUser.object.get(pk=id)
    form = UserUpdateModelForm(request.POST or None, instance=admin_user)
    if form.is_valid():
        user = form.save(commit=False)
        is_admin = form.cleaned_data['is_admin']
        if is_admin is True:
            user.group_id = None
            user.save()
            messages.success(request, 'User Updated Succesfully.')
            return HttpResponseRedirect(reverse_lazy('core:list_users'))
        else:
            if form.cleaned_data['group_id'] is None:
                messages.error(request, 'Please Select Group Or Is Admin Field')
                return render(request, 'users/form.html', {'form': form})
            else:
                user.is_admin = False
                user.save()
                messages.success(request, 'User Updated Succesfully.')
                return HttpResponseRedirect(reverse_lazy('core:list_users'))
    return render(request, 'core/users/form.html', {'form': form})


@login_required
def delete_user(request, id):
    if not check_permission(request, 'delete_adminuser'):
        return HttpResponseRedirect(reverse_lazy('core:unauthorized'))
    user = get_object_or_404(AdminUser, pk=id)
    user.delete()
    return HttpResponseRedirect(reverse_lazy('core:list_users'))


@login_required
def change_password_user(request, id):
    if not check_permission(request, 'change_adminuser'):
        return HttpResponseRedirect(reverse_lazy('core:unauthorized'))
    user = get_object_or_404(AdminUser, pk=id)
    form = UserPasswordChangeModelForm(request.POST or None)
    if form.is_valid():
        user.set_password(form.cleaned_data["password1"])
        user.save()
        messages.success(request, 'Password Chagned For The User.')
        return HttpResponseRedirect(reverse_lazy('core:list_users'))
    return render(request, 'core/users/change_password.html', {'form': form})
