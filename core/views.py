# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from utils import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from models import Tweet
from forms import TweetForm

@login_required
def homepage(request):
    """Renders homepage, with public timeline"""
    if request.method == 'POST': # If the form has been submitted...
        form = TweetForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            t=Tweet(text=form.cleaned_data['text'], owner=request.user)
            t.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = TweetForm() # An unbound form
    return render_to_response(request, 'homepage.html', {
        'form': form,
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

