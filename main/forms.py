from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User,Employer, Jobapplication, Response

class EmployeeSignUpForm(forms.ModelForm):
    email = forms.EmailField(label="Enter your Email Address")
    first_name = forms.CharField(label="Enter your first name")
    last_name = forms.CharField(label="Enter your last name")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Enter Password Again", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        
    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.is_employee = True
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        return user
    
class EmployerSignUpForm(forms.ModelForm):
    email = forms.EmailField(label="Enter your Email Address")
    first_name = forms.CharField(label="Enter your first name", widget=forms.TextInput())
    last_name = forms.CharField(label="Enter your last name", widget=forms.TextInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Enter Password Again", widget=forms.PasswordInput)
    city = forms.CharField(label="choose a City", widget=forms.TextInput())
    
    class Meta:
        model = Employer
        fields = ('first_name', 'last_name', 'email', 'city', 'password1', 'password2')
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create(email=self.cleaned_data['email'], first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'])
        user.set_password(self.cleaned_data["password1"])
        user.is_employer=  True
        user.save()

        instance = super().save(commit=False)
        instance.user = user
        instance.save()

        return instance
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
class JobApplicationForm(forms.ModelForm):
    EXPERIENCE_CHOICES = [
        ('4', 'No experience'),
        ('3', 'From 1 to 3 years'),
        ('2', 'From 3 to 6 years'),
        ('1', 'More than 6 years'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('5', 'Full - Time'),
        ('4', 'Part - Time'),
        ('3', 'Project'),
        ('2', 'Volunteering'),
        ('1', 'Internship'),
    ]
    
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('rub', 'RUB'),
    ]
    
    job_name = forms.CharField(required=True, widget=forms.TextInput())
    company_name = forms.CharField(widget=forms.TextInput())
    location = forms.CharField(widget=forms.TextInput())
    base_salary = forms.CharField(widget=forms.TextInput())
    floor_salary = forms.CharField(widget=forms.TextInput())
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES, widget=forms.RadioSelect)
    job_description = forms.CharField(widget=forms.Textarea())
    job_type = forms.ChoiceField(choices=JOB_TYPE_CHOICES, widget=forms.RadioSelect)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, widget=forms.Select)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(widget=forms.TextInput())
    
    
    class Meta:
        model = Jobapplication
        fields = ('company_name', 'job_name', 'location', 'base_salary', 'floor_salary','currency', 'experience', 'job_description', 'email', 'phone_number', 'job_type')
        
class JobApplicationEdit(forms.ModelForm):
    class Meta:
        model = Jobapplication
        fields = ('company_name', 'job_name', 'location', 'base_salary', 'floor_salary', 'experience', 'job_description', 'email', 'phone_number', 'job_type')
        
class ApplyResponseForm(forms.ModelForm):
    file = forms.FileField(label='Upload your CV')
    message = forms.CharField(widget=forms.Textarea())
    
    class Meta:
        model = Response
        fields = ('file', 'message')
        

    
