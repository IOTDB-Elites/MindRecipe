from pymongo import MongoClient

from loader.database.constant import port


class Dao:
    def __init__(self, uri):
        self.conn = MongoClient(uri, port=port)
        self.db = self.conn.mind_recipe  ## TODO ? this line decide the database?

    def list(self):
        print(self.db[''].collection)

    def insert_many(self, db_name, data_list):
        self.db[db_name].insert_many(data_list)

    # clear database
    def clear_database(self, db_name, filter=None):
        return self.db[db_name].delete_many({} if filter is None else filter)

    # read data from db_name
    def read_data_from_target_database(self, db_name, filter=None):
        if not filter:
            return self.db[db_name].find()
        return self.db[db_name].find(filter)

    # read one data from db_name
    def find_one(self, db_name, filter=None):
        if not filter:
            return self.db[db_name].find_one()
        return self.db[db_name].find_one(filter)

    def update_one(self, db_name, filter, entity):
        return self.db[db_name].update(filter, entity)

    def close(self):
        self.conn.close()


# just a example for reading data
if __name__ == '__main__':
    # dao = Dao()
    # count = 0
    # for i in dao.read_data_from_target_database('integrated_result', {'month': 9, 'day': {'$gt': 23}}):
    #     count += 1
    #     if count % 10000 == 0:
    #         print(i)

    # do not forget this
    # print(count)

    # insert into db_name, example is here
    # ```

    print("hello 1")
    DATABASE = 'mind_recipe'
    dao = Dao('mongodb://127.0.0.1:10002/mind_recipe')

    cache = []
    count = 0

    print("hello 2")
    dao.clear_database(DATABASE)

    # for i in range(1, 100):
    #     cache.append({'id': i, 'data1': 10, 'data2': 'image'})
    #
    #     print(i)
    #
    #     if len(cache) == 100:
    #         count += 100
    #         dao.insert_many(DATABASE, cache)
    #         cache.clear()
    #         if count % 1000 == 0:
    #             print(count)
    # if len(cache) != 0:
    #    dao.insert_many(DATABASE, cache)

    print('here')
    # dao.clear_database(DATABASE)
    # print(dao.update_one('read', {'uid': '882', 'aid': '670'},
    #                {"uid": "882", "aid": "670", "readTimeLength": 50, "readSequence": "3", "readOrNot": 0,
    #                 "agreeOrNot": 0, "commentOrNot": 0, "commentDetail": "hahah", "shareOrNot": 0,
    #                 "region": "Hong Kong", "category": "science"})['ok'] == 1)
    count = 0
    for i in dao.read_data_from_target_database('read'):
        print(i)

    print(count)

    dao.close()
