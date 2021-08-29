from main_app.models import Fact, Photo
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from datetime import date
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'biofacts'
# Create your views here.

class Home(ListView):
  model= Fact


class Login(LoginView):
  template_name = 'login.html'
  redirect_field_name='home'
  redirect_authenticated_user=True

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  
def about(request):
  return render(request, 'about.html')

def fact_detail(request, pk):
  fact = Fact.objects.get(id = pk)
  return render(request, 'fact/fact_detail.html', {'fact': fact})

@login_required
def add_photo(request, pk):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      fact = Fact.objects.get(id = pk)
      photo = Photo(url=url, fact=fact)
      fact_photo = Photo.objects.filter(fact=pk)
      if fact_photo.first():
        fact_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('fact_detail', pk=pk)

class FactCreate(LoginRequiredMixin, CreateView):
  model = Fact
  fields=['title', 'description']

  def form_valid(self, form):
    form.instance.author = self.request.user
    form.instance.date = date.today()
    return super().form_valid(form)

class FactUpdate(LoginRequiredMixin, UpdateView):
  model = Fact
  fields = ['title', 'description']

class FactDelete(LoginRequiredMixin, DeleteView):
  model = Fact
  success_url = '/'