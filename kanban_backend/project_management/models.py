from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TaskStatus(models.TextChoices):
    
    Assigned = "Assign", _("Assigned")
    InProcess = "InProcess", _("In Process")
    Done = "Done", _("Done")
    Closed = "Closed", _("Closed")
    Declined = "Declined", _("Declined")


User = get_user_model()

class Project(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="owner_projects")
    scrum_master =  models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    developers = models.ManyToManyField(User,related_name="dev_projects")
    date_start = models.DateField()
    date_end = models.DateField()




class Sprint(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=255)
    dev = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    date_start = models.DateField()
    date_end = models.DateField()





class Task(models.Model):
    
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=255)
    dev = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=25,choices=TaskStatus.choices)
    date_start = models.DateField()
    date_end = models.DateField()

    @property
    def project(self):
        return self.sprint.project