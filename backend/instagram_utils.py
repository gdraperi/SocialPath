import requests
import json
from datetime import datetime
from http.cookies import SimpleCookie
from backend import utilsy
class Instagram:

    def __init__(self, username, cookies=""):
        self.username = username

        try:
            cookie = SimpleCookie()
            cookie.load(cookies)
            self.cookies = {}
            for key, morsel in cookie.items():
                self.cookies[key] = morsel.value
        except:
            pass

        self.similar = {}


        self.info = {"similar":{},'bio':"", "bio_url":"", 'followers':"", "follow":"", 'name':"",'profile_pic':"", "descriptions":[], "captions":[], 'locations':{},'timestamps':{}}
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

    def get_request(self):
        endpoint = "https://www.instagram.com/"+self.username+"/?__a=1"
        req = requests.get(endpoint, headers=self.headers, cookies=self.cookies)

        if req.status_code == 200:
            try:
                req_json = json.loads(req.content) # why does it return html instead of json?
                return req_json
            except:
                return False
        else:
            return False

    def get_similar(self):
        try:
            similar_endpoint = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+self.username+"&rank_token=0.5850530814705502&include_reel=true"
            req_similar = requests.get(similar_endpoint,headers=self.headers)
            json_similar = json.loads(req_similar.content)
            for acc in json_similar['users']:
                self.similar[acc['user']['username']] = "https://instagram.com/" + acc['user']['username']

        except:
            return False

        return self.similar

    def get_account_info(self):
        details = self.get_request()

        self.get_similar()
        self.info['similar'] = self.similar

        if details:

            self.info['bio'] =details['graphql']['user']['biography']
            self.info['bio_url'] = details['graphql']['user']['external_url']
            self.info['followers'] = details['graphql']['user']['edge_followed_by']['count']
            self.info['follow'] = details['graphql']['user']['edge_follow']['count']
            self.info['name'] = details['graphql']['user']['full_name']
            self.info['profile_pic'] = details['graphql']['user']['profile_pic_url_hd']


            for item in details['graphql']['user']['edge_owner_to_timeline_media']['edges']:
                try:
                    self.info['descriptions'].append(item['node']['edge_media_to_caption']['edges'][0]['node']['text'])
                except:
                    pass

                if 'taken_at_timestamp' in item['node']:
                    self.info['timestamps'][datetime.utcfromtimestamp(item['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')] = "https://instagram.com/p/"+item['node']['shortcode']

                if 'location' in item['node']:
                    if item['node']['location']:
                        self.info['locations'][item['node']['location']['name']] = "https://instagram.com/p/" + item['node']['shortcode']

                try:
                    self.info['captions'].append(item['node']['accessibility_caption'])
                except:
                    pass


            has_more = details['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            end_cursor = details['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            while has_more:
                next_req_endpoint = "https://www.instagram.com/graphql/query/?query_id=17888483320059182&id="+str(details['graphql']['user']['id'])+"&first=12&after="+end_cursor
                next_req = requests.get(next_req_endpoint)
                next_req_json = json.loads(next_req.content)

                try:

                    for photo in next_req_json['data']['user']['edge_owner_to_timeline_media']['edges']:
                        for desc in photo['node']['edge_media_to_caption']['edges']:
                            self.info['descriptions'].append(desc['node']['text'])

                        if 'taken_at_timestamp' in photo['node']:
                            self.info['timestamps'][
                                datetime.utcfromtimestamp(photo['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')] = \
                                "https://instagram.com/p/" +photo['node']['shortcode']

                        if 'location' in photo['node']:
                            if photo['node']['location']:
                                self.info['locations'][photo['node']['location']['name']] = "https://instagram.com/p/"+photo['node']['shortcode']

                        try:
                            self.info['captions'].append(photo['node']['accessibility_caption'])
                        except:
                            pass

                    has_more = next_req_json['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
                    end_cursor = next_req_json['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                except:
                    pass # rate limit

            return self.info
        else:
            return False





