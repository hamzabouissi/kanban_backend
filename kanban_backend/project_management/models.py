from typing import Any, Collection, Dict, Optional, Tuple
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from kanban_backend.users.models import Developer, UserType

# Create your models here.


class TaskStatus(models.TextChoices):

    Assigned = "Assign", _("Assigned")
    InProcess = "InProcess", _("In Process")
    Done = "Done", _("Done")
    Closed = "Closed", _("Closed")
    Declined = "Declined", _("Declined")


class SprintStatus(models.TextChoices):
    Open = "Open", _("Open")
    Closed = "Closed", _("Closed")


User = get_user_model()

class Project(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="owner_projects",
    )
    title = models.CharField(max_length=25, default="", blank=False)
    description = models.TextField(max_length=255, default="", blank=False)
    scrum_master = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False
    )
    developers = models.ManyToManyField(User, related_name="dev_projects")
    date_start = models.DateField()
    date_end = models.DateField()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.date_start > self.date_end:
            raise ValidationError({"error":"date_start must be superio to date_end"})

    def had_active_sprints(self)-> bool:
        sprints = self.sprints.values_list("id")
        has_active_tasks = Task.objects.filter(
            sprint_id__in=sprints,
            status__in=[TaskStatus.Assigned, TaskStatus.InProcess, TaskStatus.Done],
        ).count()>0
        return has_active_tasks

    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> Tuple[int, Dict[str, int]]:
        if self.had_sprints():
            raise ValidationError({"error":"You still have sprints to close"})
        return super().delete(using=using, keep_parents=keep_parents)


class Sprint(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=255)
    dev = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="sprints",
    )
    date_start = models.DateField()
    date_end = models.DateField()

    @property
    def scrum_master(self) -> User:
        return self.project.scrum_master

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.date_start > self.date_end:
            raise ValidationError({"error":"date_start must be superio to date_end"})
        
        if self.date_end > self.project.date:
            raise ValidationError({"error":"date_end must be inferieur to project date_end"})

        if self.date_start < self.project.date_start:
            raise ValidationError({"error":"date_start must be superior to project date_start"})
        

    @property
    def status(self) -> str:
        if (
            self.tasks.filter(
                status__in=[TaskStatus.InProcess, TaskStatus.Assigned]
            ).count()
            >= 1
        ):
            return "has_tasks"
        return "clean"

    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> Tuple[int, Dict[str, int]]:
        if self.status == "has_tasks":
            raise ValidationError({"error":"You still have sprints to close"})
        return super().delete(using=using, keep_parents=keep_parents)


class Task(models.Model):

    title: str = models.CharField(max_length=25)
    description: str = models.TextField(max_length=255)
    dev: Developer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="my_tasks",
        limit_choices_to={"user_type": UserType.Developer},
    )
    sprint: Sprint = models.ForeignKey(
        Sprint, on_delete=models.CASCADE, blank=False, null=False, related_name="tasks"
    )
    status: str = models.CharField(max_length=25, choices=TaskStatus.choices,default=TaskStatus.Assigned)
    date_start = models.DateField()
    date_end = models.DateField()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def project(self):
        return self.sprint.project

    def clean(self) -> None:
        if self.date_start > self.date_end:
            raise ValidationError({"error":"date_start must be superio to date_end"})

        if self.date_end > self.sprint.date_end:
            raise ValidationError({"error":"date_end must be inferieur to sprint date_end"})
        
        if self.date_start < self.sprint.date_start:
            raise ValidationError({"error":"date_start must be superior to sprint date_start"})
        

    def change_dev(self, dev: Developer):
        if self.status != TaskStatus.Assigned:
            self.status = TaskStatus.Closed
            Task.objects.create(
                title = self.title + " (Reassigned)",
                description = self.description,
                dev = dev,
                sprint = self.sprint,
                status=TaskStatus.Assigned,
                date_start=self.date_start,
                date_end=self.date_end
            )
        else:
            self.title = self.title + " (Reassigned)"
            self.dev = dev
        self.save()

    
    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> Tuple[int, Dict[str, int]]:
        if self.status in [TaskStatus.Assigned, TaskStatus.InProcess, TaskStatus.Done]:
            raise ValidationError({"error":"Your task status must be closed or declined"})
        return super().delete(using=using, keep_parents=keep_parents)

    # TODO change dev if task stauts == Assign #Done
    # TODO Can't delete the project while have sprints
    # TODO logic delete
    # TODO TASK date_end don't expand date_end project #Done
    # TODO close and reassing task to another dev #dONE
