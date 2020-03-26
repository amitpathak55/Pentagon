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
    filename = 'student/{}_{}.{}'.format(filename, str(instance.euid),ext)
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
    major = models.ForeignKey(Program, on_delete=models.PROTECT)
    university = models.CharField(max_length=255)
    end_date = models.DateField()
    gpa = models.CharField(max_length=4)
    education_level = models.CharField(max_length=1, choices=EDUCATION_LEVEL)
    research_professor = models.CharField(max_length=255, null=True, blank=True)
    milestone = models.CharField(max_length=255, null=True, blank=True)


class EmploymentHistory(models.Model):
    hire_date = models.DateField()
    position = models.CharField(max_length=255)
    hire_type = models.CharField(max_length=255)
    pay_level = models.CharField(max_length=255)
    funding_source = models.CharField(max_length=255)
    assignment = models.CharField(max_length=255)


class StudentFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_link = models.FileField(upload_to=upload_student_files) 
    created_date = models.DateField()
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)


class StudentNotes(models.Model):
    note = models.TextField()
    created_date = models.DateField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)


class Student(models.Model):
    student_id = models.CharField(max_length=255, primary_key = True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    current_academic_level = models.CharField(max_length=1, choices=ACADEMIC_LEVEL)
    image = models.ImageField(upload_to=student_image_upload, blank=True, null=True)
    euid = models.IntegerField(unique=True)
    phone_number = models.CharField(max_length=15,blank=True)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    nationality = models.CharField(max_length=20)
    race = models.CharField(max_length=2, choices=RACE)
    gender = models.CharField(max_length=1, choices=GENDER)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    year = models.IntegerField()
    semester = models.IntegerField()
    advisor = models.CharField(max_length=255)
    education_history = models.ManyToManyField(EducationHistoy)
    employment_history = models.ManyToManyField(EmploymentHistory)
    files = models.ManyToManyField(StudentFile)
    notes = models.ManyToManyField(StudentNotes)

    def __str__(self):
        return self.first_name + self.last_name


