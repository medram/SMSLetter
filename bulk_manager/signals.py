from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from background_task.models import Task, CompletedTask

from .models import Campaign
from .tasks import campaign_task


def on_transaction_commit(fun):
    def wrap(*args, **kwargs):
        transaction.on_commit(lambda: fun(*args, **kwargs))
    return wrap


@receiver(post_save, sender=Campaign)
@on_transaction_commit
def create_task(sender, instance, created, **kwargs):
    """create the task automatically"""

    if created:
        # do the create here
        task = campaign_task(
            {
                'campaign_id': instance.pk
            },
            schedule=instance.run_at,
            repeat=instance.repeat,
            verbose_name=instance.title,
            repeat_until=instance.repeat_until
        )
        instance.task = task
        instance.save()


@receiver(post_delete, sender=Campaign)
def delete_task(sender, instance, **kwargs):
    """Delete the task automatically"""
    try:
        if instance.task:
            instance.task.delete()
        if instance.completed_task:
            instance.completed_task.delete()
    except Exception:
        pass


@receiver(post_save, sender=Campaign)
def update_task(sender, instance, created, **kwargs):
    """Update the task automatically"""
    if not created:
        # do the update here
        if instance.task:
            # update a task
            instance.task.run_at = instance.run_at
            instance.task.verbose_name = instance.title
            instance.task.repeat = instance.repeat
            instance.task.repeat_until = instance.repeat_until
            instance.task.save()
        else:
            # Create a task
            task = campaign_task(
                {
                    'campaign_id': instance.pk
                },
                schedule=instance.run_at,
                repeat=instance.repeat,
                verbose_name=instance.title,
                repeat_until=instance.repeat_until
            )
            instance.task = task
            instance.save()


# append Task to a taskAdapter
@receiver(post_save, sender=Task)
def update_campaign_on_task_changed(sender, instance, created, **kwargs):
    if created:
        Campaign.objects.filter(
            title=instance.verbose_name).update(task=instance)

    Campaign.objects.filter(title=instance.verbose_name).update(
        run_at=instance.run_at,
        repeat=instance.repeat,
        repeat_until=instance.repeat_until
    )


# append CompletedTask to a taskAdapter
@receiver(post_save, sender=CompletedTask)
def update_campaign_on_completedtask_changed(sender, instance, created, **kwargs):
    if created:
        try:
            task_adaptor = Campaign.objects.get(
                title=instance.verbose_name)
            task_adaptor.completed_task = instance
            task_adaptor.save()
        except Campaign.DoesNotExist:
            pass
