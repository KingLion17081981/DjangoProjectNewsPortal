from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  DeleteView, UpdateView)
from django.shortcuts import render, redirect
from .models import Post, Category, UsersCategory
from .forms import PostForm, CategoryForm
from .fiters import PostFilter
from django.contrib.auth.mixins import PermissionRequiredMixin

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

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)

    model = Post
    form_class = PostForm
    template_name = 'newsPortal/newsCreate.html'

    def form_valid(self, form):
        post_form = form.save(commit=False)
        post_form.type = "NW"
        return super().form_valid(form)

class ArticlesCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)

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

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)

    model = Post
    form_class = PostForm
    template_name = 'newsPortal/newsCreate.html'

class ArticlesUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)

    model = Post
    form_class = PostForm
    template_name = 'newsPortal/articlesCreate.html'

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'newsPortal/category/categoryList.html'
                  , context)

def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    context = {'category': category}
    return render(request, 'newsPortal/category/categoryDetail.html'
                  , context)

def subscribe_to_category(request, pk):
    signed = False
    category = None
    user = None
    is_save = False

    if request.user.is_authenticated:
        category = Category.objects.get(pk=pk)
        user = request.user

        if not UsersCategory.objects.filter(category=category, user=user).exists():
            UsersCategory.objects.create(user=user, category=category)
            signed = True
        else:
            is_save = True

    context = {'category': category, 'signed': signed, 'user': user, 'is_save': is_save}
    return render(request, 'newsPortal/category/categorySubscribe.html'
                  , context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('NewsPortal:category_list')

    elif request.method == 'GET':
        form = CategoryForm()
        context = {'form': form}
        return render(request, 'newsPortal/category/categoryCreate.html'
                      , context=context)










