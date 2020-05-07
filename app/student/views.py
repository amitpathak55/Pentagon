from datetime import date
from django.views.generic import (
    ListView, CreateView, UpdateView
)
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import CheckPermissionMixin
from .models import (
    Degree, Program, Student, Milestones, QuantitativeReasoning,
    EducationHistoy, StudentFile, StudentNotes, EmploymentHistory,
    VerbalReasoning
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
        'first_name','degree','gpa','email', 'last_name','gender', 'program','student_id', 'citizenship', 'city', 
        'state', 'zip_code', 'country', 'greq_score', 'grev_score', 'grea_score','gre_total_score', 'elp_score', 
        'greq_score_percent', 'grev_score_percent', 'grea_score_percent', 'image',
        'immigration', 'entry_date', 'level', 'decision', 'decision_date', 'decision_reason', 'starting_semester'
    )

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            if self.request.POST.get('note'):
                note = StudentNotes.objects.create(
                    note=self.request.POST.get('note'),
                    created_by=self.request.user,
                    created_date=date.today()
                )
                user.notes.add(note)
            if self.request.POST.get('master_degree'):
                master = EducationHistoy.objects.create(
                    major=self.request.POST.get('master_degree'),
                    country=self.request.POST.get('master_degree_country'),
                    education_level='M'
                )
                user.education_history.add(master)
            if self.request.POST.get('bachelors_degree'):
                bachelor = EducationHistoy.objects.create(
                    major=self.request.POST.get('bachelors_degree'),
                    country=self.request.POST.get('bachelors_degree_country'),
                    education_level='B'
                )
                user.education_history.add(bachelor)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('core:dashboard')
   


class StudentUpdate(LoginRequiredMixin, CheckPermissionMixin, UpdateView):
    model = Student
    template_name = 'student/update_form.html'
    permission_name = 'update_student'
    fields = (
        'first_name','degree','gpa','email', 'last_name','gender', 'program','student_id', 'citizenship', 'city', 
        'state', 'zip_code', 'country', 'greq_score', 'grev_score', 'grea_score','gre_total_score', 'elp_score', 
        'greq_score_percent', 'grev_score_percent', 'grea_score_percent', 'image',
        'immigration', 'entry_date', 'level', 'decision', 'decision_date', 'decision_reason', 'starting_semester'
    )
    success_url = reverse_lazy('core:dashboard')

    def get_context_data(self, **kwargs):
        context = super(StudentUpdate, self).get_context_data(**kwargs)
        student = self.object
        context['greq_old_score'] = None
        context['greq_score'] = None
        if student.greq_score:
            context['greq_score'] = student.greq_score
            context['greq_score_percent'] = student.greq_score_percent
            if getGreqScoreAmount(student.greq_score):
                context['greq_old_score'] = getGreqScoreAmount(student.greq_score)[0]
        context['grev_old_score'] = None
        context['grev_score'] = None
        if student.greq_score:
            context['grev_score'] = student.grev_score
            context['grev_score_percent'] = student.grev_score_percent
            if getGrevScoreAmount(student.grev_score):
                context['grev_old_score'] = getGrevScoreAmount(student.grev_score)[0]
        context['grea_score'] = None
        context['grea_score_percent'] = None
        if student.grea_score:
            context['grea_score'] = student.grea_score
            context['grea_score_percent'] = student.grea_score_percent
        return context



def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)  
    return render(
        request,
        template_name = 'student/profile.html',
        context={
            'student': student
        }
    )

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)    
    with transaction.atomic():
        files_id = list(student.files.values_list('pk', flat=True))
        note_ids = list(student.notes.values_list('pk', flat=True))
        emp = list(student.employment_history.values_list('pk', flat=True))
        edu = list(student.education_history.values_list('pk', flat=True))

        student.employment_history.clear()
        for emp_id in emp:
            EmploymentHistory.objects.filter(pk=emp_id).delete()

        student.education_history.clear()
        for edu_id in edu:
            EducationHistoy.objects.filter(pk=edu_id).delete()

        student.files.clear()
        for item in files_id:
            StudentFile.objects.filter(pk=item).delete()

        student.notes.clear()
        for note in note_ids:
            StudentNotes.objects.filter(pk=note).delete()

        student.delete()
    messages.success(request, 'Student Removed.')
    return HttpResponseRedirect(reverse_lazy('core:dashboard'))


