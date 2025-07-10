import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.utils import timezone
import datetime
from NewsPortal.models import UsersCategory, PostCategory
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    now = timezone.now()
    old_time = now - datetime.timedelta(seconds=604800)

    domain = Site.objects.get_current().domain + ':8000'
    cat_us = UsersCategory.objects.all()
    cat_us_dict = {}

    #Получаем словарь в котором ключ пользователь а значение список
    #категорий на которые он подписан
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
                                               post__created_at__gte=old_time,
                                               post__created_at__lt=now)

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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week ="*/0"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")