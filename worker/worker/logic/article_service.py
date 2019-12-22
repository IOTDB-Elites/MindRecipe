from worker.database.dao import Dao

dao = Dao()
ARTICLE_DATABASE = 'article'
POPULAR_DATABASE = 'popularrank'
BEREAD_DATABASE = 'beread'
READ_DATABASE = 'read'


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
