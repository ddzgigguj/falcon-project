from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from FalconMain.telegram_utils import send_favorite_notification
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Favorite

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get list of favorite posts for current user
            favorite_posts = Favorite.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['favorite_posts'] = list(favorite_posts)
        else:
            context['favorite_posts'] = []
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Check if post is in favorites
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, 
                post=self.object
            ).exists()
        else:
            context['is_favorite'] = False
        return context

@csrf_exempt
@login_required
@require_POST
def toggle_favorite(request, post_id):
    """AJAX view for adding/removing from favorites"""
    post = get_object_or_404(Post, id=post_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        # If already in favorites, remove it
        favorite.delete()
        is_favorite = False
        message = f'"{post.title}" removed from favorites'
    else:
        # If not in favorites, add it
        is_favorite = True
        message = f'"{post.title}" added to favorites'
        send_favorite_notification(favorite)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        return JsonResponse({
            'is_favorite': is_favorite,
            'message': message
        })
    else:
        # Regular request
        messages.success(request, message)
        return redirect('post_list')

class FavoriteListView(ListView):
    model = Favorite
    template_name = 'posts/favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user).select_related('post')
        return Favorite.objects.none()