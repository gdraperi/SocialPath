import requests
from bs4 import BeautifulSoup
import praw
from datetime import datetime
from backend import utilsy

class Reddit:

    def __init__(self, username):
        self.username = username

        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

    def get_request(self, username, type):
        endpoint = 'https://reddit.com/user/' + username +"/" + type
        req = requests.get(endpoint, headers=self.headers)
        if req.status_code == 200:
            return req.text
        else:
            return False

    def get_details(self):
        html = self.get_request(self.username, 'posts')
        if html:

            info = {"karma": "", "joined": "", "bio": "", 'profile_image': "", "background_image": "", "subreddits_posts":[],'subreddits_comments':[],
                    "posts": [], "comments": []}
            soup = BeautifulSoup(html)

            for subreddits in soup.find_all('a',{"class":"_3ryJoIoycVkA88fy40qNJc _1L0pdcPf58t25Jy6ljHIKR"}):
                subredds = subreddits.contents[0]
                info['subreddits_posts'].append(subredds)

            for post in soup.find_all('h3',{"class":"_eYtD2XCVieq6emjKBH3m"}):
                posts = post.contents[0]
                info['posts'].append(posts)

            for profile_image in soup.find_all('div',{"class":"_39rt5SOMKEB5MI0D3j7M5S"}):
                image = profile_image.attrs['style'][21:-1]
                info['profile_image'] = image

            for background_image in soup.find_all('div',{'class':"_39u8lkB0jifV2dCyGxhTst"}):
                background = background_image.attrs['style'][21:-1]
                info['background_image'] = background

            for user_karma in soup.find_all('span', {'id': 'profile--id-card--highlight-tooltip--karma'}):
                karma = user_karma.contents[0]
                info['karma'] = karma

            for timestamp in soup.find_all('span',{'id':"profile--id-card--highlight-tooltip--cakeday"}):
                joined = timestamp.contents[0]
                info['joined'] = joined

            for biography in soup.find_all('div',{'class':"bVfceI5F_twrnRcVO1328"}):
                try:
                    bio = biography.contents[0]
                except IndexError:
                    bio = ""

                info['bio'] = bio

        comments = self.get_request(self.username, 'comments')

        soup2 = BeautifulSoup(comments)

        if comments:

            for comment in soup2.find_all('p',{'class':"_1qeIAgB0cPwnLhDF9XSiJM"}):
                com = comment.contents[0]
                info['comments'].append(com)

            for subreddit_comment in soup.find_all('a',{'class':"_3ryJoIoycVkA88fy40qNJc"}):
                subreddit = subreddit_comment.contents[0]
                info['subreddits_comments'].append(subreddit)

class RedditApi:

    def __init__(self,CLIENT_ID,CLIENT_SECRET,PASSWORD,USER_AGENT,USERNAME, user):
        self.user = user
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.PASSWORD = PASSWORD
        self.USER_AGENT = USER_AGENT
        self.USERNAME = USERNAME


        self.reddit = praw.Reddit(client_id=self.CLIENT_ID,
                             client_secret=self.CLIENT_SECRET,
                             password=self.PASSWORD,
                             user_agent=self.USER_AGENT,
                             username=self.USERNAME)


    def get_details(self):

        info = {"karma": "", "joined": "", 'profile_image': "",
                "subreddits":[], "ups":{},
                "text": [], 'timestamps':{}}

        subreddits = []

        try:

            info['karma'] = str(self.reddit.redditor(self.user).comment_karma)
        except:
            return False

        info['joined'] = datetime.utcfromtimestamp(self.reddit.redditor(self.user).created_utc).strftime('%Y-%m-%d %H:%M:%S')
        info['profile_image'] = self.reddit.redditor(self.user).icon_img


        for comment in self.reddit.redditor(self.user).comments.new(limit=50):
            info['text'].append(comment.body)
            info['timestamps'][datetime.utcfromtimestamp(comment.created).strftime('%Y-%m-%d %H:%M:%S')] = "https://reddit.com" + comment.permalink
            subreddits.append(comment.subreddit_name_prefixed)
            info['ups'][comment.ups] = "https://reddit.com"+ comment.permalink

        for submission in self.reddit.redditor(self.user).submissions.new(limit=50):
            info['text'].append(submission.selftext)
            info['timestamps'][datetime.utcfromtimestamp(submission.created).strftime('%Y-%m-%d %H:%M:%S')] = "https://reddit.com" + submission.permalink
            subreddits.append(submission.subreddit_name_prefixed)
            info['ups'][submission.ups] = "https://reddit.com"+ submission.permalink

        info['subreddits'] = utilsy.count_words(subreddits)

        return info


