from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('login/', views.Login.as_view(), name='login'),
  path('signup/', views.signup, name='signup'),
  path('about/', views.about, name='about'),
  path('facts/<int:pk>/', views.fact_detail, name='fact_detail'),
  path('facts/<int:pk>/update', views.FactUpdate.as_view(), name='fact_update'),
  path('facts/<int:pk>/delete', views.FactDelete.as_view(), name='fact_delete'),
  path('facts/create', views.FactCreate.as_view(), name='fact_create'),
  path('facts/<int:pk>/addphoto', views.add_photo, name='add_photo'),
]
