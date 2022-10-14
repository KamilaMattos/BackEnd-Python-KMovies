import stat
from django.shortcuts import get_object_or_404
from rest_framework.views import Request, Response, APIView, status
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from movies.models import Movie
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsAdmOrCritic, IsAdmOrOwner


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmOrCritic]

    def get(self, req: Request, movie_id: int) -> Response:
        reviews = Review.objects.filter(movie_id=movie_id)
        paginate = self.paginate_queryset(reviews, req, view=self)

        serializer = ReviewSerializer(paginate, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = ReviewSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save(movie_id=movie, user_id=req.user)
        except ValidationError as error:
            return Response(error.args[0], status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status.HTTP_201_CREATED)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmOrOwner]

    def get(self, req: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)
        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(self, req: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)
        self.check_object_permissions(req, review)

        review.delete()

        return Response(status.HTTP_204_NO_CONTENT)
