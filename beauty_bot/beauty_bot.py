from pymongo import MongoClient
from database_management import PixnetDatabase
import jieba
DB_IP = "35.194.174.101"  # 35.194.174.101
DB_PORT = 27017  # default MongoDB port
DB_NAME = "beautybot"  # use the collection
class BeautyBot(object):
    def __init__(self):
        pass
    
    def chat(self, input):
        client = MongoClient(DB_IP, DB_PORT)
        collection_pixnet = client[DB_NAME]["pixnet"]
        collection_ptt = client[DB_NAME]["ptt"]
        p_db = PixnetDatabase()

        key_word = ['玫瑰金', '咬唇', '韓系', '土色', '裸色', '裸粉', '大紅', '暗紅', '血色',
                    '平價', '鍍金', '持久', '染唇', '絲絨', 'ysl', 'YSL', 'chanel', 'Chanel', 'dior', 'Dior',
                    'M.A.C', 'MAC', '雅詩蘭黛', '紀梵希', '蘭蔻', '美寶蓮', '巴黎萊雅', '紅', '試色', '分享',
                    '保溼', '顯色', '修護']
        search_rule = []
        for word in key_word:
            if word in input:
                search_rule.append({"title": {"$regex": word}})
        """
        search_rule = []
        jieba_list = list(jieba.cut_for_search(input))
        print(jieba_list)
        for word in jieba_list:
            search_rule.append({"title": {"$regex": word}})
        """
        if "唇" in input:
            search_rule = {"category": "lips",
                           "$or": search_rule
                           }
            article_list = p_db.search_article(collection_pixnet, search_rule)
            pick_pixnet_article_title = [art['title'] for art in article_list[:5]]
            list_array = ", \n".join(pick_pixnet_article_title)

            ptt_article = p_db.search_article(collection_ptt, search_rule)
            push = sum([art['message_push'] for art in ptt_article[:5]])
            total = sum([art['message_all'] for art in ptt_article[:5]])+1
            rating = push / total
            pick_ptt_article_title = [art['title'] for art in ptt_article[:5]]
            ptt_array = ", \n".join(pick_ptt_article_title)

            message = '找到 ' + str(len(article_list)) + ' 篇文章, 前5推荐：\n' + list_array + '\n'
            message += 'ptt 找到 ' + str(len(ptt_article)) + ' 篇文章, 前5推荐：\n' + ptt_array
            message += '\n 共' + str(total) + '篇回應, 推的比率為' + str(round(rating, 1))
        elif input in ['Hi', 'hi', '你好']:
            message = 'Hi~Beauty~~'
        else:
            message = '你說啥麼？'

        message_attachments = [
            {
                "fallback": "Upgrade your Slack client to use messages like these.",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "menu_options_2319",
                "actions": [
                    {
                        "name": "games_list",
                        "text": "Pick a game...",
                        "type": "select",
                        "data_source": "external"
                    }
                ]
            }
        ]
        return message, message_attachments


def main():
    lu = LanguageUnderstanding()
    lu.test()
    dm = DialogueManagement()
    dm.test()
    nlg = NaturalLanguageGeneration()
    nlg.test()


if __name__ == '__main__':
    main()
