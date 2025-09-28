from django.db import models
from multiselectfield import MultiSelectField
from WebApp.models import RegistrationDB
from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)



class AnimeDB(models.Model):
    Jap_Name = models.CharField(max_length=300,null=True,blank=True)
    Eng_Name = models.CharField(max_length=300,null=True,blank=True)
    Episode = models.CharField(max_length=300,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)
    Duration = models.CharField(max_length=50,null=True,blank=True)
    Studio = models.CharField(max_length=50,null=True,blank=True)
    Producer = models.CharField(max_length=50,null=True,blank=True)
    Image = models.ImageField(upload_to="Anime_Image",null=True,blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    views = models.PositiveIntegerField(default=0)
    episode_links = models.JSONField(default=list, blank=True)
    VERSION_CHOICES = [
        ('sub', 'Subbed'),
        ('dub', 'Dubbed'),
    ]
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('ova', 'OVA'),
        ('ona', 'ONA'),
        ('tv series', 'TV Series'),
    ]
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='TV Series')
    versions = MultiSelectField(choices=VERSION_CHOICES, max_length=7, blank=True)

    def get_versions_display(self):
        return ", ".join(dict(self.VERSION_CHOICES).get(v, v) for v in self.versions)      # important


    def ratings_count(self):
        return self.ratings.count()

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 1)
        return 0


class RatingDB(models.Model):
    anime = models.ForeignKey(AnimeDB, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(RegistrationDB, related_name="ratings", on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1–5 stars

    class Meta:
        unique_together = ('anime', 'user')  # one rating per user

    def __str__(self):
        return f"{self.user.UserName} rated {self.anime.Eng_Name} - {self.value} stars"

class CommentDB(models.Model):
    anime = models.ForeignKey(AnimeDB, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(RegistrationDB, on_delete=models.CASCADE)  # use your custom table
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



