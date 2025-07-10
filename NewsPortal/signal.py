from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from .models import UsersCategory, PostCategory
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

@receiver(m2m_changed, sender=PostCategory)
def create_category(sender, instance, action, *args, **kwargs):
    if action == 'post_add':
        categories_qs = PostCategory.objects.filter(post=instance)

        categories_list = []
        for category_qs in categories_qs:
            categories_list.append(category_qs.category.id)

        users = set()
        usc_qs = UsersCategory.objects.filter(category_id__in=categories_list)
        for uc_q in usc_qs:
            users.add(uc_q.user)

        for user in users:
            if user.email:
                domain = Site.objects.get_current().domain
                abs_url = instance.get_absolute_url()
                url = 'http://{domain}:8000{abs_url}'.format(domain=domain,
                                                        abs_url=abs_url)

                html_content = render_to_string('newsPortal/email/listMail.html',
                                                {'user': user,
                                                 'post': instance, 'url': url})

                msg = EmailMultiAlternatives(
                    subject=f'Новая статья {instance.title}',
                    body='В категориях на которые вы подписаны вышла новая '
                         'статья',
                    from_email='Smirnoff17081981@yandex.ru',
                    to=[user.email])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()








