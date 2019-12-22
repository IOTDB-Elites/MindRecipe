from worker.database.dao import Dao

dao = Dao()
ARTICLE_DATABASE = 'article'
POPULAR_DATABASE = 'popularrank'
BEREAD_DATABASE = 'beread'


def get_article_list(category):
    articles = dao.read_data(ARTICLE_DATABASE, {'category': category})
    if articles is None:
        return {'success': True,
                'data': {}}

    return {'success': True,
            'data': articles}


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
    return {'success': True,
            'data': feedback}

def get_popular():
    popular_rank = dao.read_data(POPULAR_DATABASE)
    if popular_rank is None:
        return {'success': True,
                'data': {}}

    return {'success': True,
            'data': popular_rank}
