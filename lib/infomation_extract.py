# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from ConfigParser import ConfigParser, NoOptionError, NoSectionError


import os
import re
import sys
import json
import requests, bs4, urllib
from urlparse import urlparse
import codecs
import ast
import uuid
import datetime

import threading
import time
from ConfigParser import ConfigParser, NoOptionError, NoSectionError

import os
import uuid

from lib.StoreRule_es import RuleCrawl, user_post

DEFAULT_EX_CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, 'conf', 'config.ini'))


class extract_data:
    def __init__(self, url ):
        self._config = ConfigParser()
        self.url = url

        path_url = urlparse(url).netloc

        # return
        with open(DEFAULT_EX_CONFIG_PATH) as fileID:
            self._config.readfp(fileID)
        ### selenium request


        try:
            self.target_url = self._config.get(path_url, 'target_url')
            self.all_sublink = self._config.get(path_url, 'query_all_forum')
            self.html_tag = self._config.get(path_url, 'html_tag')
            self.html_title = self._config.get(path_url, 'html_title')
            self.html_comment = self._config.get(path_url, 'html_comment')
            self.html_views = self._config.get(path_url, 'html_views')
            self.html_pagination = self._config.get(path_url, 'html_pagination')
            self.html_main_topic = self._config.get(path_url,'html_main_topic')

        except Exception as e:
            print (e)

    # @classmethod
    @property
    def get_all_sub_link(self):
        list_link = []
        # print("config path: {}".format(DEFAULT_EX_CONFIG_PATH))
        target_url = self.target_url
        all_sublink = self.all_sublink
        # print("target_url: {}, all_sublink: {}".format(target_url, all_sublink))
        urlLink = requests.get(target_url)
        data = json.loads(all_sublink)
        # print(data)
        soup = bs4.BeautifulSoup(urlLink.content)

        if self.target_url == "http://www.webtretho.com/forum/":
            for item in soup.find_all(data.keys()[0], data.values()[0]):
                tmp = (item.get('href'))

                if tmp:
                    # print (tmp)
                    reg_pattern = re.compile(os.path.join(target_url, '[A-z0-9\-\.]+'))
                    match = re.search(reg_pattern, tmp)
                    if match:
                        list_link.append(tmp)
            # return list_link
        elif self.target_url == "https://www.5giay.vn/":
            for item in soup.find_all(data.keys()[0], data.values()[0]):
                get_link = item.find('a')
                tmp = (get_link.get('href'))

                if tmp:
                    # print (tmp)
                    reg_pattern = re.compile(r'^[A-z0-9\-\.]+')
                    match = re.search(reg_pattern, tmp)
                    if match:
                        # print  ('netloc', urlparse(target_url).netloc)
                        list_link.append('https://' + os.path.join(urlparse(target_url).netloc, tmp))
            return list_link
        elif self.target_url == "https://nhattao.com/":
            for item in soup.find_all(data.keys()[0], data.values()[0]):
                tmp = (item.get('href'))

                if tmp:
                    # print (tmp)
                    reg_pattern = re.compile(r'^f/[A-z0-9\-\.]+')
                    match = re.search(reg_pattern, tmp)
                    if match:
                        # print  ('netloc', urlparse(target_url).netloc)
                        list_link.append('https://' + os.path.join(urlparse(target_url).netloc, tmp))
            # return list_link
        elif self.target_url == "http://ssc.vn/":
            for item in soup.find_all(data.keys()[0], data.values()[0]):
                tmp = (item.get('href'))

                if tmp:
                    # print (tmp)
                    reg_pattern = re.compile(r'^forums/[A-z0-9\-\.]+')
                    match = re.search(reg_pattern, tmp)
                    if match:
                        # print  ('netloc', urlparse(target_url).netloc)
                        list_link.append('https://' + os.path.join(urlparse(target_url).netloc, tmp))
            # return list_link

        else:
            for item in soup.find_all(data.keys()[0], data.values()[0]):
                tmp = (item.get('href'))

                if tmp:
                    # print (tmp)
                    reg_pattern = re.compile(r'^forums/[A-z0-9\-\.]+')
                    match = re.search(reg_pattern, tmp)
                    if match:
                        # print  ('netloc', urlparse(target_url).netloc)
                        list_link.append('https://' + os.path.join(urlparse(target_url).netloc, tmp))
            # return list_link

        return list_link

    @classmethod
    def get_soup_in_sublink(cls, sub_link):
        try:
            urlLink = requests.get(sub_link, timeout=3)
            soup = bs4.BeautifulSoup(urlLink.content)
        except Exception as e:
            urlLink = urllib.urlopen(sub_link)
            r = urlLink.read()
            soup = bs4.BeautifulSoup(r)


        return (soup)

    def get_info(self, list_link):
        HEADER = (u'url', u'main_topic', u'title', u'comment', u'view')

        html_tag = json.loads(self.html_tag)
        html_title = json.loads(self.html_title)
        html_comment = json.loads(self.html_comment)
        html_views = json.loads(self.html_views)
        html_pagination = json.loads(self.html_pagination)
        html_main_topic = json.loads(self.html_main_topic)

        UP = user_post()

        for item in list_link:
            ### soup cho mot link tu home forum
            print ("link {}".format(item))
            it = item
            soup = extract_data.get_soup_in_sublink(item)

            ### kiem tra soup nay co index ko
            max_page = soup.find(html_pagination.keys()[0], html_pagination.values()[0])
            try:
                # html_main = re.sub(',','',soup.find(html_main_topic.keys()[0], html_main_topic.values()[0]).get('content'))
                html_main = re.sub(',','',soup.find('meta', {'property' : 'og:title'}).get('content'))
            except Exception as e:
                # print (e)
                # html_main = re.sub(',','',str(soup.find('title')))
                html_main = re.sub(',', '', soup.find('title').text)
            # print (html_main_topic)
            ### neu co dung lai ham goi soup 'get_soup_in_sublink' cho moi trang index
            if max_page:
                k = max((re.findall(r'[0-9]+', max_page.text)))
                if self.target_url == 'https://www.otofun.net/forums/':
                    k = max([int(i) for i in re.findall(r'[0-9]+', max_page.text.replace('\n', ' '))])

                for index_page in range(int(k)):

                    if self.target_url == "http://www.webtretho.com/forum/":
                        new_sub_link = os.path.join( item, 'index' + str(index_page) + '.html' )
                        if (index_page >= 151):
                            print ("next")
                            break
                    else:
                        if self.target_url == "https://muare.vn/forums/":
                            new_sub_link = os.path.join(item, '?page-' + str(index_page))
                        else:
                            new_sub_link = os.path.join(item, 'page-' + str(index_page))
                        if (index_page >= 101):
                            print ("next")
                            break

                    index_link_soup = extract_data.get_soup_in_sublink(new_sub_link)
                    ### bat dau tim title, comment, view
                    for index_tag_info in index_link_soup.find_all(html_tag.keys()[0], html_tag.values()[0]):
                        try:

                            '''
                                get info member
                                    from tag: li
                                    - threater start is username post
                                        + os.path.join(self.target_url, index_tag_info.find('a',{'class':'username'}).get('href'))
                            '''
                            ###
                            ###
                            list_info = extract_data.get_user_info(self.target_url, index_tag_info)
                            ###
                            ### done extract user info
                            data = \
                                {
                                    'id': str(uuid.uuid4()),  # chi muc lon khi vua vao forum
                                    "main_link": item,
                                }


                            title = (index_tag_info.find(html_title.keys()[0], html_title.values()[0]).text.replace(',',''))
                            comments = (index_tag_info.find(html_comment.keys()[0], html_comment.values()[0]).text.replace('\n',''))
                            views = (index_tag_info.find(html_views.keys()[0], html_views.values()[0]).text.replace('\n',''))

                            '''
                            clean and make correct format for NoSQL to ESearch db
                            '''
                            # resp_body = {}


                            if comments == views and self.target_url == "http://www.webtretho.com/forum/":

                                # print(json.dumps({
                                #     'user': list_info,
                                #     'html_main': html_main,
                                #     'title': title.replace('\n', ''),
                                #     'views': extract_data.change_char2num(
                                #         re.sub('Lượt đọc', '', comments.split('    ')[0])),
                                #     'comments': extract_data.change_char2num(
                                #         re.sub('Trả lời', '', comments.split('    ')[1])),
                                # }, indent=4, encoding='utf-8'))

                                resp_weekly = {
                                    'user': list_info,
                                    'html_main': html_main,
                                    'title': title.replace('\n', ''),
                                    'views': extract_data.change_char2num(
                                        re.sub('Lượt đọc', '', comments.split('    ')[0])),
                                    'comments': extract_data.change_char2num(
                                        re.sub('Trả lời', '', comments.split('    ')[1])),
                                }
                                data.update({'resp_weekly': resp_weekly})

                                UP.create(data)
                                print (data)
                                # with codecs.open(new_dir + '/' + name_file + '.csv','a','utf-8' ) as fp:
                                #     fp.write(u'{},{},{},{}\n'.format(html_main, title.replace('\n', ''),
                                #                                      extract_data.change_char2num(re.sub('Lượt đọc', '', comments.split('    ')[0])),
                                #                                      extract_data.change_char2num(re.sub('Trả lời', '', comments.split('    ')[1]))))

                            else:
                                # print(json.dumps({
                                #     'user': list_info,
                                #     'html_main': html_main,
                                #     'title': title.replace('\n', ''),
                                #     'views': extract_data.change_char2num(re.sub('Trả lời:|Trả lời|Xem', '', comments)),
                                #     'comments': extract_data.change_char2num(re.sub('Xem:|Xem|Đọc|Đọc:', '', views)),
                                # }, indent=4, encoding='utf-8'))

                                resp_weekly = {
                                    'user': list_info,
                                    'html_main': html_main,
                                    'title': title.replace('\n', ''),
                                    'views': extract_data.change_char2num(re.sub('Trả lời:|Trả lời|Xem', '', comments)),
                                    'comments': extract_data.change_char2num(re.sub('Xem:|Xem|Đọc|Đọc:', '', views)),
                                }
                                data.update({'resp_weekly': resp_weekly})

                                UP.create(data)
                                print (data)
                                # with codecs.open(new_dir + '/' + name_file + '.csv','a','utf-8' ) as fp:
                                #     fp.write(u'{},{},{},{}\n'.format(html_main, title.replace('\n', ''),
                                #                                      extract_data.change_char2num(re.sub('Trả lời:|Trả lời|Xem', '', comments)),
                                #                                      extract_data.change_char2num(re.sub('Xem:|Xem|Đọc|Đọc:', '', views))))

                        except Exception as e:
                            print(e)
            else:
                for tag_info in soup.find_all(html_tag.keys()[0], html_tag.values()[0]):

                    list_info = extract_data.get_user_info(self.target_url, tag_info)

                    data = \
                        {
                            'id': str(uuid.uuid4()),  # chi muc lon khi vua vao forum
                            "main_link": item,
                        }

                    try:
                        title = (tag_info.find(html_title.keys()[0], html_title.values()[0]).text.replace(',',''))
                        comments =  (tag_info.find(html_comment.keys()[0], html_comment.values()[0]).text)
                        views = (tag_info.find(html_views.keys()[0], html_views.values()[0]).text)

                        if comments == views and self.target_url == "http://www.webtretho.com/forum/":
                            # print(json.dumps({
                            #     'user': list_info,
                            #     'html_main': html_main,
                            #     'title': title.replace('\n', ''),
                            #     'views': extract_data.change_char2num(re.sub('Lượt đọc', '', comments.split('    ')[0])),
                            #     'comments': extract_data.change_char2num(re.sub('Trả lời', '', comments.split('    ')[1])),
                            # }, indent=4, encoding='utf-8'))

                            resp_weekly = {
                                'user': list_info,
                                'html_main': html_main,
                                'title': title.replace('\n', ''),
                                'views': extract_data.change_char2num(
                                    re.sub('Lượt đọc', '', comments.split('    ')[0])),
                                'comments': extract_data.change_char2num(
                                    re.sub('Trả lời', '', comments.split('    ')[1])),
                            }
                            data.update({'resp_weekly': resp_weekly})

                            UP.create(data)
                            print (data)
                            # with codecs.open(new_dir + '/' + name_file + '.csv', 'a', 'utf-8') as fp:
                            #     fp.write(u'{},{},{},{}\n'.format(html_main, title.replace('\n', ''),
                            #                                      extract_data.change_char2num(re.sub('Lượt đọc', '', comments.split('    ')[0])),
                            #                                      extract_data.change_char2num(re.sub('Trả lời', '', comments.split('    ')[1]))))

                        else:
                            # print(json.dumps({
                            #     'user': list_info,
                            #     'html_main': html_main,
                            #     'title': title.replace('\n', ''),
                            #     'views': extract_data.change_char2num(re.sub('Trả lời:|Trả lời|Xem', '', comments)),
                            #     'comments': extract_data.change_char2num(re.sub('Xem:|Xem|Đọc|Đọc:', '', views)),
                            # }, indent=4, encoding='utf-8'))

                            resp_weekly = {
                                'user': list_info,
                                'html_main': html_main,
                                'title': title.replace('\n', ''),
                                'views': extract_data.change_char2num(re.sub('Trả lời:|Trả lời|Xem', '', comments)),
                                'comments': extract_data.change_char2num(re.sub('Xem:|Xem|Đọc|Đọc:', '', views)),
                            }
                            data.update({'resp_weekly': resp_weekly})

                            UP.create(data)
                            print (data)
                            # with codecs.open(new_dir + '/' + name_file + '.csv', 'a', 'utf-8') as fp:
                            #     fp.write(u'{},{},{},{}\n'.format(html_main, title.replace('\n', ''),
                            #                                      extract_data.change_char2num(re.sub('Trả lời:|Trả lời|Xem', '', comments)),
                            #                                      extract_data.change_char2num(re.sub('Xem:|Xem|Đọc|Đọc:', '', views))))

                    except Exception as e:
                        print (e)

    @classmethod
    def change_char2num(cls, numWchar):


        if 'K' in numWchar or 'k' in numWchar:
            new_num = float(re.sub('K', '', numWchar)) * 1000

        elif 'M' in numWchar or 'm' in numWchar:
            ### it means M in numWchar
            new_num = float(re.sub('M', '', numWchar)) * 1000000
        else:
            ### it mean both K and M none
            if ',' in numWchar:
                new_num = re.sub(',','', numWchar)
            elif '.' in numWchar:
                new_num = numWchar.replace('.','')
            else:
                new_num = numWchar
        return str(new_num)

    @classmethod
    def get_user_info(cls, target_url, active_link):
        list_info = []
        link_info_username = os.path.join(target_url, active_link.find('a', {'class': 'username'}).get('href'))
        user_link_soup = extract_data.get_soup_in_sublink(link_info_username)
        for item in user_link_soup.find_all('li', {'class': 'profileContent'}):
            # print ([ content.text for content in item.find_all('div', {'class':'section'})])
            for content in item.find_all('div', {'class': 'section'}):
                zzz = (content.find('div', {'class': 'primaryContent'}))
                #print zzz.text
                try:
                    list_info.append(zzz.text.replace('\n', ''))
                except Exception as e: pass
        ################## clean => to json ###################
        # for iii in list_info:
        #     print ([jjj.text for jjj in iii.find_all('dt') ])
        #     print ([jjj.text for jjj in iii.find_all('dd') ])
        #     # print ('{} ---- {}'.format(iii.find('dt').text.replace('\n',' '), iii.find('dd').text.replace('\n',' ')))
        return list_info

