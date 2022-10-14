from rest_framework import serializers

from genres.serializers import GenreSerializer
from genres.models import Genre
from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    premiere = serializers.DateField()
    duration = serializers.CharField(max_length=10)
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict) -> Movie:
        genres = validated_data.pop("genres")
        genres_data = [Genre.objects.get_or_create(**genre)[0] for genre in genres]

        movie = Movie.objects.create(**validated_data)
        movie.genres.set(genres_data)

        return movie

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "genres":
                genres_data = [
                    Genre.objects.get_or_create(**genre)[0] for genre in value
                ]

                instance.genres.set(genres_data)
                continue

            setattr(instance, key, value)

        instance.save()

        return instance
