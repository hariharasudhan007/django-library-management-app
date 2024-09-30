from django import urls
from django.urls import path, include

from . import views
urlpatterns = [
    path("",views.BookView.as_view(), name="allbooks"),
    path("/<int:pk>",views.BookSingleView.as_view(), name="onebook"),
]