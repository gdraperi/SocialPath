from django.urls import path
from social import views
from django.conf.urls import url

urlpatterns = [
    path("", views.users, name="users"),
    path("<str:name>/", views.details, name="details"),
    # url('<str:name>/delete', views.users, name='delete')
    url(r'^delete/(?P<name>.*)/$', views.delete, name='delete'),
    path("<str:name>/instagram", views.instagram, name="instagram"),
    path("<str:name>/twitter", views.twitter, name="twitter"),
    path("<str:name>/reddit", views.reddit, name="reddit"),
    path("<str:name>/facebook", views.facebook, name="facebook"),
    path("<str:name>/stackoverflow", views.stackoverflow, name="stackoverflow"),

]