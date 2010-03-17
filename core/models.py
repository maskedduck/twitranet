# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import utils

STATUS=(
    ('private', 'Private'),
    ('published', 'Published'),
)

class UserProfile(models.Model):
    """A set of properties that we add on top of stock Django User model"""
    # models.User properties:
    # username - Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores).
    # first_name - Optional. 30 characters or fewer.
    # last_name - Optional. 30 characters or fewer.
    # email - Optional. E-mail address.
    # password - Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password.) Raw passwords can be arbitrarily long and can contain any character. See the “Passwords” section below.
    # is_staff - Boolean. Designates whether this user can access the admin site.
    # is_active - Boolean. Designates whether this user account should be considered active. We recommend that you set this flag to False instead of deleting accounts; that way, if your applications have any foreign keys to users, the foreign keys won’t break.
    # is_superuser - Boolean. Designates that this user has all permissions without explicitly assigning them.
    # last_login - A datetime of the user’s last login. Is set to the current date/time by default.
    # date_joined - A datetime designating when the account was created. Is set to the current date/time by default when the account is created.
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    
    external_id = models.CharField(max_length=4096, null=True, blank=True)
    bio=models.TextField(null=True, blank=True)
#    picture=
    followers=models.ManyToManyField(User,related_name='following')
    following=models.ManyToManyField(User,related_name='followers')
    
class HashTag(models.Model):
    """A hashtag implementation. Is this better than a fulltext search ?"""
    name = models.CharField(max_length=128, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        return u"#%s"%self.name
    
    @classmethod
    def get_or_create(cls, name):
        """Returns the hashtag object for the given name. 
        If object doesn't exist yet, creates a new one.
        
        name is always lower-cased and cleaned.
        """                    
        name=utils.hashify(name)
        h=HashTag.get(name=name)
        if not h:
            h=HashTag(name=name)
            h.save()                   
        return h


class Publicable(models.Model):
    """An abstract model, atom of publication."""
    owner=models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    state = models.CharField(choices=STATUS,max_length=32, default="published")
    
    hashtags = models.ManyToManyField(HashTag, blank=True, null=True)
    
    hashtags_properties=[] # list of properties where to look for hashtags 
    
    def _parse_hashtags(self):
        """Parse content of publication in order to populate hashtag tables. 
        Returns a list of hashes objects"""
        result=[]
        for property_name in self.hashtags_properties:
            property_value=self.getattr(property_name,None)
            if property_value:
                hashes=utils.find_hashes(property_value)
    
class Tweet(Publicable):
    text = models.CharField(max_length=140,)
    
    hashtags_properties=['text',] # list of properties where to look for hashtags 

