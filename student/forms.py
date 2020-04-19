from django import forms
from .models import (
    Program, EducationHistoy, StudentFile, StudentNotes,
    EmploymentHistory
)
from .constants import EDUCATION_LEVEL


class EducationHistoryForm(forms.ModelForm):
    class Meta:
        model = EducationHistoy
        fields = (
            'major', 'university', 'end_date', 'gpa', 'education_level'
        )

class StudentFileUploadForm(forms.ModelForm):
    class Meta:
        model = StudentFile
        fields = (
            'file_name', 'file_link',
        )


class StudentNotesForm(forms.ModelForm):
    class Meta:
        model = StudentNotes
        fields = (
            'note',
        )


class StudentEmploymentForm(forms.ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = (
            'hire_date', 'position', 'hire_type', 'pay_level', 'funding_source',
            'assignment'
        )