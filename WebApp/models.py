from django.db import models



# Create your models here.
class RegistrationDB(models.Model):
    UserName = models.CharField(max_length=50,null=True,blank=True ,unique=True)
    Password = models.CharField(max_length=50, null=True, blank=True)
    C_Password = models.CharField(max_length=50,null=True,blank=True)
    E_Mail = models.CharField(max_length=50,null=True,blank=True)

    Profile_Image = models.ImageField(upload_to="Profile_Image", null=True, blank=True)

class WatchListDB(models.Model):
    CATEGORY_CHOICES = [
        ('watching', 'Watching'),
        ('completed', 'Completed'),
        ('on_hold', 'On-Hold'),
        ('dropped', 'Dropped'),
        ('plan_to_watch', 'Plan to Watch'),
    ]

    user = models.ForeignKey(RegistrationDB, on_delete=models.CASCADE)
    anime = models.ForeignKey("AdminApp.AnimeDB", on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    username = models.CharField(max_length=150,null=True,blank=True)
    anime_name = models.CharField(max_length=200,null=True,blank=True)

    class Meta:
        unique_together = ('user', 'anime')  # prevent duplicate entries



