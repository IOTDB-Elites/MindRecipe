from worker.database.dao import Dao
from worker.logic.utils import get_one_json_item

dao = Dao()
USER_DATABASE = 'user'
READ_DATABASE = 'read'
BEREAD_DATABASE = 'beread'
ARTICLE_DATABASE = 'article'


def get_user_info(name, region):
    user = dao.find_one(USER_DATABASE, {'name': name, 'region': region})
    if user is None:
        return {'success': False,
                'data': {}}

    return {'success': True,
            'data': user}


def get_read_list(uid):
    read_items = dao.read_data(READ_DATABASE, {'uid': uid})
    articles = dao.read_data(ARTICLE_DATABASE)
    be_read_item = dao.read_data(BEREAD_DATABASE)
    if read_items is None:
        return {'success': True,
                'data': {}}
    read_list = []
    share_list = []
    agree_list = []

    for i in read_items:
        aid = i['aid']
        timestamp = i['timestamp']
        article_info = get_one_json_item(articles, {'aid': aid})
        if article_info == {}:
            continue
        title = article_info['title']
        agreeOrNot = i['agreeOrNot']
        shareOrNot = i['shareOrNot']
        cur_beread = get_one_json_item(be_read_item, {'aid': aid})
        if cur_beread == {}:
            readNum = 0
            commentNum = 0
            agreeNum = 0
            shareNum = 0
        else:
            readNum = cur_beread['readNum']
            commentNum = cur_beread['commentNum']
            agreeNum = cur_beread['agreeNum']
            shareNum = cur_beread['shareNum']
        read_list.append({
            'aid': aid,
            'timestamp': timestamp,
            'readNum': readNum,
            'title': title,
            'commentNum': commentNum,
            'agreeNum': agreeNum,
            'shareNum': shareNum,
            'agreeOrNot': agreeOrNot,
            'shareOrNot': shareOrNot
        })
        if shareOrNot == '1':
            share_list.append({
                'aid': aid,
                'title': title,
                'readNum': readNum,
                'commentNum': commentNum,
                'agreeNum': agreeNum,
                'shareNum': shareNum
            })
        if agreeOrNot == '1':
            agree_list.append({
                'aid': aid,
                'title': title,
                'readNum': readNum,
                'commentNum': commentNum,
                'agreeNum': agreeNum,
                'shareNum': shareNum
            })
    return {'success': True,
            'data': {'read': read_list, 'share': share_list, 'agree': agree_list}}


def update_user_info(user):
    res = dao.update_one(USER_DATABASE, {'uid': user['uid']}, user)
    if res['ok'] != 1:
        return {'success': False,
                'message': 'update fail!'}

    return {'success': True,
            'message': 'update success!'}


def update_feedback(feedback):
    uid = feedback['uid']
    aid = feedback['aid']

    # check read table
    read_record = dao.find_one(READ_DATABASE, {'uid': uid, 'aid': aid})
    if read_record is None:  # if is none, insert
        res = dao.insert_many(READ_DATABASE, [{
            'timestamp': feedback['timestamp'],
            'uid': uid,
            'aid': aid,
            'readTimeLength': feedback['readTimeLength'],
            'readSequence': feedback['readSequence'],
            'readOrNot': feedback['readOrNot'],
            'commentOrNot': feedback['commentOrNot'],
            'agreeOrNot': feedback['agreeOrNot'],
            'shareOrNot': feedback['shareOrNot'],
            'commentDetail': feedback['commentDetail']
        }])
        return {'success': True,
                'message': 'update success!'}
    else:
        read_record['timestamp'] = feedback['timestamp']
        read_record['readTimeLength'] = feedback['readTimeLength']
        read_record['readSequence'] = feedback['readSequence']
        read_record['readOrNot'] = feedback['readOrNot']
        read_record['commentOrNot'] = feedback['commentOrNot']
        read_record['agreeOrNot'] = feedback['agreeOrNot']
        read_record['shareOrNot'] = feedback['shareOrNot']
        read_record['commentDetail'] = feedback['commentDetail']

        res = dao.update_one(READ_DATABASE, {'aid': aid, 'uid': uid}, read_record)

        if res['ok'] != 1:
            return {'success': False,
                    'message': 'update fail!'}
        else:
            return {'success': True,
                    'message': 'update success!'}
