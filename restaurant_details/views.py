from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from .models import Restaurant, ReviewAndRating, BookmarkAndVisited
from .serializers import RestaurantSerializer, ReviewAndRatingSerializer, BookmarkAndVisitedSerializer, UserVisitedSerializer, UserBookmarkedSerializer, CreateRestaurantSerializer

class RestaurantList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_staff:
            serializer = CreateRestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

class RestaurantDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        if request.user == restaurant.owner:
            serializer = RestaurantSerializer(restaurant, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        if request.user == restaurant.owner:
            restaurant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)



class RestaurantListByCity(APIView):
    def get(self, request, city, format=None):
        restaurants = Restaurant.objects.filter(location__iexact=city).order_by('title')
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


class ReviewRatingView(APIView):
    def get(self, request, restaurant_id, format=None):
        reviews = ReviewAndRating.objects.filter(restaurant_id=restaurant_id)
        review_serializer = ReviewAndRatingSerializer(reviews, many=True)
        return Response(review_serializer.data)

    def post(self, request, restaurant_id, format=None):
        data = request.data
        data['restaurant_id'] = restaurant_id
        serializer = ReviewAndRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, restaurant_id, review_id, format=None):
        review = ReviewAndRating.objects.get(id=review_id, restaurant_id=restaurant_id)
        serializer = ReviewAndRatingSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, restaurant_id, review_id, format=None):
        review = ReviewAndRating.objects.get(id=review_id, restaurant_id=restaurant_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkAndVisitedView(APIView):
    def get_object(self, restaurant_id, user_id):
        try:
            return BookmarkAndVisited.objects.get(restaurant=restaurant_id, user=user_id)
        except BookmarkAndVisited.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, restaurant_id, user_id):
        all_data = BookmarkAndVisited.objects.all()
        serializer = BookmarkAndVisitedSerializer(all_data, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_id, user_id):
        serializer = BookmarkAndVisitedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, restaurant_id, user_id):
        bookmark = self.get_object(restaurant_id, user_id)
        serializer = BookmarkAndVisitedSerializer(bookmark, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, restaurant_id, user_id):
    #     bookmark = self.get_object(restaurant_id, user_id)
    #     bookmark.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UserBookmarkView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkAndVisitedSerializer

    def get(self, request, user_id):
        queryset = BookmarkAndVisited.objects.filter(user=user_id, bookmarked=True)
        serializer = UserBookmarkedSerializer(queryset, many=True)
        return Response(serializer.data)


class UserVisitedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkAndVisitedSerializer

    def get(self, request, user_id):
        queryset = BookmarkAndVisited.objects.filter(user=user_id, visited=True)
        serializer = UserVisitedSerializer(queryset, many=True)
        return Response(serializer.data)
    

class SortByRatingView(APIView):
    def get(self, request, format=None):
        queryset = Restaurant.objects.annotate(avg_rating=Avg('reviewandrating__rating'))
        sort_by = self.request.query_params.get('sort_by', None)
        print(sort_by)
        if sort_by == 'high_to_low':
            queryset = queryset.order_by('-avg_rating')
        elif sort_by == 'low_to_high':
            queryset = queryset.order_by('avg_rating')
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data)