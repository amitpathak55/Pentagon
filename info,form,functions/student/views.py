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

    def get_queryset(self):
        queryset = super(StudentList, self).get_queryset()
        if self.request.GET.get('full_name'):
            queryset = queryset.filter(
                Q(first_name__icontains=self.request.GET.get('full_name')) |
                Q(middle_name__icontains=self.request.GET.get('full_name')) |
                Q(last_name__icontains=self.request.GET.get('full_name')) 
            )
        if self.request.GET.get('student_id'):
            queryset = queryset.filter(
                student_id=self.request.GET.get('student_id')
            )
        if self.request.GET.get('euid'):
            queryset = queryset.filter(
                euid=self.request.GET.get('euid')
            )
        if self.request.GET.get('phone_number'):
            queryset = queryset.filter(
                phone_number__icontains=self.request.GET.get('phone_number')
            )
        return queryset


class StudentCreate(LoginRequiredMixin, CheckPermissionMixin, CreateView):
    model = Student
    template_name = 'student/form.html'
    permission_name = 'add_student'
    fields = (
        'first_name', 'middle_name', 'last_name', 'euid', 'image', 'phone_number', 'address_line',
        'race', 'gender', 'program', 'year', 'semester','student_id', 'nationality', 'city', 
        'state', 'zip_code', 'country','current_academic_level', 'advisor'
    )
    success_url = reverse_lazy('student:list_student')


class StudentUpdate(LoginRequiredMixin, CheckPermissionMixin, UpdateView):
    model = Student
    template_name = 'student/form.html'
    permission_name = 'update_student'
    fields = (
        'first_name', 'middle_name', 'last_name', 'euid', 'image', 'phone_number', 'address_line',
        'race', 'gender', 'program', 'year', 'semester','student_id', 'nationality', 'city', 
        'state', 'zip_code', 'country','current_academic_level', 'advisor'
    )
    success_url = reverse_lazy('student:list_student')


def education_history(request, pk):
    student = get_object_or_404(Student, pk=pk)
    history = student.education_history.all()
    print(history)
    return render(
        request,
        template_name = 'student/education/list.html',
        context={
            'student': student, 'history': history
        }
    )


