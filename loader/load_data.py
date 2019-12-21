import datetime
import json

from loader.dao import Dao

ARTICLE_PATH = '/data/mind_recipe_raw_data/article.dat'
USER_PATH = '/data/mind_recipe_raw_data/user.dat'
READ_PATH = '/data/mind_recipe_raw_data/read.dat'

ARTICLE = 'article'
USER = 'user'
READ = 'read'
BEREAD = 'beread'
POPULARRANK = 'popularrank'

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


def load_pop():
    map_aid_category = {}
    with open(ARTICLE_PATH, 'r') as load_article:
        for line in load_article:
            data = json.loads(line)
            map_aid_category[data['aid']] = data['category']

    list_id_time = []
    with open(READ_PATH, 'r') as load_read:
        for line in load_read:
            data = json.loads(line)
            timestamp = int(data['timestamp']) / 1000
            one_record = {'id': data['id'],
                          'aid': data['aid'],
                          'timestamp': timestamp,
                          'score': int(data['readOrNot'])
                                   + int(data['agreeOrNot'])
                                   + int(data['shareOrNot'])
                                   + int(data['commentOrNot'])}
            list_id_time.append(one_record)
    list_id_time.sort(key=lambda k: (k.get('timestamp'), 0), reverse=True)
    current_time = float(list_id_time[0]['timestamp'])
    day_time = last_day(current_time)
    week_time = last_week(current_time)
    month_time = last_month(current_time)

    list_aid_dayscore = []
    list_aid_monthscore = []
    list_aid_weekscore = []
    map_aid_dayscore = {}
    map_aid_monthscore = {}
    map_aid_weekscore = {}

    for i in range(0, len(list_id_time)):
        record = list_id_time[i]
        if record['timestamp'] <= day_time:
            if not (record['aid'] in map_aid_dayscore):
                map_aid_dayscore[record['aid']] = record['score']
                map_aid_monthscore[record['aid']] = record['score']
                map_aid_weekscore[record['aid']] = record['score']
            else:
                map_aid_dayscore[record['aid']] = map_aid_dayscore[record['aid']] + record['score']
                map_aid_monthscore[record['aid']] = map_aid_monthscore[record['aid']] + record['score']
                map_aid_weekscore[record['aid']] = map_aid_weekscore[record['aid']] + record['score']
        elif record['timestamp'] <= week_time:
            if not (record['aid'] in map_aid_weekscore):
                map_aid_monthscore[record['aid']] = record['score']
                map_aid_weekscore[record['aid']] = record['score']
            else:
                map_aid_monthscore[record['aid']] = map_aid_monthscore[record['aid']] + record['score']
                map_aid_weekscore[record['aid']] = map_aid_weekscore[record['aid']] + record['score']
        elif record['timestamp'] <= month_time:
            if not (record['aid'] in map_aid_monthscore):
                map_aid_monthscore[record['aid']] = record['score']
            else:
                map_aid_monthscore[record['aid']] = map_aid_monthscore[record['aid']] + record['score']
        else:
            break
    for aid, score in map_aid_dayscore.items():
        list_aid_dayscore.append({'aid': aid, 'score': score})
    for aid, score in map_aid_weekscore.items():
        list_aid_weekscore.append({'aid': aid, 'score': score})
    for aid, score in map_aid_monthscore.items():
        list_aid_monthscore.append({'aid': aid, 'score': score})
    list_aid_dayscore.sort(key=lambda k: (k.get('score'), 0), reverse=True)
    list_aid_weekscore.sort(key=lambda k: (k.get('score'), 0), reverse=True)
    list_aid_monthscore.sort(key=lambda k: (k.get('score'), 0), reverse=True)

    dbms1_day_aid = []
    dbms1_week_aid = []
    dbms1_month_aid = []
    dbms2_day_aid = []
    dbms2_week_aid = []
    dbms2_month_aid = []

    for i in range(0, len(list_aid_dayscore)):
        aid = list_aid_dayscore[i]['aid']
        if map_aid_category[aid] == 'science':
            dbms1_day_aid.append(aid)
            dbms2_day_aid.append(aid)
        elif map_aid_category[aid] == 'technology':
            dbms2_day_aid.append(aid)
    for i in range(0, len(list_aid_weekscore)):
        aid = list_aid_weekscore[i]['aid']
        if map_aid_category[aid] == 'science':
            dbms1_week_aid.append(aid)
            dbms2_week_aid.append(aid)
        elif map_aid_category[aid] == 'technology':
            dbms2_week_aid.append(aid)
    for i in range(0, len(list_aid_monthscore)):
        aid = list_aid_monthscore[i]['aid']
        if map_aid_category[aid] == 'science':
            dbms1_month_aid.append(aid)
            dbms2_month_aid.append(aid)
        elif map_aid_category[aid] == 'technology':
            dbms2_month_aid.append(aid)
    cache_dbms1 = []
    cache_dbms2 = []
    dao_dbms1 = Dao(dbms1)
    dao_dbms2 = Dao(dbms2)
    cache_dbms1.append({'id': 1,
                        'timestamp': datetime.datetime.now().timestamp(),
                        'temporalGranularity': 'daily', 'articleAidList': dbms1_day_aid})
    cache_dbms1.append({'id': 2,
                        'timestamp': datetime.datetime.now().timestamp(),
                        'temporalGranularity': 'weekly', 'articleAidList': dbms1_week_aid})
    cache_dbms1.append({'id': 3,
                        'timestamp': datetime.datetime.now().timestamp(),
                        'temporalGranularity': 'monthly', 'articleAidList': dbms1_month_aid})

    cache_dbms2.append({'id': 1,
                        'timestamp': datetime.datetime.now().timestamp(),
                        'temporalGranularity': 'daily', 'articleAidList': dbms2_day_aid})
    cache_dbms2.append({'id': 2,
                        'timestamp': datetime.datetime.now().timestamp(),
                        'temporalGranularity': 'weekly', 'articleAidList': dbms2_week_aid})
    cache_dbms2.append({'id': 3,
                        'timestamp': datetime.datetime.now().timestamp(),
                        'temporalGranularity': 'monthly', 'articleAidList': dbms2_month_aid})

    dao_dbms1.insert_many(POPULARRANK, cache_dbms1)
    dao_dbms2.insert_many(POPULARRANK, cache_dbms2)


def last_day(timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    return datetime.datetime(time.year, time.month, time.day).timestamp()


def last_week(timestamp):
    time = last_day(timestamp)
    return time - 7 * 24 * 60 * 60


def last_month(timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    return datetime.datetime(time.year, time.month, 1).timestamp()


# def lastWeek(timestamp):
#
# def lastMonth(timestamp):


if __name__ == '__main__':
    # map = load_user()
    # load_article()
    # load_read(map)
    # load_be_read()

    load_pop()

# i = int(time.time())
# print(i)
# t = time.localtime(i)
# print(time.strftime("%Y-%m-%d %H:%M:%S", t))
# x = t + relativedelta(months=-1)
# print()
# data_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

# print(t)
# print(data_time)
