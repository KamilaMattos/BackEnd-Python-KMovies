from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication

from .models import Movie
from .permissions import IsAdmOrReadOnly
from .serializers import MovieSerializer


class MovieView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = MovieSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def get(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    def patch(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie, req.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()

        return Response(status.HTTP_204_NO_CONTENT)
