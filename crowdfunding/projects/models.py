from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    country = models.CharField(max_length=80, default="Australia") # 26/09 - adding country to the database
    amount_raised = models.IntegerField(default=0) #26/09 - adding amount raised to keep a tally of pledges vs goal
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, #deletes projects if user is deleted
        related_name='owner_projects' #user.owner_projects will give you all projects for that user. It is like a reverse connection
    )

class Pledge(models.Model): 
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )

    #after creating the user models, and changing the link between user (used to be a character field) and pledges and projects it is better to delete the database sqlite and start fresh with makemigrations and migrate
    