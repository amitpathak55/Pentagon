import time
from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_unique_slug
from .constants import (
    RACE, GENDER, ACADEMIC_LEVEL, EDUCATION_LEVEL
)
import random, string
from uuid import uuid4

def student_image_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'student/{}_{}.{}'.format(filename, str(time.time()  ),ext)
    return filename

def upload_student_files(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'student/files/{}_{}.{}'.format(filename, str(time.time()),ext)
    return filename

class Degree(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Program(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'degree')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'name')
        super(Program, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name + ' - ' +self.degree.title


class Advisor(models.Model):
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'full_name')
        super(Advisor, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class EducationHistoy(models.Model):
    major = models.CharField(max_length=255, null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    gpa = models.CharField(max_length=4, null=True, blank=True)
    education_level = models.CharField(max_length=1, choices=EDUCATION_LEVEL)


class EmploymentHistory(models.Model):
    hire_date = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    hire_type = models.CharField(max_length=255)
    pay_level = models.CharField(max_length=255, blank=True, null=True)
    funding_source = models.CharField(max_length=255, blank=True, null=True)
    assignment = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    tbp_hours = models.CharField(max_length=255, blank=True, null=True)


class StudentFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_link = models.FileField(upload_to=upload_student_files) 
    created_date = models.DateField()
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)


class StudentNotes(models.Model):
    note = models.TextField()
    created_date = models.DateField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

class Milestones(models.Model):
    degree_plan = models.CharField(max_length=255, null=True, blank=True)
    degree_plan_file = models.FileField(upload_to=upload_student_files, null=True, blank=True)
    major_professor_form = models.CharField(max_length=255, null=True, blank=True)
    major_professor_form_file = models.FileField(upload_to=upload_student_files, null=True, blank=True) 
    committee_appointment_form = models.CharField(max_length=255, null=True, blank=True)
    committee_appointment_form_file = models.FileField(upload_to=upload_student_files, null=True, blank=True) 
    qualifying_exam = models.CharField(max_length=255, null=True, blank=True)
    qualifying_exam_file = models.FileField(upload_to=upload_student_files, null=True, blank=True) 
    topic_proposal = models.CharField(max_length=255, null=True, blank=True)
    topic_proposal_file = models.FileField(upload_to=upload_student_files, null=True, blank=True) 
    thesis = models.CharField(max_length=255, null=True, blank=True)
    thesis_file = models.FileField(upload_to=upload_student_files, null=True, blank=True) 


class Student(models.Model):
    student_id = models.CharField(max_length=255, primary_key = True)
    starting_semester = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    entry_date = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=250, blank=True, null=True)
    gpa = models.CharField(max_length=5, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    zip_code = models.CharField(max_length=40, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    citizenship = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
    immigration = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    elp_score = models.IntegerField(blank=True, null=True)
    greq_score = models.IntegerField(blank=True, null=True)
    grev_score = models.IntegerField(blank=True, null=True)
    grea_score = models.IntegerField(blank=True, null=True)
    greq_score_percent = models.IntegerField(blank=True, null=True)
    grev_score_percent = models.IntegerField(blank=True, null=True)
    grea_score_percent = models.IntegerField(blank=True, null=True)
    gre_total_score = models.IntegerField(blank=True, null=True)
    education_history = models.ManyToManyField(EducationHistoy)
    employment_history = models.ManyToManyField(EmploymentHistory)
    milestones = models.ManyToManyField(Milestones)
    files = models.ManyToManyField(StudentFile)
    notes = models.ManyToManyField(StudentNotes)
    level = models.CharField(max_length=255, null=True, blank=True)
    decision = models.CharField(max_length=255, null=True, blank=True)
    decision_date = models.CharField(max_length=255, null=True, blank=True)
    decision_reason = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=student_image_upload, null=True, blank=True) 

    def __str__(self):
        return self.student_id


class QuantitativeReasoning(models.Model):
    score_on_prior_scale = models.IntegerField()
    score_on_current_scale = models.IntegerField()
    rank = models.IntegerField()

class VerbalReasoning(models.Model):
    score_on_prior_scale = models.IntegerField()
    score_on_current_scale = models.IntegerField()
    rank = models.IntegerField()