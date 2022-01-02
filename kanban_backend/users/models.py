from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    Developer = "Dev", _("Developer")
    ScrumMaster = "ScumM", _("ScrumMaster")
    ProjectOwner = "ProjectO", _("ProjectOwner")


class User(AbstractUser):
    """Default user for kanban_backend."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    user_type = models.CharField(max_length=25, choices=UserType.choices,default=UserType.Developer)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    
    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
        

    # def clean(self) -> None:
       

    def add_user_type_profile(self):
        if self.user_type == UserType.Developer:
            model = Developer
        if self.user_type == UserType.ScrumMaster:
            model = ScrumMaster
        elif self.user_type == UserType.ProjectOwner:
            model = ProjectOwner
        model.objects.create(user=self)





class ProjectOwner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="+",
        limit_choices_to={"user_type": UserType.ProjectOwner},
    )


class ScrumMaster(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="+",
        limit_choices_to={"user_type": UserType.ScrumMaster},
    )


class Developer(models.Model):
    pass
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="+",
        limit_choices_to={"user_type": UserType.Developer},
    )