class extract_feed:
    def __init__(self, url):
        self._config = ConfigParser()
        self.url = url

        path_url = urlparse(url).netloc

        # return
        with open(DEFAULT_EX_CONFIG_PATH) as fileID:
            self._config.readfp(fileID)

        try:
            self.target_url = self._config.get(path_url, 'target_url')
            self.all_sublink = self._config.get(path_url, 'query_all_forum')
            self.feed_item = self._config.get(path_url, 'feed_item')
            self.feed_time_create = self._config.get(path_url, 'feed_time_create')
            self.feed_link = self._config.get(path_url, 'feed_link')
            self.feed_guild = self._config.get(path_url, 'feed_guild')
            self.feed_author = self._config.get(path_url, 'feed_author')
            self.feed_creator = self._config.get(path_url,'feed_creator')
            self.feed_comment = self._config.get(path_url,'feed_comment')

        except Exception as e:
            print (e)

    def get_feed(self):

        eA = extract_data(self.url)
        target_url = eA.target_url
        all_sublink = eA.all_sublink
        tmp = eA.get_all_sub_link

        '''
        url = 'https://nhattao.com/f/dien-thoai.543/index.rss'
        urlLink = requests.get(url)
        soup = bs4.BeautifulSoup(urlLink.content)
        '''
        data = \
            {
                'id': str(uuid.uuid4()),  # chi muc lon khi vua vao forum
                "main_link": "",
            }
        resp_daily_feed = []

        index_sub = 0

        for item in tmp:
            data.update({'main_link': os.path.join(item, 'index.rss')})
            data.update(
                {
					"list_sub_link": \
                        {
                            'id_sub_link': index_sub,
                            'sublink': os.path.join(item, 'index.rss')
                        }
                })


            new_link = os.path.join(item, 'index.rss')
            soup = extract_data.get_soup_in_sublink(new_link)

            for item in soup.find_all('item'):
                # try:
                title = item.find('title').get_text(strip=True)

                time_create = item.find('pubdate').text
                link = item.find('link')

                if not item.find('guild'):
                    guild = ""
                else:
                    guild = item.find('guild').text

                # test_val = extract_feed.is_none(guild)
                if not item.find('author'):
                    author = ""
                else:
                    author = item.find('author').text

                if not item.find('dc:creator'):
                    creator = ""
                else:
                    creator = item.find('dc:creator').text

                if not item.find('slash:comments'):
                    comment = ""
                else:
                    comment = item.find('slash:comments').text

                resp_daily_feed.append(
                    {
                        'sub_link': new_link,
                        'title': title,
                        'time_create': time_create,
                        'guild': guild,
                        'author': author,
                        'creator': creator,
                        'comment': comment
                    }
                )

                # print (json.dumps(
                #     {
                #         'sub_link': new_link,
                #         'title': title,
                #         'time_create': time_create,
                #         'guild': guild,
                #         'author': author,
                #         'creator': creator,
                #         'comment': comment
                #     }, encoding='utf-8'
                # ))
            index_sub += 1

            data.update({"resp_daily_feed": resp_daily_feed})

            RC = RuleCrawl()
            RC.create(data)
            # time.sleep(5)
        return data

