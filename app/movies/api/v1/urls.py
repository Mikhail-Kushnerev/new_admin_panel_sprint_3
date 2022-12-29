from django.urls import path

from .views import MoviesListApi, MovieDetailAPI


urlpatterns = [
    path('movies/', MoviesListApi.as_view()),
    path('movies/<uuid:pk>', MovieDetailAPI.as_view())
]
