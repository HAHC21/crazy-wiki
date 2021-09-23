from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="single_entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/", views.editredir, name="editredir"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random, name="random"),
]
