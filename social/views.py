from django.shortcuts import render
from django.contrib.auth.models import User

from social.models import Users
from django.contrib import messages
from .tasks import instag, twitter_task, reddit_task, facebook_task, stackoverflow_task

from backend import utilsy

from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from social.forms import PostForm
from django.core import serializers
import subprocess
from django import forms


def search(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if not Users.objects.filter(name=name).exists():
                u = Users(name=name)
                u.save()
                utilsy.create_directory(name)
                keys = utilsy.get_keys()
                # subprocess.Popen(['python', 'manage.py', 'process_tasks'], stdout=subprocess.PIPE,
                #              stderr=subprocess.PIPE)
                #
                twitter_task(name, keys['keys']['twitter']['TWITTER_ACCESS_TOKEN'],keys['keys']['twitter']['TWITTER_ACCESS_TOKEN_SECRET'],
                             keys['keys']['twitter']['TWITTER_CONSUMER_KEY'], keys['keys']['twitter']['TWITTER_CONSUMER_SECRET'])
                # subprocess.Popen(['python', 'manage.py', 'process_tasks'], stdout=subprocess.PIPE,
                #              stderr=subprocess.PIPE)

                # subprocess.Popen(['python', 'manage.py', 'process_tasks'], stdout=subprocess.PIPE,
                #               stderr=subprocess.PIPE)


                reddit_task(name, keys['keys']['reddit']['CLIENT_ID'], keys['keys']['reddit']['CLIENT_SECRET'],keys['keys']['reddit']['PASSWORD'],
                            keys['keys']['reddit']['USER_AGENT'], keys['keys']['reddit']['USERNAME'])
                stackoverflow_task(name)
                # subprocess.Popen(['python', 'manage.py', 'process_tasks'], stdout=subprocess.PIPE,
                #               stderr=subprocess.PIPE)

                facebook_task(name)
                instag(name, keys['keys']['instagram']['instagram_cookie'])

                #
                subprocess.Popen(['python3', 'manage.py', 'process_tasks'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

                return redirect('users')
            else:

                messages.warning(request, 'User already exists in the database.')  # <-
                return render(request, 'search.html', {'form': form})

                # raise form.ValidationError('Looks like a username with that email or password already exists')
        else:
            messages.error(request, "Error")
    else:
        form = PostForm()

    return render(request, 'search.html', {'form': form})

def delete(request, name):
    p = Users.objects.filter(name=name)
    p.delete()
    context = {
        'details': details
    }

    return redirect('users')
    # return redirect("social_index.html")

# class UserDelete(DeleteView):
#     model = Users
#     success_url = reverse_lazy('index')
#
#     def user_delete(self, request, *args, **kwargs):
#         obj = self.get_object()
#         messages.success(request, '{} was deleted'.format(obj.name))
#         return super(UserDelete, self).delete(request, *args, **kwargs)

def instagram(request, name):
    instagram_details = Users.objects.get(name=name)
    context = {
        'details': instagram_details
    }

    return render(request, 'instagram.html', context)

def stackoverflow(request, name):
    stackoverflow_details = Users.objects.get(name=name)
    context = {
        'details': stackoverflow_details
    }

    return render(request, 'stackoverflow.html', context)

def facebook(request, name):
    facebook_details = Users.objects.get(name=name)
    context = {
        'details': facebook_details
    }

    return render(request, 'facebook.html', context)

def reddit(request, name):
    reddit_details = Users.objects.get(name=name)
    context = {
        'details': reddit_details
    }

    return render(request, 'reddit.html', context)

def twitter(request, name):
    twitter_details = Users.objects.get(name=name)
    context = {
        'details': twitter_details
    }

    return render(request, 'twitter.html', context)


def details(request, name):
    details = Users.objects.get(name=name)
    context = {
        'details':details
    }

    return render(request, 'social_details.html',context)


# def social_details(request, pk):
#     users = Users.objects.get(pk=pk)
#
#     context = {
#
#         'name': users
#
#     }
#
#     return render(request, 'social_details.html', context)

class UserDelete(DeleteView):
    model = Users
    success_url = reverse_lazy('social_index.html')

def users(request):
    users = Users.objects.all()
    context = {

        'name': users

    }
    return render(request, 'social_index.html', context)


