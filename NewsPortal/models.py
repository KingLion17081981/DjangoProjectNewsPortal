from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

article = 'AR'
news = 'NW'

TYPE_OF_PUBLICATION = [
    (article, 'Статья'),
    (news, 'Новость')
]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0, blank=True)

    def update_rating(self):
        sum_comments_autor = 0
        sum_posts_autor = 0
        sum_comments_post_autor = 0

        f_comments = Comment.objects.filter(author=self.user)
        if f_comments.exists():
            for comment in f_comments:
                sum_comments_autor += comment.rating

        f_posts = Post.objects.filter(author=self)
        if f_posts.exists():
            for post in f_posts:
                sum_posts_autor += post.rating

                f_comments_post_autor = Comment.objects.filter(post=post)
                if f_comments_post_autor.exists():
                    for f_comment_post_autor in f_comments_post_autor:
                        sum_comments_post_autor += f_comment_post_autor.rating

        self.rating = (sum_comments_autor + sum_posts_autor * 3
                       + sum_comments_post_autor)
        self.save()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE_OF_PUBLICATION)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField(default=0, blank=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating:
            self.rating -= 1
        else:
            self.rating = 0
        self.save()

    def preview(self):
        return f'{self.content[:124]} ...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating:
            self.rating -= 1
        else:
            self.rating = 0
        self.save()



