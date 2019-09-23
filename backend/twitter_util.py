import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import tweepy

class Twitter:

    def __init__(self, username):
        self.username = username

    def get_request(self, username):
        endpoint = 'https://twitter.com/' + username
        req = requests.get(endpoint)
        if req.status_code == 200:
            return req.text
        else:
            return False


    def get_details(self):
        html = self.get_request(self.username)
        if html:

            info = {"username": "", "bio": "", "joined": "", 'profile_image': "", "background_image": "",
                    "number_of_tweets": "", "following": "", "followers": "", "likes": "", "emoji_links": [], "links": [],
                    "mentioned": [], "text": []}
            soup = BeautifulSoup(html)

            for user in soup.find_all('a', {'class': 'ProfileHeaderCard-nameLink u-textInheritColor js-nav'}):
                nick = user.contents[0]
                info['username'] = nick

            for description in soup.find_all('p',{'class':"ProfileHeaderCard-bio u-dir"}):
                try:
                    bio = description.contents[0]
                except IndexError:
                    bio = ""

                info['bio'] = bio


            for timestamp in soup.find_all('span',{"class":"ProfileHeaderCard-joinDateText js-tooltip u-dir"}):
                join_date = timestamp.attrs['title']
                info['joined'] = join_date

            for image in soup.find_all('a',{'class':"ProfileAvatar-container u-block js-tooltip profile-picture"}):
                profile_image = image.attrs['href']
                info['profile_image'] = profile_image

            for background in soup.find_all('div',{"class":"ProfileCanopy-headerBg"}):
                background_image = background.contents[1].attrs['src']
                info['background_image'] = background_image

            for details in soup.find_all('span',{"class":"ProfileNav-value"}):
                try:
                    if details.parent.attrs['data-nav'] == "tweets":
                        number_of_tweets = details.attrs['data-count']
                        info["number_of_tweets"] = number_of_tweets
                    if details.parent.attrs['data-nav'] == "following":
                        following = details.attrs['data-count']
                        info["following"] = following
                    if details.parent.attrs['data-nav'] == "followers":
                        followers = details.attrs['data-count']
                        info['followers'] = followers
                    if details.parent.attrs['data-nav'] == "favorites":
                        likes = details.attrs['data-count']
                        info["likes"] = likes
                except KeyError as e:
                    pass

            c = 0
            for tweets in soup.find_all('p',{"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}):
                c = c+ 1
                print("Tweet no. " + str(c))
                text1 = tweets.text
                info["text"].append(text1)
                for content in tweets.contents:
                    if isinstance(content,Tag):
                        if 'aria-label' in content.attrs:
                            emoji_link = content.attrs['src']
                            info["emoji_links"].append(emoji_link)
                        if 'data-expanded-url' in content.attrs:
                            link = content.attrs['data-expanded-url']
                            info["links"].append(link)
                        if 'data-mentioned-user-id' in content.attrs:
                            mentioned = content.attrs['href'] # only profile /aaa
                            info['mentioned'].append(mentioned)

            return info

class TwitterApi:

    def __init__(self, username, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET):
        self.username = username

        self.TWITTER_ACCESS_TOKEN = TWITTER_ACCESS_TOKEN
        self.TWITTER_ACCESS_TOKEN_SECRET = TWITTER_ACCESS_TOKEN_SECRET
        self.TWITTER_CONSUMER_KEY = TWITTER_CONSUMER_KEY
        self.TWITTER_CONSUMER_SECRET = TWITTER_CONSUMER_SECRET

        self.auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        self.auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        # Create API object
        self.api = tweepy.API(self.auth)

        self.info = {"similar":{},"favourites":"","followers":"","following":"","created_at":"","description":"","profile_pic":"","hashtags":[], "symbols":[], "user_mentions" :{}, "urls": [], "text":[], "timestamps":{}, "geo":[]}

    def get_similar(self):
        try:
            similar = self.api.search_users(self.username)
            similar_dict = {}
            for i in similar:
                if not i.screen_name == self.username:
                    similar_dict[i.screen_name] = "https://twitter.com/" + i.screen_name

            return similar_dict
        except:
            return False

    def get_details(self):
        try:
            user_info = self.api.get_user(self.username)
        except Exception as e:
            return False

        similar = self.get_similar()

        self.info['similar'] = similar
        self.info['profile_pic'] = user_info.profile_image_url_https.replace("normal","400x400")
        self.info['created_at'] = user_info.created_at.strftime("%Y-%m-%d %H:%M:%S")
        self.info['description'] = user_info.description
        self.info['favourites'] = str(user_info.favourites_count)
        self.info['followers'] = str(user_info.followers_count)
        self.info['following'] = str(user_info.friends_count)

        try:
            for status in tweepy.Cursor(self.api.user_timeline, screen_name=self.username, tweet_mode="extended").items():

                try:
                    for hashtag in status.entities['hashtags']:
                        self.info['hashtags'].append("#"+hashtag['text'])

                    for symbol in status.entities['symbols']:
                        print(symbol)

                    for mentions in status.entities['user_mentions']:
                        if mentions['screen_name'] not in self.info['user_mentions']:
                            self.info['user_mentions'][mentions['screen_name']] = "https://twitter.com/"+ self.username + "/status/"+ status.id_str

                    for url in status.entities['urls']:
                        self.info['urls'].append(url['expanded_url'])

                    if status.geo is not None:
                        print('a')

                    if not status.full_text.startswith("RT"):
                        self.info['text'].append(status.full_text)
                    self.info['timestamps'][status.created_at.strftime("%Y-%m-%d %H:%M:%S")] = "https://twitter.com/" + self.username +"/status/" + status.id_str
                except:
                    pass
        except:
            return False

        return self.info