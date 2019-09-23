# SocialPath
![](https://imgur.com/daYzPlO.jpg)

Write-up https://medium.com/@woj_ciech/socialpath-track-users-across-social-media-platforms-ed5226c8ee8c

Track users across social media platforms

Supported services:
- Facebook (posts only)
- Twitter
- Stackoverflow
- Instagram
- Reddit

App uses Django and D3js to draw charts.

Requirements:
- Django
- Tweepy
- PRAW
- Django related packages
- facebook_scraper

# Install
```
pip3 install -r requirements.txt
python3 manage.py makemigrations social
python3 manage.py migrate
python3 manage.py migrate social
python3 manage.py createsuperuser
python3 manage.py runserver
```
After that SocialPath will be accessible at localhost:8000/search

Paste your API keys into [backend/keys.json](https://github.com/woj-ciech/SocialPath/blob/master/backend/keys.json) Remember to escape double quotes (") in instagram cookie with \ in json

Change your timezone at [socialpath/settings.py](https://github.com/woj-ciech/SocialPath/blob/master/socialpath/settings.py#L116). It's important for scheduled background tasks.

Make sure you have added python3 to your PATH, app calls subprocess in [social/views.py](https://github.com/woj-ciech/SocialPath/blob/master/social/views.py#L52)

You can check status of the tasks on http://localhost:8000/admin/background_task

Directory is created for each user with csv inside under /static/, for visualizations.

# Screens
![](https://imgur.com/q7JwZWH.jpg)
![](https://imgur.com/YikqzMA.jpg)
![](https://imgur.com/xqRwKug.jpg)
![](https://imgur.com/AkffJES.jpg)
![](https://imgur.com/eu3d5xt.jpg)
![](https://imgur.com/sgPdznj.jpg)
![](https://imgur.com/bd1sa0c.jpg)
![](https://imgur.com/KxBlnwv.jpg)
