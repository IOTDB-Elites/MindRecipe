import json

from dao import Dao

ARTICLE_PATH = '/data/mind_recipe_raw_data/article.dat'
USER_PATH = '/data/mind_recipe_raw_data/user.dat'
READ_PATH = '/data/mind_recipe_raw_data/read.dat'

ARTICLE = 'article'
USER = 'user'
READ = 'read'
BEREAD = 'beread'

dbms1 = 'mongodb://127.0.0.1:10001/mind_recipe'
dbms2 = 'mongodb://127.0.0.1:10002/mind_recipe'


def format_json(fields, raw_json):
    res = {}
    for i in range(0, len(fields)):
        filed = fields[i];
        res[filed] = raw_json[filed]
    return res


def user_format(raw_json):
    fields = ['id', 'timestamp', 'uid', 'name', 'gender', 'email', 'phone', 'dept', 'grade', 'language', 'region',
              'role', 'preferTags', 'obtainedCredits']
    return format_json(fields, raw_json)


def article_format(raw_json):
    fields = ['id', 'timestamp', 'aid', 'title', 'category', 'abstract', 'articleTags', 'authors', 'language', 'text',
              'image', 'video']
    return format_json(fields, raw_json)


def read_format(raw_json):
    fields = ['id', 'timestamp', 'uid', 'aid', 'readTimeLength', 'readSequence', 'readOrNot', 'agreeOrNot',
              'commentOrNot', 'commentDetail', 'shareOrNot']
    return format_json(fields, raw_json)


# def be_read_format(raw_json):
#     fields = ['id', 'timestamp', 'aid', 'readNum', 'readUidList', 'commentNum',
#               'commentUidList', 'agreeNum', 'agreeUidList', 'shareNum', 'shareUidList']
#     return format_json(fields, raw_json)


def load_user():
    uid_region_map = {}
    dao_dbms1 = Dao(dbms1)
    dao_dbms2 = Dao(dbms2)
    cache_dbms1 = []
    cache_dmbs2 = []
    with open(USER_PATH, 'r') as load_f:
        for line in load_f:
            data = json.loads(line)
            # data = user_format(data)
            uid_region_map[data['uid']] = data['region']
            if (data['region'] == 'Hong Kong'):
                cache_dbms1.append(data)
            elif (data['region'] == 'Beijing'):
                cache_dmbs2.append(data)
            if (len(cache_dbms1) == 100):
                dao_dbms1.insert_many(USER, cache_dbms1)
                cache_dbms1 = []
            if (len(cache_dmbs2) == 100):
                dao_dbms2.insert_many(USER, cache_dmbs2)
                cache_dmbs2 = []
        if (len(cache_dbms1) > 0):
            dao_dbms1.insert_many(USER, cache_dbms1)
        if (len(cache_dmbs2) > 0):
            dao_dbms2.insert_many(USER, cache_dmbs2)
    return uid_region_map


def load_article():
    cache_dbms1 = []
    cache_dbms2 = []
    dao_dbms1 = Dao(dbms1)
    dao_dbms2 = Dao(dbms2)
    with open(ARTICLE_PATH, 'r') as load_f:
        for line in load_f:
            data = json.loads(line)
            # data = article_format(data)
            if (data['category'] == 'science'):
                cache_dbms1.append(data)
                cache_dbms2.append(data)
            elif (data['category'] == 'technology'):
                cache_dbms2.append(data)
            if (len(cache_dbms1) == 100):
                dao_dbms1.insert_many(ARTICLE, cache_dbms1)
                cache_dbms1 = []
            if (len(cache_dbms2) == 100):
                dao_dbms2.insert_many(ARTICLE, cache_dbms2)
                cache_dbms2 = []
        if (len(cache_dbms1) > 0):
            dao_dbms1.insert_many(ARTICLE, cache_dbms1)
        if (len(cache_dbms2) > 0):
            dao_dbms2.insert_many(ARTICLE, cache_dbms2)


