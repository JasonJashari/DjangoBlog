from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = 'Your profile was created successfully'


@login_required
def profile(request):
    return render(request, 'users/profile.html')