def create_education_history(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = EducationHistoryForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                education_history = form.save()
                student.education_history.add(education_history)
            messages.success(request, 'New Education History Added.')
            return HttpResponseRedirect(reverse_lazy('student:list_education_history', kwargs={'pk': student.pk}))
    else:
        form = EducationHistoryForm()
    return render(
        request,
        template_name = 'student/education/form.html',
        context={
            'student': student, 'form': form
        }
    )


def update_education_history(request, pk):
    history = get_object_or_404(EducationHistoy, pk=pk)
    student = Student.objects.get(education_history=history)
    form = EducationHistoryForm(instance=history)
    if request.method == 'POST':
        form = EducationHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education History Updated.')
            return HttpResponseRedirect(reverse_lazy('student:list_education_history', kwargs={'pk': student.pk}))
    return render(
        request,
        template_name = 'student/education/form.html',
        context={
            'student': student, 'form': form
        }
    )


def delete_education_history(request, pk):
    history = get_object_or_404(EducationHistoy, pk=pk)
    student = Student.objects.get(education_history=history)
    with transaction.atomic():
        student.education_history.remove(history)
        history.delete()
    messages.success(request, 'Education History Removed.')
    return HttpResponseRedirect(reverse_lazy('student:list_education_history', kwargs={'pk': student.pk}))
    return render(
        request,
        template_name = 'student/education/form.html',
        context={
            'student': student, 'form': form
        }
    )


def list_user_files(request, pk):
    student = get_object_or_404(Student, pk=pk)
    files = student.files.all()
    return render(
        request,
        template_name = 'student/files/list.html',
        context={
            'student': student, 'files': files
        }
    )


def upload_file(upload_file):
    fs = FileSystemStorage()
    filename = fs.save(upload_file.name, upload_file)
    return fs.url(filename)
        

def upload_user_file(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                file_data = StudentFile.objects.create(
                    file_name=form.cleaned_data['file_name'],
                    file_link=upload_file(request.FILES['file_link']),
                    created_date=date.today(),
                    uploaded_by=request.user
                )
                student.files.add(file_data)
        messages.success(request, 'File Uploaded Successfully.')
        return HttpResponseRedirect(reverse_lazy('student:list_user_files', kwargs={'pk': student.pk}))
    else:
        form = StudentFileUploadForm()
    return render(
        request,
        template_name = 'student/files/form.html',
        context={
            'student': student, 'form': form
        }
    )


def delete_user_file(request, pk):
    user_file = get_object_or_404(StudentFile, pk=pk)
    student = Student.objects.get(files=user_file)
    file_name = user_file.file_link.name.split('/')[2]
    with transaction.atomic():
        student.files.remove(user_file)
        user_file.delete()
    fs = FileSystemStorage()
    fs.delete(file_name)
    messages.success(request, 'File Deleted Successfully.')
    return HttpResponseRedirect(reverse_lazy('student:list_user_files', kwargs={'pk': student.pk}))


def list_user_notes(request, pk):
    student = get_object_or_404(Student, pk=pk)
    notes = student.notes.all()
    return render(
        request,
        template_name = 'student/notes/list.html',
        context={
            'student': student, 'notes': notes
        }
    )


def add_user_note(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentNotesForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                note_data = StudentNotes.objects.create(
                    note=form.cleaned_data['note'],
                    created_date=date.today(),
                    created_by=request.user
                )
                student.notes.add(note_data)
        messages.success(request, 'Note Added Successfully.')
        return HttpResponseRedirect(reverse_lazy('student:list_user_notes', kwargs={'pk': student.pk}))
    else:
        form = StudentNotesForm()
    return render(
        request,
        template_name = 'student/notes/form.html',
        context={
            'student': student, 'form': form
        }
    )


def update_user_note(request, pk):
    note = get_object_or_404(StudentNotes, pk=pk)
    student = Student.objects.get(notes=note)
    if request.method == 'POST':
        form = StudentNotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
        messages.success(request, 'Note Updated Successfully.')
        return HttpResponseRedirect(reverse_lazy('student:list_user_notes', kwargs={'pk': student.pk}))
    else:
        form = StudentNotesForm(instance=note)
    return render(
        request,
        template_name = 'student/notes/form.html',
        context={
            'student': student, 'form': form
        }
    )


def delete_user_note(request, pk):
    note = get_object_or_404(StudentNotes, pk=pk)
    student = Student.objects.get(notes=note)
    with transaction.atomic():
        student.notes.remove(note)
        note.delete()
    messages.success(request, 'Note Deleted Successfully.')
    return HttpResponseRedirect(reverse_lazy('student:list_user_notes', kwargs={'pk': student.pk}))


def list_user_employment_history(request, pk):
    student = get_object_or_404(Student, pk=pk)
    employments = student.employment_history.all()
    return render(
        request,
        template_name = 'student/employment/list.html',
        context={
            'student': student, 'employments': employments
        }
    )


def add_employment_history(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentEmploymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                emp_history = EmploymentHistory.objects.create(
                    hire_date=form.cleaned_data['hire_date'],
                    position=form.cleaned_data['position'],
                    hire_type=form.cleaned_data['hire_type'],
                    pay_level=form.cleaned_data['pay_level'],
                    funding_source=form.cleaned_data['funding_source'],
                    assignment=form.cleaned_data['assignment'],
                )
                student.employment_history.add(emp_history)
        messages.success(request, 'Employment History Added Successfully.')
        return HttpResponseRedirect(reverse_lazy('student:list_user_employment_history', kwargs={'pk': student.pk}))
    else:
        form = StudentEmploymentForm()
    return render(
        request,
        template_name = 'student/employment/form.html',
        context={
            'student': student, 'form': form
        }
    )


def update_employment_history(request, pk):
    emp_history = get_object_or_404(EmploymentHistory, pk=pk)
    student = Student.objects.get(employment_history=emp_history)
    if request.method == 'POST':
        form = StudentEmploymentForm(request.POST, instance=emp_history)
        if form.is_valid():
            with transaction.atomic():
                form.save()
        messages.success(request, 'Employment History Updated Successfully.')
        return HttpResponseRedirect(reverse_lazy('student:list_user_employment_history', kwargs={'pk': student.pk}))
    else:
        form = StudentEmploymentForm(instance=emp_history)
    return render(
        request,
        template_name = 'student/employment/form.html',
        context={
            'student': student, 'form': form
        }
    )


def delete_employment_history(request, pk):
    emp_history = get_object_or_404(EmploymentHistory, pk=pk)
    student = Student.objects.get(employment_history=emp_history)
    with transaction.atomic():
        student.employment_history.remove(emp_history)
        emp_history.delete()
    messages.success(request, 'Employment History Deleted Successfully.')
    return HttpResponseRedirect(reverse_lazy('student:list_user_employment_history', kwargs={'pk': student.pk}))