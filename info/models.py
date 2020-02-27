from django.db import models


class Student(models.Model):
    image = models.CharField(max_length=50000)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10)
    euid = models.CharField(max_length=10)
    email = models.CharField(max_length=200)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    race = models.CharField(max_length=20)
    immigration = models.CharField(max_length=50)
    address_line = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    adviser = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    degree_level = models.CharField(max_length=50)
    app_status = models.CharField(max_length=50)
    app_received_date = models.CharField(max_length=50)
    program = models.CharField(max_length=100)
    notes = models.CharField(max_length=10000)
    files = models.CharField(max_length=10000)

    def __str__(self):
        return self.first_name + '-' + self.student_id + '-' + self.degree_level


class Undergrad(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    toefl = models.CharField(max_length=10)
    sat_reading = models.CharField(max_length=10)
    sat_writing = models.CharField(max_length=10)
    sat_math = models.CharField(max_length=10)
    sat_total = models.CharField(max_length=10)
    major = models.CharField(max_length=100)
    minor = models.CharField(max_length=100)
    ba_university = models.CharField(max_length=200)
    ba_year = models.CharField(max_length=20)
    ba_country = models.CharField(max_length=50)
    ba_gpa = models.CharField(max_length=10)

    def __str__(self):
        return self.major + '-' + self.ba_country + '-' + self.ba_gpa


class Masters(models.Model):
    undergrad = models.ForeignKey(Student, on_delete=models.CASCADE)
    gre_a = models.CharField(max_length=10)
    gre_q = models.CharField(max_length=10)
    gre_v = models.CharField(max_length=10)
    gre_total = models.CharField(max_length=10)
    ms_major = models.CharField(max_length=100)
    ms_university = models.CharField(max_length=200)
    ms_year = models.CharField(max_length=10)
    ms_country = models.CharField(max_length=50)
    ms_gpa = models.CharField(max_length=10)

    def __str__(self):
        return self.ms_major + '-' + self.ms_country


class Phd(models.Model):
    masters = models.ForeignKey(Student, on_delete=models.CASCADE)
    phd_major = models.CharField(max_length=100)
    research_professor = models.CharField(max_length=100)
    milestone = models.CharField(max_length=10000)
    evaluation = models.CharField(max_length=10000)

    def __str__(self):
        return self.phd_major + '-' + self.research_professor


class Employment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    hire_type = models.CharField(max_length=100)
    pay_level = models.CharField(max_length=100)
    funding_source = models.CharField(max_length=200)
    assignment = models.CharField(max_length=1000)
    employment_history = models.CharField(max_length=2500)

    def __str__(self):
        return self.position + '-' + self.hire_type