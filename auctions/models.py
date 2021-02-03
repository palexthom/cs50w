from django.contrib.auth.models import AbstractUser
from django.db import models


class ListingManager(models.Manager):
    def create_listing(self, data_listing):

        listing = self.create()

        listing.title = data_listing['title']
        listing.brand = data_listing['brand']
        listing.description = data_listing['description']
        listing.start_bid = int(data_listing['start_bid'])
        listing.url = data_listing['pic_url']
        listing.category = data_listing['cat']
        listing.username = data_listing['username']
        listing.status = data_listing['status']

        listing.save()


class Listing(models.Model):
    ROAD = 'R'
    FIXED = 'F'
    GRAVEL = 'G'
    TOURING = 'T'
    CAT_BIKE = [(ROAD, 'Road'), (FIXED, 'Fixed'), (GRAVEL, 'Gravel'), (TOURING, 'Touring')]

    OPEN = 'O'
    CLOSE = 'C'
    STATUS = [(OPEN, 'Open'),(CLOSE, 'Close')]

    title = models.CharField(max_length=32)
    brand = models.CharField(max_length=32)
    description = models.TextField()
    start_bid = models.IntegerField(default=1)
    url = models.URLField()
    category = models.CharField(
        max_length=1,
        choices=CAT_BIKE,
        default=ROAD
    )
    username = models.CharField(max_length=32, default="admin")
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=OPEN
    )
    won_bid = models.CharField(max_length=32, null=True, blank=True)

    objects = ListingManager()


class CommentManager(models.Manager):
    def create_comment(self, author, date, text, listing):
        comment = self.create()

        comment.author = author
        comment.date = date
        comment.text = text
        comment.listing_id = listing
        comment.save()


class Comment(models.Model):
    author = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-date']


class User(AbstractUser, models.Model, models.Manager):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="users")


class BidManager(models.Manager):
    def create_bid(self, bidd, listing_id, username):
        bid = self.create()
        bid.bid_val = bidd
        bid.listing_id = Listing.objects.get(id=listing_id)
        bid.username = username
        bid.save()


class Bid(models.Model):
    username = models.CharField(max_length=32, null=True, blank=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True, blank=True)
    bid_val = models.IntegerField(null=True, blank=True)

    objects = BidManager()

    class Meta:
        ordering = ['-bid_val']
