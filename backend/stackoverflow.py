import requests
import json
from urllib.parse import urlsplit
from datetime import datetime

class Stackoverflow:

    def __init__(self,username):

        self.username = username

    def get_similar(self):
        similar = {}
        try:
            req = requests.get(
                "https://api.stackexchange.com/2.2/users?order=desc&inname=" + self.username + "&site=stackoverflow")
            req_json = json.loads(req.content)
            for i in req_json['items']:
                similar[i['display_name']] = i['link']
        except:
            return False

        return similar

    def get_accounts(self):
        info = {}
        counter = 0
        try:
            req = requests.get(
                "https://api.stackexchange.com/2.2/users?order=desc&inname=" + self.username + "&site=stackoverflow")
            req_json = json.loads(req.content)
            for item in req_json['items']:
                if 'location' in item:
                    location = item['location']
                else:
                    location = ""

                if 'website_url' in item:
                    url = item['website_url']

                else:
                    url = ""

                id = urlsplit(item['link'])[2].split('/')[2]

                info[counter] = {'name': item['display_name'], 'last_access_date': item['last_access_date'],
                                 'reputation': item['reputation'],
                                 'created': datetime.utcfromtimestamp(item['creation_date']).strftime(
                                     '%Y-%m-%d %H:%M:%S'), 'location': location, 'url': url,
                                 'link': item['link'], 'profile_image': item['profile_image'], 'id': id}

                counter = counter + 1

            return info
        except:
            return False

    def get_details(self):

        accounts = self.get_accounts()
        if accounts:
            info1 = {"created_at": "" , "location": "", "profile_pic": "",
                     'reputation': "",
                     'last_access':"",
                     "url": "", "score": {}, "tags": {}, "text": [], "timestamps": {}, 'similar': {}, "user_url":""}


            for i in accounts:

                info1['similar'][accounts[i]['name']] = accounts[i]['link']
                if accounts[i]['name'].lower() == self.username.lower():

                    info1['url'] = accounts[i]['link']
                    info1['user_url'] = accounts[i]['url']
                    info1['last_access'] =  datetime.utcfromtimestamp(accounts[i]['last_access_date']).strftime('%Y-%m-%d %H:%M:%S')
                    info1['location'] = accounts[i]['location']
                    info1['profile_pic'] = accounts[i]['profile_image']
                    info1['reputation'] = accounts[i]['reputation']
                    info1['created_at'] = accounts[i]['created']



                    page = 1
                    has_more = True

                    while has_more:
                        req_tags = requests.get("https://api.stackexchange.com/2.2/users/" + accounts[i][
                            'id'] + "/tags?order=desc&sort=popular&site=stackoverflow&pagesize=100&page=" + str(
                            page) + "&filter=!9WaZnBfu9")
                        req_json_posts = json.loads(req_tags.content)


                        page = page + 1
                        for tag in req_json_posts['items']:
                            info1['tags'][tag['name']] = str(tag['count'])


                        has_more = req_json_posts['has_more']

                        if page == 10:
                            break

                    page = 1
                    has_more = True

                    while has_more:
                        req_posts = requests.get("https://api.stackexchange.com/2.2/users/"+accounts[i]['id']+"/posts?order=desc&sort=activity&site=stackoverflow&pagesize=100&page="+str(page)+"&filter=!3ykawIm9Sw9*3Q51G")
                        req_json_posts = json.loads(req_posts.content)

                        page = page + 1
                        for post in req_json_posts['items']:
                            info1['text'].append(post['body_markdown'])
                            info1['score'][post['score']] = post['link']
                            info1['timestamps'][datetime.utcfromtimestamp(post['creation_date']).strftime('%Y-%m-%d %H:%M:%S')] = post['link']

                        has_more = req_json_posts['has_more']

                        if page==10:
                            break

        else:
            return False

        if info1['created_at'] == "":
            return False

        return info1