def education_history(request, pk):
    student = get_object_or_404(Student, pk=pk)
    history = student.education_history.all()
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
            if request.POST.get('next') == 'Save':
                return HttpResponseRedirect(
                    reverse_lazy('student:upload_user_file', kwargs={'pk': student.pk})
                )
            elif request.POST.get('next') == 'Save & Exit':
                return HttpResponseRedirect(
                    reverse_lazy('student:list_education_history', kwargs={'pk': student.pk})
                )
            else:
                return HttpResponseRedirect(
                    reverse_lazy('student:list_user_files', kwargs={'pk': student.pk})
                )
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
            if request.POST.get('next') == 'Save':
                return HttpResponseRedirect(reverse_lazy('student:upload_user_file', kwargs={'pk': student.pk}))
            elif request.POST.get('next') == 'Save & Exit':
                return HttpResponseRedirect(reverse_lazy('student:list_user_files', kwargs={'pk': student.pk}))
            else:
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
            if request.POST.get('next') == 'Save':
                return HttpResponseRedirect(reverse_lazy('student:add_user_note', kwargs={'pk': student.pk}))
            elif request.POST.get('next') == 'Save & Exit':
                return HttpResponseRedirect(reverse_lazy('student:list_user_notes', kwargs={'pk': student.pk}))
            else:
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
                    tbp_hours=form.cleaned_data['tbp_hours'],
                    note=form.cleaned_data['note'],
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


