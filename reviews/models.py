from email.policy import default
from django.db import models


class RecomendationChoices(models.TextChoices):
    MUST_WATCH = "Must Watch"
    SHOULD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    NO_OPINION = "No Opinion"


class Review(models.Model):
    stars = models.PositiveIntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(default=False, blank=True, null=True)
    recomendation = models.CharField(
        max_length=50,
        choices=RecomendationChoices.choices,
        default=RecomendationChoices.NO_OPINION,
    )

    movie_id = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user_id = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        unique_together = ["movie_id", "user_id"]
