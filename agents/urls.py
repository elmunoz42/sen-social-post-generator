from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.agent_dashboard, name='dashboard'),
    path('process/', views.process_prompt, name='process_prompt'),
    path('api/process/', views.process_prompt_ajax, name='process_prompt_ajax'),
]
