from django.urls import path
from .views import home, search_papers, download_csv

urlpatterns = [
    path("", home, name="home"),
    path("search/", search_papers, name="search_papers"),
    path("download/", download_csv, name="download_csv"),
]
