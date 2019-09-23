from facebook_scraper import get_posts


class Facebook():

    def __init__(self, username):
        self.username = username
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

        self.info = {'username':"",'timestamps': {}, 'words':[], 'likes':{}, 'comments':{}}


    def timeline(self):
        self.info['username'] = self.username

        f = get_posts(self.username)
        try:

            for post in get_posts(self.username, pages=50):
                if post['time'] and post['post_url']:
                    self.info['timestamps'][post['time'].strftime("%Y-%m-%d %H:%M:%S")] = post['post_url']
                try:
                    self.info['words'].append(post['text'][:50])
                    if post['post_url']:
                        self.info['likes'][post['likes']] = post['post_url']
                        self.info['comments'][post['comments']] = post['post_url']
                except:
                    pass
        except Exception as e:
            pass

        if not self.info['words']:
            return False


        return self.info
