from django.urls import path
from .views import (
PostListView, 
PostDetailView, 
toggle_favorite, 
FavoriteListView
)

urlpatterns = [
path("", PostListView.as_view(), name="post_list"),
path("detail/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
path("favorite/<int:post_id>/", toggle_favorite, name="toggle_favorite"),
path("favorites/", FavoriteListView.as_view(), name="favorite_list"),
]