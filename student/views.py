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
