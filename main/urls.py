from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import EmployeeSignUpView, EmployerSignUpView, LoginView, index
from django.conf.urls.static import static 
from django.conf import settings


urlpatterns = [
    path("", index, name="index"),
    path("<int:pk>/", views.ApplicationView, name='application_view'),
    path("<int:application_id>/upload_cv", views.UploadCV, name='upload_cv'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", views.LogOut, name='logout'),
    path('jobs/', views.Jobs, name='jobs'),
    path("employee_signup/", EmployeeSignUpView.as_view(), name='employee_signup'),
    path("employer_signup/", EmployerSignUpView.as_view(), name='employer_signup'),
    path("employer_dashboard/application_creation/", views.ApplicationCreation, name="application_creation"),
    path("employee_dashboard/", views.EmployeeDashboard, name="employee_dashboard"),
    path("employer_dashboard/", views.EmployerDashboard, name="employer_dashboard"),
    path("employer_dashboard/response_view", views.ResponseView, name='response_view'),
    path("employer_dashboard/application_edit/<int:application_id>/", views.ApplicationEdit, name='application_edit'),
    path("employer_dashboard/<int:application_id>/", views.ApplicationDelete, name='application_delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

