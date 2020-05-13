from worker.database.dao import Dao
# from worker.logic.hdfs_reader import read_txt
from worker.logic.paramExcep import paramExcp

dao = Dao()
ARTICLE_DATABASE = 'article'
POPULAR_DATABASE = 'popularrank'
BEREAD_DATABASE = 'beread'
READ_DATABASE = 'read'
USER_DATABASE = 'user'


def get_article_list(category, start, end):
    start = int(start) - 1
    end = int(end) - 1
    articles = dao.read_data(ARTICLE_DATABASE, {'category': category})
    total_num = len(articles)
    if start > total_num:
        return {'success': False,
                'message': 'start index out of bound'}
    if end > total_num:
        end = total_num
    articles_res = []
    for a in articles[start: end]:
        aid = a['aid']
        be_read_info = dao.find_one(BEREAD_DATABASE, {'aid': aid})
        if be_read_info is None:
            a['readNum'] = 0
            a['agreeNum'] = 0
            a['commentNum'] = 0
            a['shareNum'] = 0
        else:
            a['readNum'] = be_read_info['readNum']
            a['agreeNum'] = be_read_info['agreeNum']
            a['commentNum'] = be_read_info['commentNum']
            a['shareNum'] = be_read_info['shareNum']
        articles_res.append(a)

    if articles is None:
        return {'success': True,
                'data': {'articles': {},
                         'start_idx': start,
                         'end_idx': end,
                         'total': total_num}
                }
    return {'success': True,
            'data': {'articles': articles_res,
                     'start_idx': start,
                     'end_idx': end,
                     'total': total_num
                     }
            }


def get_article(aid):
    article = dao.find_one(ARTICLE_DATABASE, {'aid': aid})

    if article is None:
        return {'success': True,
                'data': {}}

    # filename = 'articles/article' + str(article['aid']) + '/' + str(article['text'])  ## TODO
    # lines = read_txt(filename)
    article['text'] = 'TsinghuaTsinghua'

    # imgs = []
    # for image_name in article['image']:
    #     imgs.append(read_img('articles/article' + str(article['aid']) + '/' + image_name))
    #
    # article['image'] = imgs

    return {'success': True,
            'data': article}


def get_feedback(aid):
    feedback = dao.find_one(BEREAD_DATABASE, {'aid': aid})
    if feedback is None:
        return {'success': True,
                'data': {}}
    commentUidList = feedback['commentUidList']
    commentList = []
    for uid in commentUidList:
        read_records = dao.find_one(READ_DATABASE, {'aid': aid, 'uid': uid})
        if read_records is None:
            continue
        comment_details = read_records['commentDetail']
        commentList.append({'uid': uid, 'commentDetail': comment_details})
    del feedback['commentUidList']
    feedback['commentList'] = commentList
    return {'success': True,
            'data': feedback}


def get_popular():
    popular_rank = dao.read_data(POPULAR_DATABASE)
    if popular_rank is None:
        return {'success': True,
                'data': {}}

    for i in range(0, len(popular_rank)):
        one_record = popular_rank[i]
        aid_list = one_record['articleAidList']
        if len(aid_list) > 10:
            aid_list = aid_list[0:10]
        article_detail_list = []
        for aid in aid_list:
            article_detail = dao.find_one(ARTICLE_DATABASE, {'aid': aid})
            be_read_info = dao.find_one(BEREAD_DATABASE, {'aid': aid})
            if be_read_info is None:
                article_detail['readNum'] = 0
                article_detail['agreeNum'] = 0
                article_detail['commentNum'] = 0
                article_detail['shareNum'] = 0
            else:
                article_detail['readNum'] = be_read_info['readNum']
                article_detail['agreeNum'] = be_read_info['agreeNum']
                article_detail['commentNum'] = be_read_info['commentNum']
                article_detail['shareNum'] = be_read_info['shareNum']
            article_detail_list.append(article_detail)
        one_record['articles'] = article_detail_list
        del popular_rank[i]['articleAidList']
        popular_rank[i]['articles'] = article_detail_list

    return {'success': True,
            'data': popular_rank}


