from django.urls import path
from . import views
urlpatterns = [
    path('posts/', views.PostListApiView.as_view(), name='article-list'),
    path('posts/<int:article_id>/rate/', views.RatePostView.as_view(), name='rate-article'),
]
