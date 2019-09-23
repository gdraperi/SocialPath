from background_task import background
from backend import instagram_utils, twitter_util
from backend import stackoverflow
from .models import Users
from backend import utilsy, reddit_util,facebook, stackoverflow
from datetime import datetime


@background(schedule=1)
def instag(username, cookie):
    utilsy.create_directory(username+"/instagram")
    insta = instagram_utils.Instagram(username, cookie)
    account_info = insta.get_account_info()
    u = Users.objects.get(name=username)
    if account_info:
        u.insta_exists = True
        u.insta_name = account_info['name']
        if account_info['bio']:
            u.insta_bio = account_info['bio']
        u.insta_timestamps = account_info['timestamps']
        u.insta_locations = account_info['locations']
        u.insta_bio_url = account_info['bio_url']
        u.insta_followers = account_info['followers']
        u.insta_follow = account_info['follow']
        u.insta_name = account_info['name']
        u.insta_profile_pic = account_info['profile_pic']
        u.insta_descriptions = account_info['descriptions']
        u.insta_captions = account_info['captions']
        u.insta_similar = account_info['similar']
        utilsy.savecsv(account_info['timestamps'], "calendar", username + "/instagram")
        hashtags = utilsy.count_hashtags(account_info['descriptions'], "")
        utilsy.savecsv(hashtags, "hashtags", username + "/instagram")
        words = utilsy.count_text(account_info['descriptions'])
        utilsy.savecsv(words, "words", username + "/instagram")
    else:
        similar = insta.get_similar()
        if similar:
            u.insta_similar = similar

    u.save()

@background(schedule=1)
def twitter_task(username,TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET):
    utilsy.create_directory(username+"/twitter")
    twitter = twitter_util.TwitterApi(username,TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET)
    account_info = twitter.get_details()
    u = Users.objects.get(name=username)
    if account_info:
        u.twitter_exists = True # ?
        u.twitter_timestamps = account_info['timestamps']
        u.twitter_geo = account_info['geo']
        u.twitter_created_at = account_info['created_at']
        u.twitter_bio = account_info['description']
        u.twitter_text = account_info['text']
        u.twitter_hashtags = account_info['hashtags']
        u.twitter_user_mentions = account_info['user_mentions']
        u.twitter_url = account_info['urls']
        u.twitter_symbols = account_info['symbols']
        u.twitter_profile_pic = account_info['profile_pic']
        u.twitter_favourites = account_info['favourites']
        u.twitter_following = account_info['following']
        u.twitter_followers = account_info['followers']
        u.twitter_similar = account_info['similar']

        utilsy.savecsv(account_info['timestamps'], "calendar", username + "/twitter")
        hashtags = utilsy.count_hashtags(account_info['hashtags'], 'twitter')
        utilsy.savecsv(hashtags, "hashtags", username + "/twitter")
        words = utilsy.count_text(account_info['text'])
        utilsy.savecsv(words, "words", username + "/twitter")
    else:
        similar = twitter.get_similar()
        if similar:
            u.twitter_similar = similar

        u.twitter_bio = "User does not exist"

    u.save()



@background(schedule=1)
def reddit_task(username, CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME):

    utilsy.create_directory(username+"/reddit")

    red = reddit_util.RedditApi(CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME, username)

    account_info = red.get_details()
    u = Users.objects.get(name=username)
    if account_info:
        u.reddit_exists = True

        u.reddit_timestamps = account_info['timestamps']
        u.reddit_karma = account_info['karma']
        u.reddit_joined = account_info['joined']
        u.reddit_profile_pic = account_info['profile_image']
        u.reddit_text = account_info['text']
        u.reddit_subreddits = account_info['subreddits']
        u.reddit_ups = account_info['ups']


        if account_info['timestamps']:
            utilsy.savecsv(account_info['timestamps'], "calendar", username + "/reddit")

        if account_info['subreddits']:
            hashtags = utilsy.count_words(account_info['subreddits'])
            utilsy.savecsv(hashtags, "hashtags", username + "/reddit")

        if account_info['text']:
            words = utilsy.count_text(account_info['text'])
            utilsy.savecsv(words, "words", username + "/reddit")

    else:
        pass

    u.save()


@background(schedule=1)
def facebook_task(username):
    utilsy.create_directory(username+"/facebook")
    f = facebook.Facebook(username)
    account_info = f.timeline()
    u = Users.objects.get(name=username)
    if account_info:
        u.facebook_exists = True

        u.facebook_timestamps = account_info['timestamps']
        u.facebook_comments = account_info['comments']
        u.facebook_likes = account_info['likes']
        u.facebook_text = account_info['words']

        utilsy.savecsv(account_info['timestamps'], "calendar", username + "/facebook")
        words = utilsy.count_text(account_info['words'])
        utilsy.savecsv(words, "words", username + "/facebook")


    u.save()



@background(schedule=1)
def stackoverflow_task(username):
    utilsy.create_directory(username+"/stackoverflow")
    s = stackoverflow.Stackoverflow(username)
    account_info = s.get_details()
    u = Users.objects.get(name=username)
    if account_info:
        u.stackoverflow_exists = True
        u.stackoverflow_location = account_info['location']
        u.stackoverflow_reputation = account_info['reputation']
        u.stackoverflow_created_at = account_info['created_at']
        u.stackoverflow_last_access = account_info['last_access']
        u.stackoverflow_url = account_info['url']
        u.stackoverflow_score = account_info['score']
        u.stackoverflow_tags = account_info['tags']
        u.stackoverflow_text = account_info['text']
        u.stackoveflow_timestamps = account_info['timestamps']
        u.stackoverflow_profile_pic = account_info['profile_pic']
        u.stackoverflow_similar = account_info['similar']
        u.stackoverflow_user_url = account_info['user_url']
        utilsy.savecsv(account_info['timestamps'], "calendar", username + "/stackoverflow")
        utilsy.savecsv(account_info['tags'], "hashtags", username + "/stackoverflow")
        words = utilsy.count_text(account_info['text'])
        utilsy.savecsv(words, "words", username + "/stackoverflow")

    else:
        similar = s.get_similar()
        if similar:
            u.stackoverflow_similar = similar


    u.save()

