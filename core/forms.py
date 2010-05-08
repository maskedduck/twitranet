from django.forms import ModelForm
from models import *

class TweetForm(ModelForm):
    class Meta:
        model = Tweet


class ImageLinkForm(ModelForm):
    class Meta:
        model = ImageLink

