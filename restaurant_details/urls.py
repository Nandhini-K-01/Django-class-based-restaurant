from django.urls import path
from . import views



urlpatterns = [
    path('restaurants/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('restaurants/city/<str:city>/', views.RestaurantListByCity.as_view(), name='sort_by_city'),
    path('restaurants/<int:restaurant_id>/reviews/', views.ReviewRatingView.as_view(), name='review_rating'),
    path('restaurants/<int:restaurant_id>/reviews/<int:review_id>/', views.ReviewRatingView.as_view(), name='review_rating_id'),
    path('restaurants/<int:restaurant_id>/users/<int:user_id>/bookmark_visited/', views.BookmarkAndVisitedView.as_view(), name='bookmark-visited'),
    path('users/<int:user_id>/bookmarked/', views.UserBookmarkView.as_view(), name='user-bookmarks'),
    path('users/<int:user_id>/visited/', views.UserVisitedView.as_view(), name='user_visited_view'),
    path('restaurants/sort_by_rating/', views.SortByRatingView.as_view(), name='sort_by_rating')
]

# urlpatterns = [
#     path('allrestaurants/', views.RestaurantList, name='restaurants'),
#     path('allrestaurants/<int:id>', views.RestaurantDetail, name='restaurant_detail'),
#     path('restaurants/sort/<str:order>/', views.SortRestaurantsByRating, name='sort_by_rating'),
#     path('restaurants/city/<str:city>/', views.RestaurantListByCity, name='sort_by_city'),
#     path('restaurants/rating/<int:restaurant_id>/get/<int:user_id>', views.Review_Rating, name='rating_all'),
#     path('restaurants/rating/<int:restaurant_id>/update/<int:user_id>', views.Review_Rating, name='rating_update'),
#     path('restaurants/rating/<int:restaurant_id>/delete/<int:user_id>', views.Review_Rating, name='rating_delete'),
#     path('restaurants/<int:restaurant_id>/bookmark/<int:user_id>', views.bookmark, name='bookmark'),
#     path('restaurants/bookmarked/<int:user_id>', views.user_bookmarked, name='user_bookmarked'),
#     path('restaurants/visited/<int:user_id>', views.user_visited, name='user_visited'),
# ]