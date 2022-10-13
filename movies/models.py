from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10)
    premiere = models.DateField()
    classification = models.PositiveIntegerField()
    synopsis = models.TextField()

    # Relação: Um filme pode ter vários generos, e um genero pode ser de vários filmes.
    genres = models.ManyToManyField("genres.Genre", related_name="movies")
