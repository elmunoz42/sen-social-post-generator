from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

# Custom login view to redirect to dashboard after login
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/agents/'
