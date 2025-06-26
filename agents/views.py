from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post
import json
import logging

# Import our reflection agent
try:
    from .agents.reflect_agent import process_user_request
except ImportError:
    # Fallback for development
    def process_user_request(user_input):
        return {
            'final_post': f"Mock response for: {user_input}",
            'conversation_history': [
                {'content': f"Processing: {user_input}", 'is_feedback': False},
                {'content': "Feedback: This is a mock feedback", 'is_feedback': True},
            ]
        }

logger = logging.getLogger(__name__)

@login_required
def agent_dashboard(request):
    """Main dashboard for the reflection agent"""
    return render(request, 'agents/dashboard.html')

@login_required
def process_prompt(request):
    """Process a user prompt through the reflection agent"""
    if request.method == 'POST':
        try:
            user_prompt = request.POST.get('prompt', '').strip()
            
            if not user_prompt:
                messages.error(request, 'Please enter a prompt.')
                return redirect('agent_dashboard')
            
            # Process through the reflection agent
            logger.info(f"Processing prompt: {user_prompt[:100]}...")
            result = process_user_request(user_prompt)
            
            context = {
                'user_prompt': user_prompt,
                'final_post': result.get('final_post'),
                'conversation_history': result.get('conversation_history', []),
                'success': True
            }
            
            return render(request, 'agents/result.html', context)
            
        except Exception as e:
            logger.error(f"Error processing prompt: {str(e)}")
            messages.error(request, f'Error processing your request: {str(e)}')
            return redirect('agent_dashboard')
    
    return redirect('agent_dashboard')

@login_required
@csrf_exempt
def process_prompt_ajax(request):
    """AJAX endpoint for processing prompts (for future real-time features)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_prompt = data.get('prompt', '').strip()
            
            if not user_prompt:
                return JsonResponse({'success': False, 'error': 'Please enter a prompt.'})
            
            result = process_user_request(user_prompt)
            
            return JsonResponse({
                'success': True,
                'final_post': result.get('final_post'),
                'conversation_history': result.get('conversation_history', [])
            })
            
        except Exception as e:
            logger.error(f"AJAX Error processing prompt: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def save_draft(request):
    """Save generated content as a draft post"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            content = request.POST.get('content', '').strip()
            original_prompt = request.POST.get('original_prompt', '').strip()
            conversation_history_json = request.POST.get('conversation_history', '[]')
            
            if not title:
                messages.error(request, 'Please provide a title for your draft.')
                return redirect('agent_dashboard')
            
            if not content:
                messages.error(request, 'No content to save.')
                return redirect('agent_dashboard')
            
            # Parse conversation history
            try:
                conversation_history = json.loads(conversation_history_json)
            except json.JSONDecodeError:
                conversation_history = []
            
            # Create the post draft
            post = Post.objects.create(
                title=title,
                content=content,
                original_prompt=original_prompt,
                created_by=request.user,
                conversation_history=conversation_history,
                status='draft'
            )
            
            messages.success(request, f'Draft "{title}" saved successfully!')
            return redirect('agents:post_detail', post_id=post.id)
            
        except Exception as e:
            logger.error(f"Error saving draft: {str(e)}")
            messages.error(request, f'Error saving draft: {str(e)}')
            return redirect('agent_dashboard')
    
    return redirect('agent_dashboard')

@login_required
def post_list(request):
    """List all posts created by the user"""
    posts = Post.objects.filter(created_by=request.user)
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        posts = posts.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(original_prompt__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_posts': posts.count(),
        # Add boolean flags to avoid template == syntax issues
        'draft_selected': status_filter == 'draft',
        'published_selected': status_filter == 'published',
        'archived_selected': status_filter == 'archived',
    }
    
    return render(request, 'agents/post_list.html', context)

@login_required
def post_detail(request, post_id):
    """View details of a specific post"""
    post = get_object_or_404(Post, id=post_id, created_by=request.user)
    
    context = {
        'post': post,
    }
    
    return render(request, 'agents/post_detail.html', context)

@login_required
def post_edit(request, post_id):
    """Edit a post draft"""
    post = get_object_or_404(Post, id=post_id, created_by=request.user)
    
    if request.method == 'POST':
        try:
            post.title = request.POST.get('title', '').strip()
            post.content = request.POST.get('content', '').strip()
            post.status = request.POST.get('status', 'draft')
            
            if not post.title:
                messages.error(request, 'Please provide a title.')
                return render(request, 'agents/post_edit.html', {'post': post})
            
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('agents:post_detail', post_id=post.id)
            
        except Exception as e:
            logger.error(f"Error updating post: {str(e)}")
            messages.error(request, f'Error updating post: {str(e)}')
    
    context = {
        'post': post,
        'status_choices': Post.STATUS_CHOICES
    }
    
    return render(request, 'agents/post_edit.html', context)

@login_required
def post_delete(request, post_id):
    """Delete a post"""
    post = get_object_or_404(Post, id=post_id, created_by=request.user)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" deleted successfully!')
        return redirect('agents:post_list')
    
    context = {
        'post': post,
    }
    
    return render(request, 'agents/post_delete.html', context)

@login_required
def post_status_update(request, post_id):
    """Update post status via AJAX"""
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=post_id, created_by=request.user)
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status in ['draft', 'published', 'archived']:
                post.status = new_status
                post.save()
                return JsonResponse({'success': True, 'status': new_status})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid status'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Custom login view to redirect to dashboard after login
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/agents/'
