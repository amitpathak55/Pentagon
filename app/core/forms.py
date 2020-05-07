from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class AdminLoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "example@gmail.com",
        "title": "Please enter you email"
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "title": "Please enter your password",
        "placeholder": "******"
    }))


class GroupModelForm(ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Group
        fields = '__all__'


class UserCreateModelForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Password confirmation',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = get_user_model()
        fields = '__all__'
        exclude = ['password', 'is_active', 'last_login']

    field_order = [
        'email', 'first_name', 'last_name',
        'password1','password2', 'is_admin', 'group_id'
    ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreateModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateModelForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = get_user_model()
        fields = '__all__'
        exclude = ['password', 'is_active', 'last_login']

    field_order = [
        'email', 'first_name', 'last_name',
        'is_admin', 'group_id'
    ]


class UserPasswordChangeModelForm(forms.Form):
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Password confirmation',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class MyPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label='Old Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Password confirmation',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2