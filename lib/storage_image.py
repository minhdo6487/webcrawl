import urllib
import re, requests, bs4
import ast
import os
import sys
import json
import uuid

folder_name = sys.argv[1]
url_link = sys.argv[2]

class storage_img:
    path_img = "/media/images/"
    folder_name = sys.argv[1]
    url_link = sys.argv[2]

    @classmethod
    def store_img(cls, url, num, folder):
        path_dir = storage_img.path_img

        name_url = str(num) + ".jpg"

        urllib.urlretrieve(url, path_dir+str(folder)+'/'+name_url)

    @classmethod
    def crawl_img(cls, url):
        fol_name = os.makedirs('/media/images/'+storage_img.folder_name)
        #fol_name = os.makedirs(storage_img.folder_name)
        mmm = storage_img.folder_name
        nnn = storage_img.url_link
        urlLink = requests.get(nnn)
        count_index = 0
        soup = bs4.BeautifulSoup(urlLink.content)
        for item in soup.body:
            for url_img in item.split('\n'):
                storage_img.store_img(url_img, count_index, mmm)
                count_index += 1

    @classmethod
    def api_from_pixelbay(cls):
        url = "https://pixabay.com/api/"
        mmm = storage_img.folder_name
        #fol_name = os.makedirs(storage_img.folder_name)
        fol_name = os.makedirs('/media/images/'+storage_img.folder_name)
        querystring = {
                        "key":"5983412-c5bef11f746432e97a446b798",
                        "q":mmm,
                        "image_type":"photo",
                        "per_page":"200"
                        }
        headers = {
                    'cache-control': "no-cache",
                    'postman-token': "13bbcbbf-07d7-8fbe-e587-45f17ea204ff"
                    }
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.text
        #print urls
        data = json.loads(res)
        #print urls['hits'][0]['webformatURL']
        #count_index = 0
        for url in data['hits']:
            url_img = url['webformatURL']
            storage_img.store_img(url_img, uuid.uuid4(), mmm)
            #count_index += 1



if __name__ == '__main__':
    storage_img.api_from_pixelbay()
