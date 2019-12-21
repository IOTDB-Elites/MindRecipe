from worker.database.fake_dao import Dao

dao = Dao()
USER_DATABASE = 'user'


def get_user_info(name):
    user = dao.find_one(USER_DATABASE, {'name': name})
    if user is None:
        return {'success': True,
                'data': {}}

    return {'success': True,
            'data': user}


def update_user_info(user):
    res = dao.update_one(USER_DATABASE, {'uid': user['uid']}, user)
    if res['ok'] != 1:
        return {'success': False,
                'message': 'update fail!'}

    return {'success': True,
            'message': 'update success!'}
