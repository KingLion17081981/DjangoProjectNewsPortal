from celery import shared_task
from .models import Post, UsersCategory, PostCategory

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from django.utils import timezone
import datetime

@shared_task
def send_massage_new_post(pk):
    category_list = []

    post = Post.objects.get(id=pk)
    categories = Post.objects.get(id=pk).category.all()

    for category in categories:
        category_list.append(category.id)

    filter_qs = UsersCategory.objects.filter(category__in=category_list)
    for value in filter_qs:
        if value.user.email:
            domain = Site.objects.get_current().domain
            abs_url = post.get_absolute_url()
            url = 'http://{domain}:8000{abs_url}'.format(domain=domain,
                                                         abs_url=abs_url)

            html_content = render_to_string('newsPortal/email/listMail.html',
                                            {'user': value.user,
                                             'post': post, 'url': url})

            msg = EmailMultiAlternatives(
                subject=f'Новая статья {post.title}',
                body='В категориях на которые вы подписаны вышла новая '
                     'статья',
                from_email='Smirnoff17081981@yandex.ru',
                to=[value.user.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

@shared_task
def send_massage_post_every_monday_8am():
    now = timezone.now()
    start_week = now - datetime.timedelta(seconds=8*60*60)
    start_previous_week = start_week - datetime.timedelta(seconds=604800)


    domain = Site.objects.get_current().domain + ':8000'
    cat_us = UsersCategory.objects.all()
    cat_us_dict = {}

    # Получаем словарь в котором ключ пользователь а значение список
    # категорий на которые он подписан
    for elem in cat_us:
        if cat_us_dict.get(elem.user) is None:
            cat_us_dict[elem.user] = [elem.category]
        else:
            cat_us_dict[elem.user].append(elem.category)

    for key in cat_us_dict.keys():
        if not key.email:
            continue

        posts = []
        value = cat_us_dict.get(key)
        post_cat = PostCategory.objects.filter(category__in=value,
                                               post__created_at__gte=start_previous_week,
                                               post__created_at__lt=start_week)

        for elem in post_cat:
            posts.append(elem.post)

        html_content = render_to_string('newsPortal/email/listMailWeek.html',
                                        {'user': key,
                                         'posts': posts, 'domain': domain})

        msg = EmailMultiAlternatives(
            subject=f'Новые статьи за неделю ',
            body='В категориях на которые вы подписаны за неделю вышли статьи',
            from_email='Smirnoff17081981@yandex.ru',
            to=[key.email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()