# def main(url, dirpath):
#
#     if not os.path.exists(os.path.join(os.getcwd() , dirpath)):
#         print (True, "chua ton tai")
#         os.makedirs(dirpath)
#         print ("Create new path dir")
#         new_dir = os.path.join(os.getcwd() , dirpath)
#     else:
#         print ("da ton tai")
#         new_dir = os.path.join(os.getcwd() , dirpath)
#
#
#     eA = extract_data(url)
#     target_url = eA.target_url
#     all_sublink = eA.all_sublink
#     tmp = eA.get_all_sub_link
#     timestamp = '{:%H%M%S_%Y%m%d}_'.format(datetime.datetime.now())
#     '''
#     format:
#         hhmmss_yymmdd
#         hh: hour
#         mm: minutes:
#         ss: second
#         yy: year
#         mm: month
#         dd: date
#     '''
#
#     reg_pattern = re.compile(r'(tinhte|webtretho|nhattao|5giay|bkvn|muare|otofun|gsm|2banh)+')
#     path_url = re.findall(reg_pattern, url)[0]
#     name_file = timestamp + path_url
#     HEADER = (u'main_topic', u'title', u'comment', u'view')
#
#     with codecs.open(new_dir + '/' + name_file +  '.csv', 'a', 'utf-8') as fp:
#         fp.write(u'{}\n'.format(url))
#         fp.write(u'{}\n'.format(u','.join(HEADER)))
#     eA.get_info(tmp)


