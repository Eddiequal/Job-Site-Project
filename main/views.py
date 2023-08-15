from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.urls import reverse
from .forms import EmployeeSignUpForm, EmployerSignUpForm, LoginForm, JobApplicationForm, ApplyResponseForm
from .models import User, Jobapplication, Response

# Create your views here.
def index(request):
    data_job_details = Jobapplication.objects.all()
    
    home_paginator = Paginator(data_job_details, 4)
    
  
    page = request.GET.get('page')
    applications = home_paginator.get_page(page)
    
    return render(request, "index.html", {'applications': applications})


class EmployeeSignUpView(CreateView):
    model = User
    template_name = "employee_signup.html"
    form_class = EmployeeSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
    
    
class EmployerSignUpView(CreateView):
    model = User
    template_name = "employer_signup.html"
    form_class = EmployerSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        user.save()
        
        return redirect('index')
    
    
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_employee:
                return reverse('index')
            elif user.is_employer:
                return reverse('index')
        else:
            return reverse('login')
        
        
def LogOut(request):
    auth.logout(request)  # logout is predefined
    return redirect('/')


def EmployeeDashboard(request):
    current_user = request.user.employee
    
    responses = Response.objects.filter(employee=current_user)
    
    return render(request, "employee_dashboard.html", {"responses": responses})

    
def EmployerDashboard(request):
    current_user = request.user.employer

    data_job_details = Jobapplication.objects.filter(employer=current_user)

    return render(request, "employer_dashboard.html", {'data_job_details': data_job_details})


def ApplicationCreation(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.employer = request.user.employer
            application.save()
            return redirect('index')
    else:
        form = JobApplicationForm()
    return render(request, "application_creation.html", {'form': form})


def ApplicationView(request, pk):
    application = get_object_or_404(Jobapplication, pk=pk)
    
    return render(request, "application_view.html", {'application': application})


def ResponseView(request):
    current_user = request.user.employer

    data_job_details = Jobapplication.objects.filter(employer=current_user)

    return render(request, "response_view.html", {'data_job_details': data_job_details})


def ApplicationEdit(request, application_id):
    application = get_object_or_404(Jobapplication, id=application_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')  
    else:
        form = JobApplicationForm(instance=application)
    
    return render(request, "application_edit.html", {'form': form, 'application': application})


def Jobs(request):
    data_job_details = Jobapplication.objects.all()
    
    jobs_paginator = Paginator(data_job_details, 4)
    

    page = request.GET.get('page')
    applications = jobs_paginator.get_page(page)
    
    return render(request, "jobs.html", {'applications': applications})


def UploadCV(request, application_id):
    application = Jobapplication.objects.get(pk=application_id)
    if request.method == 'POST':
        form = ApplyResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.employee = request.user.employee
            response.application = application
            response.save()
            return redirect('index')
    else:
        form = ApplyResponseForm()
        
    return render(request, "upload_cv.html", {'form': form})


def ApplicationDelete(request, application_id):
    application = get_object_or_404(Jobapplication, pk=application_id).delete()
    return redirect('employer_dashboard')


    
    
    
    


    
            
            

    
