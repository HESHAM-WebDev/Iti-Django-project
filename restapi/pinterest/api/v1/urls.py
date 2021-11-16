from django.urls import path
from .views import hello, movie_list, movie_create, movie_detail, movie_delete, movie_update


app_name = 'pinterest-v1'

urlpatterns = [
    path('hello-api/<str:mykey>', hello, name='hello'),
    path('api/v1/movies', movie_list, name='movie-index'),
    path('api/v1/movie/create', movie_create, name='movie-create'),
    path('api/v1/movie/<int:pk>', movie_detail, name='movie-detail'),
    path('api/v1/movie/<int:pk>/delete', movie_delete, name='movie-delete'),
    path('api/v1/movie/<int:pk>/update', movie_update, name='movie-update'),

]