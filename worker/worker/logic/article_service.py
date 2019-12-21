from worker.database.dao import Dao

dao = Dao()
USER_DATABASE = 'article'

def get_article_list(category):
    articles = dao.read_data(USER_DATABASE, {'category': category})
    if articles is None:
        return {'success': True,
                'data': {}}

    return {'success': True,
            'data': articles}