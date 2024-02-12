from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist, Category

from auctions.forms import ListingForm, BidForm, CommentForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    """ Create a new listing """
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data["name"]
            description = form.cleaned_data["details"]
            startingbid = form.cleaned_data["price"]
            # Default Category and Default Image
            category = form.cleaned_data["category"]
            if not category:
                category = "General"
            image = form.cleaned_data["image"]
            if not image:
                image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPSsfpUD2GGmdda2rnmdC1xt7TofAHXB1J5w&usqp=CAU"

            newListing = Listing(user=user, name=title, price=startingbid, details=description, image=image)
            newListing.save()
            newCategory, created = Category.objects.get_or_create(category=category)

            newCategory.item.add(newListing)
            newCategory.save()


    return render(request, "auctions/newlisting.html", {
        "form": ListingForm()
    })


@login_required
def listing(request, listing_id):
    """ Show the listing page. Enable user to place a bid """

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["amount"]
            thislisting = Listing.objects.get(pk=listing_id)
            currentbids = Bid.objects.filter(item=thislisting)
            startingbid = thislisting.price

            # Check if the bid is valid
            if bid <= startingbid:
                return render(request, "auctions/error.html", {
                            "message": "Your Bid is below the starting bid!"
                        })
            for bids in currentbids:
                if bids.amount >= bid:
                    return render(request, "auctions/error.html", {
                        "message": "Someone already bid higher!"
                    })

            # Place the bid
            user = request.user
            bidding = Bid(item=thislisting, bidder=user, amount=bid)
            bidding.save()


    page = Listing.objects.get(pk=listing_id)
    category = Category.objects.get(item=page)
    owner = page.user
    user = request.user
    close_button = False
    victory = False

    # Check if the owner of the listing is viewing the page
    if owner == user:
        close_button = True

    # Check if the winner is viewing the page
    highestBid = Bid.objects.filter(item=page).order_by("-amount").first()
    if highestBid:
        winner = highestBid.bidder
        if user == winner:
            victory = True

    comments = Comment.objects.filter(item=page)
    bid_count = Bid.objects.filter(item=page).count()

    in_watchlist = False
    wlist = Watchlist.objects.filter(user=user)
    for model in wlist:
        if model.item == page:
            in_watchlist = True


    return render(request, "auctions/listing.html", {
        "listing": page,
        "category": category,
        "form": BidForm(),
        "close": close_button,
        "open": page.is_active,
        "victory": victory,
        "addcomment": CommentForm(),
        "comments": comments,
        "bidcount": bid_count,
        "in_watchlist": in_watchlist
    })


@login_required
def watchlist(request):
    """ Render the watchlist of the user """

    user = request.user
    wlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": wlist
    })


@login_required
def addtowatchlist(request, listing_id):
    """ Add a listing to a user's watchlist """

    user = request.user
    item =  Listing.objects.get(pk=listing_id)

    # If the listing does not already exist in the user's watchlist
    if not Watchlist.objects.filter(user=user, item=item).exists():
        entry = Watchlist(user=user, item=item)
        entry.save()
    return redirect("listing", listing_id=listing_id)


@login_required
def removefromwatchlist(request, listing_id):
    """ Remove a listing from a user's watchlist """
    user = request.user
    item =  Listing.objects.get(pk=listing_id)

    # If the listing exist in the user's watchlist
    if Watchlist.objects.filter(user=user, item=item).exists():
        entry = Watchlist.objects.get(user=user, item=item)
        entry.delete()
    return redirect("listing", listing_id=listing_id)


@login_required
def close(request, listing_id):
    """ Enable the creator of a listing to close it """

    item = Listing.objects.get(pk=listing_id)
    if item.is_active:
        item.is_active = False
        item.save()
    return redirect("listing", listing_id=listing_id)


@login_required
def add_comment(request, listing_id):
    """ Enable users to comment on listings """

    comment = CommentForm(request.POST)
    if comment.is_valid():
        comm = comment.cleaned_data["comment"]
        item = Listing.objects.get(pk=listing_id)
        user = request.user

        comment = Comment(user=user, item=item, comm=comm)
        comment.save()

    return redirect("listing", listing_id=listing_id)


def categories(request):
    """ Display a list of all available categories. If clicked, take user to a page displaying all listings of that category """

    catmodel = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": catmodel
    })


def category_listings(request, category_id):
    """ Render all listings in a particular category """

    category = Category.objects.get(id=category_id)
    items = category.item.all()

    return render(request, "auctions/category.html", {
        "category": category.category,
        "listings": items
    })