# def update_feedback(feedback):
#     uid = feedback['uid']
#     aid = feedback['aid']
#
#     delta_share = 0
#     delta_comment = 0
#     delta_agree = 0
#     delta_read = 0
#
#     res = {'success': False,
#            'data': {
#                'read_update': False,
#                'be_read_update': False
#            }}
#
#     user_record = dao.find_one(USER_DATABASE, {'uid': uid})
#     if user_record is not None:
#
#         # check read table
#         read_record = dao.find_one(READ_DATABASE, {'uid': uid, 'aid': aid})
#         if read_record is None:  # if is none, insert
#             delta_read = 1
#             delta_agree = int(feedback['agreeOrNot'])
#             delta_comment = int(feedback['commentOrNot'])
#             delta_share = int(feedback['shareOrNot'])
#
#             dao.insert_many(READ_DATABASE, [{
#                 'timestamp': feedback['timestamp'],
#                 'uid': uid,
#                 'aid': aid,
#                 'readTimeLength': feedback['readTimeLength'],
#                 'readSequence': feedback['readSequence'],
#                 'readOrNot': feedback['readOrNot'],
#                 'commentOrNot': feedback['commentOrNot'],
#                 'agreeOrNot': feedback['agreeOrNot'],
#                 'shareOrNot': feedback['shareOrNot'],
#                 'commentDetail': feedback['commentDetail']
#             }])
#             res['data']['read_update'] = True
#         else:
#             delta_agree = int(feedback['agreeOrNot']) - int(read_record['agreeOrNot'])
#             print("del_garee = " + str(delta_agree))
#             delta_comment = int(feedback['commentOrNot']) - int(read_record['commentOrNot'])
#             delta_share = int(feedback['shareOrNot']) - int(read_record['shareOrNot'])
#             read_record['timestamp'] = feedback['timestamp']
#             read_record['readTimeLength'] = feedback['readTimeLength']
#             read_record['readSequence'] = feedback['readSequence']
#             read_record['readOrNot'] = feedback['readOrNot']
#             read_record['commentOrNot'] = feedback['commentOrNot']
#             read_record['agreeOrNot'] = feedback['agreeOrNot']
#             read_record['shareOrNot'] = feedback['shareOrNot']
#             read_record['commentDetail'] = feedback['commentDetail']
#
#             update_read_res = dao.update_one(READ_DATABASE, {'aid': aid, 'uid': uid}, read_record)
#
#             if update_read_res['ok'] != 1:
#                 # res['data']['read_update'] = False
#                 return res
#             else:
#                 res['data']['read_update'] = True
#                 # return {'success': False,
#                 #         'message': 'update fail!'}
#             # else:
#             #     return {'success': True,
#             #             'message': 'update success!'}
#
#     article_record = dao.find_one(ARTICLE_DATABASE, {'aid': aid})
#
#     if article_record is not None:
#
#         # update be-read table
#         be_read_record = dao.find_one(BEREAD_DATABASE, {'aid': aid})
#         print(be_read_record)
#         print(delta_agree)
#         if be_read_record is None:
#             timestamp = feedback['timestamp']
#             readNum = 1
#             readUidList = [uid]
#             if delta_comment == 1:
#                 commentNum = 1
#                 commentUidList = [uid]
#             elif delta_comment == 0:
#                 commentNum = 0
#                 commentUidList = []
#             else:
#                 raise paramExcp('commentNum is wrong')
#             if delta_share == 1:
#                 shareNum = 1
#                 shareUidList = [uid]
#             elif delta_comment == 0:
#                 shareNum = 0
#                 shareUidList = []
#             else:
#                 raise paramExcp('shareNum is wrong')
#             if delta_agree == 1:
#                 agreeNum = 1
#                 agreeUidList = [uid]
#             elif delta_comment == 0:
#                 agreeNum = 0
#                 agreeUidList = []
#             else:
#                 raise paramExcp('agreeNum is wrong')
#
#             record = {
#                 'timestamp': timestamp,
#                 'aid': aid,
#                 'readNum': readNum,
#                 'readUidList': readUidList,
#                 'commentNum': commentNum,
#                 'commentUidList': commentUidList,
#                 'agreeNum': agreeNum,
#                 'agreeUidList': agreeUidList,
#                 'shareNum': shareNum,
#                 'shareUidList': shareUidList
#             }
#             dao.insert_many(BEREAD_DATABASE, [record])
#             res['data']['be_read_update'] = True
#             # return {'success': True,
#             #         'message': 'update success!'}
#         else:
#             be_read_record['timestamp'] = feedback['timestamp']
#             readUidList = be_read_record['readUidList']
#             if delta_read == 1:
#                 readUidList.append(uid)
#             be_read_record['readUidList'] = readUidList
#             be_read_record['readNum'] = int(be_read_record['readNum']) + delta_read
#             if delta_comment == -1:
#                 be_read_record['commentUidList'].remove(uid)
#             elif delta_comment == 1:
#                 be_read_record['commentUidList'].append(uid)
#             be_read_record['commentNum'] = int(be_read_record['commentNum']) + delta_comment
#             if delta_agree == -1:
#                 be_read_record['agreeUidList'].remove(uid)
#             elif delta_agree == 1:
#                 be_read_record['agreeUidList'].append(uid)
#             be_read_record['agreeNum'] = int(be_read_record['agreeNum']) + delta_agree
#             if delta_share == -1:
#                 be_read_record['shareUidList'].remove(uid)
#             elif delta_share == 1:
#                 be_read_record['shareUidList'].append(uid)
#             be_read_record['shareNum'] = int(be_read_record['agreeNum']) + delta_share
#             update_be_read_res = dao.update_one(BEREAD_DATABASE, {'aid': aid}, be_read_record)
#             if update_be_read_res['ok'] != 1:
#                 return res
#                 # return {'success': False,
#                 #         'message': 'update fail!'}
#             else:
#                 res['data']['be_read_update'] = True
#                 # return {'success': True,
#                 #         'message': 'update success!'}
#     res['success'] = True
#
#     return res


