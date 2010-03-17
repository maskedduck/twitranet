from django.contrib import admin
from models import HashTag, Tweet

class HashTagAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['name',]
    list_display=('name',)


class TweetAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['text',]
    list_display=('owner','modified','text')
    list_filter=('state',)
    

admin.site.register(HashTag, HashTagAdmin)
admin.site.register(Tweet, TweetAdmin)
