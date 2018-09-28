from pymongo import MongoClient
import json

DB_IP = "35.194.174.101"  # 35.194.174.101
DB_PORT = 27017  # default MongoDB port
DB_NAME = "beautybot"  # use the collection


class DataBase(object):
    def drop_db(self, client, db_name):
        client.drop_database(db_name)

    def remove_all_documents(self, collection):
        print("removing all documents...")
        result = collection.delete_many({})
        print(result.deleted_count)

    def create_pixnet(self, collection_pixnet, content):
        title = content['title']
        if "唇" in title:
            category = "lips"
        elif "眼" in title:
            category = "eyes"
        elif "霜" in title:
            category = "cream"
        elif "面膜" in title:
            category = "mask"
        else:
            category = "other"
        article = {
            "article_id": content["article_id"],
            "title": title,
            "category": category,
            "tags": content['tags']
        }
        collection_pixnet.insert_one(article).inserted_id

    def create_collection_pixnet(self, collection_pixnet):
        self.remove_all_documents(collection_pixnet)
        with open("makeup.json") as json_data:
            for article in json_data:
                try:
                    j_content = json.loads(article)
                    content = {
                        "title": j_content["title"],
                        "tags": j_content['tags'],
                        "article_id": j_content['article_id']
                    }
                    print(content['title'])
                    self.create_pixnet(collection_pixnet, content)
                except KeyError as e:
                    print("KeyError" + str(e))

    def create_ptt(self, collection_ptt, content):
        title = content['title']
        if "唇" in title:
            category = "lips"
        elif "眼" in title:
            category = "eyes"
        elif "霜" in title:
            category = "cream"
        elif "面膜" in title:
            category = "mask"
        else:
            category = "other"
        article = {
            "article_id": content["article_id"],
            "title": title,
            "category": category,
            "message_all": content["message_all"],
            "message_push": content["message_push"],
            "message_boo": content["message_boo"]
        }
        collection_ptt.insert_one(article).inserted_id

    def create_collection_ptt(self, collection_ptt):
        self.remove_all_documents(collection_ptt)
        with open("MakeUp.json") as ptt_makeup_file:
            ptt_makeup = json.load(ptt_makeup_file)
            for post in ptt_makeup['articles']:
                post_id = post['article_id']
                post_title = post['article_title']
                try:
                    content = {
                        "title": post_title,
                        "article_id": post_id,
                        "message_all": post['message_conut']['all'],
                        "message_push": post['message_conut']['push'],
                        "message_boo": post['message_conut']['boo'],
                    }
                    print(content['title'])
                    self.create_ptt(collection_ptt, content)
                except KeyError as e:
                    print("KeyError" + str(e))


def main():
    client = MongoClient(DB_IP, DB_PORT)
    """
    # Put Data into monogodb
    db = DataBase()
    collection_pixnet = client[DB_NAME]["pixnet"]
    db.create_collection_pixnet(collection_pixnet)
    print(collection_pixnet.count())
    # Delete all data
    # drop_db(client, DB_NAME)
    """

    """
    db = DataBase()
    collection_ptt = client[DB_NAME]["ptt"]
    db.create_collection_ptt(collection_ptt)
    print(collection_ptt.count())
    """

    collection_pixnet = client[DB_NAME]["pixnet"]
    print(collection_pixnet.count())
    collection_ptt = client[DB_NAME]["ptt"]
    print(collection_ptt.count())

    ptt_article = collection_ptt.find({"category": "lips", "title": {"$regex": "霧面"}})
    print(ptt_article.count())
    for article in ptt_article[:5]:
        print(article)
    pixnet_article = collection_pixnet.find({"category": "lips", "title": {"$regex": "霧面"}})
    print(pixnet_article.count())
    for article in pixnet_article[:5]:
        print(article)

if __name__ == '__main__':
    main()
