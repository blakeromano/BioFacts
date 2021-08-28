from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView

# Create your views here.

# class Home(ListView):
#   model=Fact

class Login(LoginView):
  template_name='login.html'