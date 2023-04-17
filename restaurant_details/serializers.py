from rest_framework import serializers
from .models import Restaurant, ReviewAndRating, BookmarkAndVisited
from django.db.models import Avg
from .models import Cuisine, Dish

class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ReviewAndRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAndRating
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    cuisines = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    menu = serializers.StringRelatedField(many=True)
    reviews = ReviewAndRatingSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_avg_rating(self, obj):
        return obj.reviewandrating_set.aggregate(Avg('rating'))['rating__avg']


class BookmarkAndVisitedSerializer(serializers.ModelSerializer):
     class Meta:
        model = BookmarkAndVisited
        fields = '__all__'


class UserBookmarkedSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    class Meta:
        model = BookmarkAndVisited
        fields = ['restaurant']



class UserVisitedSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    class Meta:
        model = BookmarkAndVisited
        fields = ['restaurant']
