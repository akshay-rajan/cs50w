from django.urls import path


from . import views

urlpatterns = [
    path("random/", views.random, name="random"),
    path("edit/", views.edit, name="edit"),
    path("wiki/<str:title>", views.getpage, name="title"),
    path("newpage/", views.newpage, name="newpage"),
    path("search/", views.search, name="search"),
    path("", views.index, name="index")
]