def report(request):
    programs = Program.objects.all()
    students = Student.objects.all()
    filtered = False
    if request.GET.get('starting_semester'):
        filtered = True
        students.filter(starting_semester=request.GET.get('starting_semester'))
    if request.GET.get('entry_date'):
        filtered = True
        students.filter(entry_date=request.GET.get('entry_date'))
    if request.GET.get('last_name'):
        filtered = True
        students.filter(last_name__icontains=request.GET.get('last_name'))
    if request.GET.get('first_name'):
        filtered = True
        students.filter(first_name__icontains=request.GET.get('first_name'))

    if request.GET.get('student_id'):
        filtered = True
        students = students.filter(
            student_id=request.GET.get('student_id')
        )
    if request.GET.get('student_id'):
        filtered = True
        students = students.filter(
            student_id=request.GET.get('student_id')
        )
    if request.GET.get('degree'):
        filtered = True
        students = students.filter(
            degree=request.GET.get('degree')
        )
    if request.GET.get('program'):
        filtered = True
        students = students.filter(
            program=request.GET.get('program')
        )
    if request.GET.get('gpa'):
        filtered = True
        students = students.filter(
            gpa__gte=request.GET.get('gpa')
        )

    if request.GET.get('greq_score'):
        filtered = True
        students = students.filter(
            greq_score__gte=request.GET.get('greq_score')
        )
    if request.GET.get('greq_score_percent'):
        filtered = True
        students = students.filter(
            greq_score_percent__gte=request.GET.get('greq_score_percent')
        )
    if request.GET.get('grev_score'):
        filtered = True
        students = students.filter(
            grev_score__gte=request.GET.get('grev_score')
        )
    if request.GET.get('grev_score_percent'):
        filtered = True
        students = students.filter(
            grev_score_percent__gte=request.GET.get('grev_score_percent')
        )
    if request.GET.get('grea_score'):
        filtered = True
        students = students.filter(
            grea_score__gte=request.GET.get('grea_score')
        )
    if request.GET.get('grea_score_percent'):
        filtered = True
        students = students.filter(
            grea_score_percent__gte=request.GET.get('grea_score_percent')
        )
    if request.GET.get('gre_total_score'):
        filtered = True
        students = students.filter(
            gre_total_score__gte=request.GET.get('gre_total_score')
        )
    if request.GET.get('elp_score'):
        filtered = True
        students = students.filter(
            elp_score__gte=request.GET.get('elp_score')
        )

    if request.GET.get('gender'):
        filtered = True
        students = students.filter(
            gender=request.GET.get('gender')
        )
    if request.GET.get('city'):
        filtered = True
        students = students.filter(
            city=request.GET.get('city')
        )
    if request.GET.get('state'):
        filtered = True
        students = students.filter(
            state=request.GET.get('state')
        )
    if request.GET.get('country'):
        filtered = True
        students = students.filter(
            country=request.GET.get('country')
        )
    if request.GET.get('citizenship'):
        filtered = True
        students = students.filter(
            citizenship=request.GET.get('citizenship')
        )
    if request.GET.get('email'):
        filtered = True
        students = students.filter(
            email=request.GET.get('email')
        )
    if request.GET.get('immigration'):
        filtered = True
        students = students.filter(
            immigration=request.GET.get('immigration')
        )

    if request.GET.get('bachelors_degree'):
        filtered = True
        students = students.filter(
            Q(education_history__major=request.GET.get('bachelors_degree')) & 
            Q(education_history__education_level='B')
        )
    if request.GET.get('bachelors_degree_country'):
        filtered = True
        students = students.filter(
            Q(education_history__country=request.GET.get('bachelors_degree_country')) & 
            Q(education_history__education_level='B')
        )

    if request.GET.get('master_degree'):
        filtered = True
        students = students.filter(
            Q(education_history__major__icontains=request.GET.get('master_degree')) & 
            Q(education_history__education_level='M')
        )
    if request.GET.get('master_degree_country'):
        filtered = True
        students = students.filter(
            Q(education_history__country__icontains=request.GET.get('master_degree_country')) & 
            Q(education_history__education_level='M')
        )
    if request.GET.get('level'):
        filtered = True
        students = students.filter(
            level=request.GET.get('level')
        )
    if request.GET.get('note'):
        filtered = True
        students = students.filter(
            notes__note__icontains=request.GET.get('note')
        )
    if request.GET.get('decision'):
        filtered = True
        students = students.filter(
            decision=request.GET.get('decision')
        )
    if request.GET.get('decision_date'):
        filtered = True
        students = students.filter(
            decision_date=request.GET.get('decision_date')
        )
    if request.GET.get('decision_reason'):
        filtered = True
        students = students.filter(
            decision_reason=request.GET.get('decision_reason')
        )
    if request.GET.get('hire_date'):
        filtered = True
        students = students.filter(
            employment_history__hire_date__icontains=request.GET.get('hire_date')
        )
    if request.GET.get('position'):
        filtered = True
        students = students.filter(
            employment_history__position__icontains=request.GET.get('position')
        )
    if request.GET.get('hire_type'):
        filtered = True
        students = students.filter(
            employment_history__hire_type__icontains=request.GET.get('hire_type')
        )
    if request.GET.get('funding_source'):
        filtered = True
        students = students.filter(
            employment_history__funding_source__icontains=request.GET.get('funding_source')
        )
    if request.GET.get('assignment'):
        filtered = True
        students = students.filter(
            employment_history__assignment__icontains=request.GET.get('assignment')
        )
    if request.GET.get('tbp_hour'):
        filtered = True
        students = students.filter(
            employment_history__tbp_hours__icontains=request.GET.get('tbp_hour')
        )
    print(students)

    return render(
        request,
        template_name = 'student/report.html',
        context={
            'students': students if filtered else [],
            'programs': programs
        }
    )


