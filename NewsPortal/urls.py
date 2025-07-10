from django.urls import path
from .views import (PostListView, PostDetailView, NewsCreateView,
                    ArticlesCreateView, NewsDeleteView, ArticlesDeleteView,
                    NewsUpdateView, ArticlesUpdateView, category_list,
                    category_detail, subscribe_to_category, category_create)

app_name = 'NewsPortal'

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
    path('categories/', category_list, name='category_list'),
    path('categories/<int:pk>/', category_detail, name='category_detail'),
    path('categories/subscribe/<int:pk>/', subscribe_to_category,
         name='category_subscribe'),
    path('categories/create/', category_create, name='category_create'),
]