from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('login/', views.Login.as_view(), name='login'),
  path('signup/', views.signup, name='signup'),
  path('about/', views.about, name='about'),
  path('facts/<int:fact_id>/', views.fact_detail, name='fact_detail'),
  path('facts/<int:fact_id>/addphoto', views.add_photo, name='add_photo'),
]