def student_milestone(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(
        request,
        template_name = 'student/milestone/list.html',
        context={
            'student': student,
        }
    )



class StudentMilestoneCreate(LoginRequiredMixin, CheckPermissionMixin, CreateView):
    model = Milestones
    template_name = 'student/milestone/form.html'
    permission_name = 'add_student'
    fields = (
    'degree_plan',
    'degree_plan_file',
    'major_professor_form',
    'major_professor_form_file', 
    'committee_appointment_form',
    'committee_appointment_form_file', 
    'qualifying_exam',
    'qualifying_exam_file', 
    'topic_proposal',
    'topic_proposal_file', 
    'thesis',
    'thesis_file', 
    )

    def form_valid(self, form):
        with transaction.atomic():
            student = Student.objects.get(pk=self.kwargs['pk'])
            with transaction.atomic():
                milestone = form.save()
                student.milestones.add(milestone)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('student:student_milestone', kwargs={'pk': self.kwargs['pk']})
   

class StudentMilestoneUpdate(LoginRequiredMixin, CheckPermissionMixin, UpdateView):
    model = Milestones
    template_name = 'student/milestone/form.html'
    permission_name = 'add_student'
    fields = (
    'degree_plan',
    'degree_plan_file',
    'major_professor_form',
    'major_professor_form_file', 
    'committee_appointment_form',
    'committee_appointment_form_file', 
    'qualifying_exam',
    'qualifying_exam_file', 
    'topic_proposal',
    'topic_proposal_file', 
    'thesis',
    'thesis_file', 
    )

    def get_success_url(self):
        student = Student.objects.get(milestones=self.kwargs['pk'])
        return reverse_lazy('student:student_milestone', kwargs={'pk': student.student_id})
   

def delete_milestone(request, pk):
    milestone = get_object_or_404(Milestones, pk=pk)
    student = Student.objects.get(milestones=milestone)
    with transaction.atomic():
        student.milestones.remove(milestone)
        milestone.delete()
    messages.success(request, 'Milestone Deleted Successfully.')
    return HttpResponseRedirect(reverse_lazy('student:student_milestone', kwargs={'pk': student.pk}))


def getGreqScoreAmount(score):
    prior_scale = QuantitativeReasoning.objects.filter(
        score_on_current_scale=score
    )
    if not prior_scale:
        return None
    old_value = None
    rank = None
    if prior_scale.count() > 1:
        largest = 0
        largest_rank = 0
        for item in prior_scale:
            if item.score_on_prior_scale > largest:
                largest = item.score_on_prior_scale
                largest_rank = item.rank
        old_value = largest
        rank = largest_rank
    else:
        old_value = prior_scale[0].score_on_prior_scale
        rank = prior_scale[0].rank
    return (old_value, rank)

def getGrevScoreAmount(score):
    prior_scale = VerbalReasoning.objects.filter(
        score_on_current_scale=score
    )
    if not prior_scale:
        return None
    old_value = None
    rank = None
    if prior_scale.count() > 1:
        largest = 0
        largest_rank = 0
        for item in prior_scale:
            if item.score_on_prior_scale > largest:
                largest = item.score_on_prior_scale
                largest_rank = item.rank
        old_value = largest
        rank = largest_rank
    else:
        old_value = prior_scale[0].score_on_prior_scale
        rank = prior_scale[0].rank
    return (old_value, rank)


def getGreqScore(request):
    amount = getGreqScoreAmount(int(request.POST.get('score')))
    if amount is None:
        return JsonResponse({'status': False, 'message': 'Score not found on the conversion chart.'})
    return JsonResponse({'status': True, 'data': amount[0], 'rank': amount[1] })

def getGrevScore(request):
    amount = getGrevScoreAmount(int(request.POST.get('score')))
    if amount is None:
        return JsonResponse({'status': False, 'message': 'Score not found on the conversion chart.'})
    return JsonResponse({'status': True, 'data': amount[0], 'rank': amount[1] })