from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username} ({self.email})"


class Listing(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    details = models.TextField()
    image = models.URLField(max_length=400, null=True)

    def __str__(self):
        return self.name


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="currentbids")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.item.name}: {self.amount}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comm = models.TextField()

    def __str__(self):
        return f"{self.user.username} in {self.item.name}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} added {self.item.name}"


class Category(models.Model):
    item = models.ManyToManyField(Listing, related_name="category")
    category = models.CharField(max_length=20, default="General")

    def __str__(self):
        return self.category


