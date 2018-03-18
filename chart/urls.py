from django.urls import path
from . import views

app_name = 'chart'

urlpatterns = [
    path('', views.chart_select, name='chart_select'),
    path('get_selected_fx_data/', views.get_selected_fx_data, name='get_selected_fx_data'),
]
