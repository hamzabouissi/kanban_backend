


from kanban_backend.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=User)
def create_user_profile(instance:User,created, **kwargs):
    if created:
        instance.add_user_type_profile()