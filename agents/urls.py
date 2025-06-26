from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.agent_dashboard, name='dashboard'),
    path('process/', views.process_prompt, name='process_prompt'),
    path('api/process/', views.process_prompt_ajax, name='process_prompt_ajax'),
    
    # Post management URLs
    path('save-draft/', views.save_draft, name='save_draft'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('api/posts/<int:post_id>/status/', views.post_status_update, name='post_status_update'),
]
