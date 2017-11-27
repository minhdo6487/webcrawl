from elasticsearch import Elasticsearch, NotFoundError
import requests, os

class RuleCrawl:
    # def __init__(self, index, doctype):
    # def __init__(self, index, doctype):
    def __init__(self):
        self.host = "elasticsearch"
        self.port = 9200
        # self.index = index #'feed'
        self.index = 'feed'
        # self.doctype = doctype #'daily'
        self.doctype = 'daily'
        self._es = Elasticsearch(
                            host=self.host,
                            port=self.port
                            )
    def __repr__(self):
        print
        pass

    @classmethod
    def create(cls, rule_crawl):
        model = RuleCrawl()
        es = RuleCrawl()._es
        # rule crawl should should be add when call save method
        # query all data in elasticsearch
        # "http://localhost:9200/[your index name]/_search?size=1000&from=0"
        # "http://localhost:9200/rule/_search?size=1000&from=0"
        #
        raw = es.index(
                        index=model.index,
                        doc_type=model.doctype,
                        id=rule_crawl['id'],
                        body=rule_crawl,
                        )
        return raw

    @classmethod
    def update(self, rule_id, rule_crawl):
        model = RuleCrawl()
        es = RuleCrawl()._es
        raw = es.update(
                        index=model.index,
                        doc_type=model.doctype,
                        id=rule_id,
                        body={"doc": rule_crawl}
                        )
        return raw

    def search(self, url_netloc, url_path):
        raw = self._es.search(
                                index= RuleCrawl().index,
                                body= {

                                        "query":
                                            {"match_all":
                                                {}
                                            }
                                        },
                                doc_type="list_rule",
                                scroll="2m",
                                size= 10000
                                )
        return raw

class user_post():
    def __init__(self):
        self.host = "elasticsearch"
        self.port = 9200
        # self.index = index #'feed'
        self.index = 'user_post'
        # self.doctype = doctype #'daily'
        self.doctype = 'weekly'
        self._es = Elasticsearch(
            host=self.host,
            port=self.port
        )

    @classmethod
    def create(cls, rule_crawl):
        model = user_post()
        es = user_post()._es
        # rule crawl should should be add when call save method
        # query all data in elasticsearch
        # "http://localhost:9200/[your index name]/_search?size=1000&from=0"
        # "http://localhost:9200/rule/_search?size=1000&from=0"
        #
        raw = es.index(
            index=model.index,
            doc_type=model.doctype,
            id=rule_crawl['id'],
            body=rule_crawl,
        )
        return raw

    @classmethod
    def update(self, rule_id, rule_crawl):
        model = user_post()
        es = user_post()._es
        raw = es.update(
            index=model.index,
            doc_type=model.doctype,
            id=rule_id,
            body={"doc": rule_crawl}
        )
        return raw
if __name__ == '__main__':

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
    # RuleCrawl.create(data)
    # RuleCrawl()
    raw = RuleCrawl.search(RuleCrawl(),"xxx","yyy")
