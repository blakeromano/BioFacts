from main_app.models import Fact, Photo
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'biofacts'
# Create your views here.

class Home(ListView):
  model= Fact


class Login(LoginView):
  template_name = 'login.html'

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
      return redirect('cats_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  
def about(request):
  return render(request, 'about.html')

def fact_detail(request, fact_id):
  fact = Fact.objects.get(id = fact_id)
  return render(request, 'fact/fact_detail.html', {'fact': fact})

def add_photo(request, fact_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, fact_id=fact_id)
      # Remove old photo if it exists
      fact_photo = Photo.objects.filter(fact_id=fact_id)
      if fact_photo.first():
        fact_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('fact_detail', fact_id=fact_id)