from ast import Raise
from rest_framework import serializers
from .models import Review
from users.models import User
from django.core.exceptions import ValidationError


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    user_id = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "movie_id",
            "user_id",
            "recomendation",
        ]
        read_only_fields = ["movie_id"]
        extra_kwargs = {"stars": {"min_value": 1, "max_value": 10}}

    def create(self, validated_data: dict):
        user = validated_data.pop("user_id")
        movie = validated_data.pop("movie_id")

        is_duplicated = Review.objects.filter(movie_id=movie.id, user_id=user)

        if is_duplicated:
            raise ValidationError({"msg": "Review already exists!"})

        return Review.objects.create(**validated_data, user_id=user, movie_id=movie)
