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
            'major', 'university', 'end_date', 'gpa', 'education_level',
            'research_professor', 'milestone'
        )

    def clean(self):
        form_data = self.cleaned_data
        if form_data['education_level'] == 'P':
            if not form_data['research_professor']:
                self._errors['research_professor'] = 'This field is required if education level is PHD'
            if not form_data['milestone']:
                self._errors['milestone'] = 'This field is required if education level is PHD'
        return form_data


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