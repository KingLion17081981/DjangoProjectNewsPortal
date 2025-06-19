from django.urls import path
from .views import (PostListView, PostDetailView, NewsCreateView,
                    ArticlesCreateView, NewsDeleteView, ArticlesDeleteView,
                    NewsUpdateView, ArticlesUpdateView)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreateView.as_view(),
         name='articles_create'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(),
         name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDeleteView.as_view(),
         name='articles_delete'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(),
         name='news_update'),
    path('articles/<int:pk>/update/', ArticlesUpdateView.as_view(),
         name='articles_update'),
]