from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import UserRegistrationForm

class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_url = '/accounts/login/'

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