def load_read(user_region_map):
    cache_dbms1 = []
    cache_dbms2 = []
    dao_dbms1 = Dao(dbms1)
    dao_dbms2 = Dao(dbms2)
    with open(READ_PATH, 'r') as load_f:
        for line in load_f:
            data = json.loads(line)
            # data = article_format(data)
            if (user_region_map[data['uid']] == 'Hong Kong'):
                cache_dbms1.append(data)
            elif (user_region_map[data['uid']] == 'Beijing'):
                cache_dbms2.append(data)
            if (len(cache_dbms1) == 100):
                dao_dbms1.insert_many(READ, cache_dbms1)
                cache_dbms1 = []
            if (len(cache_dbms2) == 100):
                dao_dbms2.insert_many(READ, cache_dbms2)
                cache_dbms2 = []
        if (len(cache_dbms1) > 0):
            dao_dbms1.insert_many(READ, cache_dbms1)
        if (len(cache_dbms2) > 0):
            dao_dbms2.insert_many(READ, cache_dbms2)


def load_be_read():
    map_aid_id = {}
    map_aid_category = {}
    map_aid_timestamp = {}
    map_aid_readNum = {}
    map_aid_readUidList = {}
    map_aid_commentNum = {}
    map_aid_commentUidList = {}
    map_aid_agreeNum = {}
    map_aid_agreeUidList = {}
    map_aid_shareNum = {}
    map_aid_shareUidList = {}
    with open(ARTICLE_PATH, 'r') as load_article:
        for line in load_article:
            data = json.loads(line)
            map_aid_id[data['aid']] = data['id']
            map_aid_timestamp[data['aid']] = data['timestamp']
            map_aid_category[data['aid']] = data['category']

    with open(READ_PATH, 'r') as load_read:
        for line in load_read:
            data = json.loads(line)
            article_id = data['aid']
            if data['readOrNot'] == '1':
                map_aid_readNum[article_id] = map_aid_readNum.get(article_id, 0) + 1
                if not (article_id in map_aid_readUidList):
                    map_aid_readUidList[article_id] = []
                else:
                    map_aid_readUidList[article_id].append(data['uid'])
            if data['commentOrNot'] == '1':
                map_aid_commentNum[article_id] = map_aid_commentNum.get(article_id, 0) + 1
                if not (article_id in map_aid_commentUidList):
                    map_aid_commentUidList[article_id] = []
                else:
                    map_aid_commentUidList[article_id].append(data['uid'])
            if data['agreeOrNot'] == '1':
                map_aid_agreeNum[article_id] = map_aid_agreeNum.get(article_id, 0) + 1
                if not (article_id in map_aid_agreeUidList):
                    map_aid_agreeUidList[article_id] = []
                else:
                    map_aid_agreeUidList[article_id].append(data['uid'])
            if data['shareOrNot'] == '1':
                map_aid_shareNum[article_id] = map_aid_shareNum.get(article_id, 0) + 1
                if not (article_id in map_aid_shareUidList):
                    map_aid_shareUidList[article_id] = []
                else:
                    map_aid_shareUidList[article_id].append(data['uid'])
    cache_dbms1 = []
    cache_dbms2 = []
    dao_dbms1 = Dao(dbms1)
    dao_dbms2 = Dao(dbms2)
    for aid in map_aid_id:
        data = {'id': map_aid_id[aid],
                'timestamp': map_aid_timestamp[aid],
                'aid': aid,
                'readNum': map_aid_readNum[aid],
                'readUidList': map_aid_readUidList[aid],
                'commentNum': map_aid_commentNum[aid],
                'commentUidList': map_aid_commentUidList[aid],
                'agreeNum': map_aid_agreeNum[aid],
                'agreeUidList': map_aid_agreeUidList[aid],
                'shareNum': map_aid_shareNum[aid],
                'shareUidList': map_aid_shareUidList[aid]}
        if map_aid_category[aid] == 'science':
            cache_dbms1.append(data)
            cache_dbms2.append(data)
        elif map_aid_category[aid] == 'technology':
            cache_dbms2.append(data)
        if (len(cache_dbms1) == 100):
            dao_dbms1.insert_many(BEREAD, cache_dbms1)
            cache_dbms1 = []
        if (len(cache_dbms2) == 100):
            dao_dbms2.insert_many(BEREAD, cache_dbms2)
            cache_dbms2 = []
    if (len(cache_dbms1) > 0):
        dao_dbms1.insert_many(BEREAD, cache_dbms1)
    if (len(cache_dbms2) > 0):
        dao_dbms2.insert_many(BEREAD, cache_dbms2)


if __name__ == '__main__':
    map = load_user()
    load_article()
    load_read(map)
    load_be_read()

