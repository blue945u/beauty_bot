from pymongo import MongoClient
import json

DB_IP = "35.194.174.101"  # 35.194.174.101
DB_PORT = 27017  # default MongoDB port
DB_NAME = "beautybot"  # use the collection

class PixnetDatabase(object):

    def __init__(self):
        pass

    def search_article(self, collection_pixnet, search_rule):
        article_list = []
        for article in collection_pixnet.find(search_rule):
            print(article['title'])
            article_list.append(article)
        return article_list


def main():
    client = MongoClient(DB_IP, DB_PORT)
    collection_pixnet = client[DB_NAME]["pixnet"]
    print("Total Pixnet articles: ", collection_pixnet.count())

    search_rule = {"category": "lips", "title": {"$regex": "霧"}}
    pixnet_db = PixnetDatabase()
    pixnet_db.search_article(collection_pixnet, search_rule)


if __name__ == '__main__':
    main()