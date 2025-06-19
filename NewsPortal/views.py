from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  DeleteView, UpdateView)
from .models import Post
from .forms import PostForm
from .fiters import PostFilter

# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at']
    template_name = 'newsPortal/newsList.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'newsPortal/newsDetail.html'

class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'newsPortal/newsCreate.html'

    def form_valid(self, form):
        post_form = form.save(commit=False)
        post_form.type = "NW"
        return super().form_valid(form)

class ArticlesCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'newsPortal/articlesCreate.html'

    def form_valid(self, form):
        post_form = form.save(commit=False)
        post_form.type = "AR"
        return super().form_valid(form)

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'newsPortal/newsDelete.html'
    success_url = reverse_lazy('post_list')

class ArticlesDeleteView(DeleteView):
    model = Post
    template_name = 'newsPortal/articlesDelete.html'
    success_url = reverse_lazy('post_list')

class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'newsPortal/newsCreate.html'

class ArticlesUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'newsPortal/articlesCreate.html'



