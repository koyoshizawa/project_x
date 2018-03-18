from django.urls import path
from . import views

app_name = 'back_test'

urlpatterns = [
    path('', views.index, name='index'),
    path('exec_back_test/', views.exec_back_test, name='exec_back_test')
]