from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .models import Student, Undergrad, Masters, Phd, Employment
from .forms import UserForm


class IndexView(generic.ListView):
    template_name = 'info/index.html'

    def get_queryset(self):
        return Student.objects.all()


class DetailView(generic.DetailView):
    model = Student
    template_name = 'info/detail.html'


class UserFormView(View):
    form_class = UserForm
    template_name = 'info/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                    if user.is_active:
                        login(request, user)
                        return redirect('music:index')     #landing page

        return render(request, self.template_name, {'form': form})