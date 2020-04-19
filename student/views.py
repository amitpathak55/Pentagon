from datetime import date
from django.views.generic import (
    ListView, CreateView, UpdateView
)
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import CheckPermissionMixin
from .models import (
    Degree, Program, Student,
    EducationHistoy, StudentFile, StudentNotes, EmploymentHistory
)
from django.core.files.storage import FileSystemStorage
from .forms import (
    EducationHistoryForm, StudentFileUploadForm, StudentNotesForm,
    StudentEmploymentForm
)


class DegreeList(LoginRequiredMixin, CheckPermissionMixin, ListView):
    model = Degree
    template_name = 'student/degree/list.html'
    permission_name = 'view_degree'
    context_object_name = 'degree'


class DegreeCreate(LoginRequiredMixin, CheckPermissionMixin, CreateView):
    model = Degree
    fields = ('title',)
    template_name = 'student/degree/form.html'
    permission_name = 'add_degree'
    success_url = reverse_lazy('student:list_degree')


class DegreeUpdate(LoginRequiredMixin, CheckPermissionMixin, UpdateView):
    model = Degree
    fields = ('title',)
    slug_field = 'title'
    template_name = 'student/degree/form.html'
    permission_name = 'change_degree'
    success_url = reverse_lazy('student:list_degree')


class ProgramList(LoginRequiredMixin, CheckPermissionMixin, ListView):
    model = Program
    template_name = 'student/program/list.html'
    permission_name = 'view_program'
    context_object_name = 'programs'


class ProgramCreate(LoginRequiredMixin, CheckPermissionMixin, CreateView):
    model = Program
    fields = ('name', 'degree')
    template_name = 'student/program/form.html'
    permission_name = 'add_program'
    success_url = reverse_lazy('student:list_program')


class ProgramUpdate(LoginRequiredMixin, CheckPermissionMixin, UpdateView):
    model = Program
    fields = ('name', 'degree')
    template_name = 'student/program/form.html'
    permission_name = 'change_program'
    success_url = reverse_lazy('student:list_program')


class StudentList(LoginRequiredMixin, CheckPermissionMixin, ListView):
    model = Student
    template_name = 'student/list.html'
    permission_name = 'view_studient'
    context_object_name = 'students'
    ordering = '-student_id'
    paginate_by = 20

    def get_queryset(self):
        queryset = super(StudentList, self).get_queryset()
        filtered = False
        if self.request.GET.get('first_name'):
            filtered = True
            queryset = queryset.filter(
                first_name__icontains=self.request.GET.get('first_name')
            )
        if self.request.GET.get('last_name'):
            filtered = True
            queryset = queryset.filter(
                last_name__icontains=self.request.GET.get('last_name')
            )
        if self.request.GET.get('student_id'):
            filtered = True
            queryset = queryset.filter(
                student_id=self.request.GET.get('student_id')
            )
        if self.request.GET.get('euid'):
            filtered = True
            queryset = queryset.filter(
                euid=self.request.GET.get('euid')
            )
        return queryset if filtered else []


class StudentCreate(LoginRequiredMixin, CheckPermissionMixin, CreateView):
    model = Student
    template_name = 'student/form.html'
    permission_name = 'add_student'
    fields = (
        'first_name', 'middle_name', 'email', 'last_name', 'image','gender', 'program', 'starting_semester','student_id', 'citizenship', 'city', 
        'state', 'zip_code', 'country', 'advisor', 'greq_score', 'grev_score', 'grea_score',
        'gre_total_score', 'elp_score'
    )

    def get_success_url(self):
        if(self.request.POST.get('next') == 'Save & Continue'):
            return reverse_lazy('student:create_education_history', kwargs={'pk': self.object})
        return reverse_lazy('core:dashboard')
   


class StudentUpdate(LoginRequiredMixin, CheckPermissionMixin, UpdateView):
    model = Student
    template_name = 'student/form.html'
    permission_name = 'update_student'
    fields = (
        'first_name', 'middle_name', 'email', 'last_name', 'image', 'gender', 'program', 'starting_semester','student_id', 'citizenship', 'city', 
        'state', 'zip_code', 'country', 'advisor', 'greq_score', 'grev_score', 'grea_score',
        'gre_total_score', 'elp_score'
    )
    success_url = reverse_lazy('core:dashboard')


def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)  
    return render(
        request,
        template_name = 'student/profile.html',
        context={
            'student': student
        }
    )