if __name__ == '__main__':
    # import json
    # main(sys.argv[1], sys.argv[2])
    # main('https://www.otofun.net/forums/', 'test_test_020')
    # main('http://gsm.vn/forums/', 'test_test_020')
    # main('https://www.2banh.vn/forums/', 'test_test_020')
    # main('https://www.otofun.net/forums/', 'test_test_020')
    # main('https://nhattao.com/', 'test_test_020')
    # main('https://bkvn.com/', 'test_test_020')
    # main('https://tinhte.vn/forums/', 'test_test_020')
    # main('http://www.webtretho.com/forum/', 'test_test_020')
    # print ("{}".format(os.getcwd()))
    # print ("{}".format(os.path.join(os.path.dirname(__file__), os.path.pardir, 'conf', 'config.ini')))
    # url = "https://nhattao.com/"
    # ef = extract_feed(url)
    # ef.get_feed()
    url = "https://nhattao.com/"
    ea = extract_data(url)
    tmp = ea.get_all_sub_link
    ea.get_info(tmp)


    '''
    json form 
    data = \
        {
            'id_main_link': "",                              # chi muc lon khi vua vao forum
            "main_link": "www.google.com.vn",
            "list_sub_link": [
                {
                    "id_sub_link": "",
                    "sublink": "www"
                },
                ### ...
            ],
            'resp_daily_feed': [
                {
                    "comment": "51",
                    "sub_link": "https://nhattao.com/f/sua-chua-nang-cap.725/index.rss",
                    "guild": "",
                    "creator": "phukien420",
                    "time_create": "Fri, 17 Nov 2017 10:05:14 +0000",
                    "author": "invalid@example.com (phukien420)",
                    "title": "Thay m\u1eb7t k\u00ednh Iphone 4/5/5s/6 ipad uy t\u00edn gi\u00e1 r\u1ebb"
                },
                ### ...
            ]
        }
        
    '''