def update_read(read_record):
    uid = read_record['uid']
    aid = read_record['aid']
    old_read_record = dao.find_one(READ_DATABASE, {'uid': uid, 'aid': aid})
    if old_read_record is not None:
        delta_comment = int(read_record['commentOrNot']) - int(old_read_record['commentOrNot'])
        delta_share = int(read_record['shareOrNot']) - int(old_read_record['shareOrNot'])
        delta_agree = int(read_record['agreeOrNot']) - int(old_read_record['agreeOrNot'])
        delta_read = 0
        res = dao.update_one(READ_DATABASE, {'uid': uid, 'aid': aid}, read_record)
        if res['ok'] != 1:
            return {'success': False,
                    'message': 'update fail!'}
    else:
        delta_comment = int(read_record['commentOrNot'])
        delta_share = int(read_record['shareOrNot'])
        delta_agree = int(read_record['agreeOrNot'])
        delta_read = 1
        dao.insert_many(READ_DATABASE, [read_record])

    return {'success': True,
            'message': 'update success!',
            'data': {'delta_comment': delta_comment, 'delta_share': delta_share, 'delta_agree': delta_agree,
                     'delta_read': delta_read}}


def update_be_read(update_be_read_data):
    uid = update_be_read_data['uid']
    aid = update_be_read_data['aid']
    be_read_item = dao.find_one(BEREAD_DATABASE, {'aid': aid})
    delta_comment = update_be_read_data['delta_comment']
    delta_agree = update_be_read_data['delta_agree']
    delta_share = update_be_read_data['delta_share']
    delta_read = update_be_read_data['delta_read']
    if be_read_item is None:
        timestamp = update_be_read_data['timestamp']
        readNum = 1
        readUidList = [uid]
        if delta_comment == 1:
            commentNum = 1
            commentUidList = [uid]
        elif delta_comment == 0:
            commentNum = 0
            commentUidList = []
        else:
            raise paramExcp('commentNum is wrong')
        if delta_share == 1:
            shareNum = 1
            shareUidList = [uid]
        elif delta_comment == 0:
            shareNum = 0
            shareUidList = []
        else:
            raise paramExcp('shareNum is wrong')
        if delta_agree == 1:
            agreeNum = 1
            agreeUidList = [uid]
        elif delta_comment == 0:
            agreeNum = 0
            agreeUidList = []
        else:
            raise paramExcp('agreeNum is wrong')
        record = {
            'timestamp': timestamp,
            'aid': aid,
            'readNum': readNum,
            'readUidList': readUidList,
            'commentNum': commentNum,
            'commentUidList': commentUidList,
            'agreeNum': agreeNum,
            'agreeUidList': agreeUidList,
            'shareNum': shareNum,
            'shareUidList': shareUidList
        }
        dao.insert_many(BEREAD_DATABASE, [record])
        return {
            'success': True,
            'message': 'update success'
        }
    else:
        timestamp = update_be_read_data['timestamp']
        readUidList = be_read_item['readUidList']
        if delta_read == 1:
            readUidList.append(uid)
        readNum = int(be_read_item['readNum']) + delta_read

        commentUidList = be_read_item['commentUidList']
        if delta_comment == -1:
            commentUidList.remove(uid)
        elif delta_comment == 1:
            commentUidList.append(uid)
        commentNum = int(be_read_item['commentNum']) + delta_comment

        agreeUidList = be_read_item['agreeUidList']
        if delta_agree == -1:
            agreeUidList.remove(uid)
        elif delta_agree == 1:
            agreeUidList.append(uid)
        agreeNum = int(be_read_item['agreeNum']) + delta_agree

        shareUidList = be_read_item['shareUidList']
        if delta_share == -1:
            shareUidList.remove(uid)
        elif delta_share == 1:
            shareUidList.append(uid)
        shareNum = int(be_read_item['shareNum']) + delta_share
        record = {
            'timestamp': timestamp,
            'aid': aid,
            'readNum': readNum,
            'readUidList': readUidList,
            'commentNum': commentNum,
            'commentUidList': commentUidList,
            'agreeNum': agreeNum,
            'agreeUidList': agreeUidList,
            'shareNum': shareNum,
            'shareUidList': shareUidList
        }
        update_be_read_res = dao.update_one(BEREAD_DATABASE, {'aid': aid}, record)
        if update_be_read_res['ok'] != 1:
            return {
                'success': False,
                'message': 'update be read table failed',
                'data': {}
            }
    return {
        'success': True,
        'message': 'update success',
        'data': {}
    }
