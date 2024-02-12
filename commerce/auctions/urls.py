from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:listing_id>/addtowatchlist", views.addtowatchlist, name="addtowatchlist"),
    path("listings/<int:listing_id>/removefromwatchlist", views.removefromwatchlist, name="removefromwatchlist"),
    path("listings/<int:listing_id>/close", views.close, name="close"),
    path("listings/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)