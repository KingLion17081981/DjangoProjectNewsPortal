from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at']
    template_name = 'newsPortal/newsList.html'

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'newsPortal/newsDetail.html'