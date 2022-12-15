from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images/%D/%M/%Y/')
    caption = models.TextField()
    bid = models.DecimalField(null=True, max_length=12, decimal_places=2, editable=True)
    multiplenum = models.IntegerField(default=2, null=True)
    closed = models.BooleanField(default=False, null=True)
    winner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True, related_name="purchased_listings")
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class Bids(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="bids")
    aurthor = models.ForeignKey(User , on_delete=models.CASCADE,related_name="bids_made")
    bid_offer = models.DecimalField(max_digits=8 , decimal_places=2)

    def clean(self):
        if self.bid_offer > self.list.starting_bid:
            # self.list.starting_bid = self.bid_offer
            # self.listing.save()
            # print(self.listing.current_price)
            return True
        else:
            return False
    
    def __str__(self):
        return f"{self.list} by {self.aurthor} offered {self.bid_offer}"


class Comments(models.Model):
    user =models.ForeignKey(User, related_name="comments_made", on_delete=models.CASCADE)
    comments = models.CharField(max_length=2048)
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments_have")

    def __str__(self):
        return f"comment by {self.user} : {self.comments[:20]} on list {self.list}"