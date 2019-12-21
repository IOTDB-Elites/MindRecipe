from pymongo import MongoClient
from worker.database.constant import port, uri


class Dao:
    def __init__(self):
        self.conn = MongoClient(uri, port=port)
        self.db = self.conn.mind_recipe

    # insert into db_name, example is here
    # ```
    # DATABASE = 'your_name'
    # dao = Dao()
    # cache = []
    # count = 0
    #
    # dao.clear_database(DATABASE)
    # for row in your_data:
    #     cache.append({'month': 10,
    #                   'day': row[0],
    #                   'hour': row[1],
    #                   'lng_gcj02': row[2],
    #                   'lat_gcj02': row[3],
    #                   'value': row[4])})
    #
    #     if len(cache) == 100:
    #         count += 100
    #         dao.insert_many(DATABASE, cache)
    #         cache.clear()
    #         if count % 1000 == 0:
    #             print(count)
    # if len(cache) != 0:
    #     dao.insert_many(DATABASE, cache)
    # dao.close()
    # ```
    def insert_many(self, db_name, data_list):
        self.db[db_name].insert_many(data_list)

    # clear database
    def clear_database(self, db_name, filter=None):
        # warning need security check
        return self.db[db_name].delete_many({} if filter is None else filter)

    # read data from db_name
    def read_data(self, db_name, filter=None):
        if not filter:
            return self.db[db_name].find()
        find_res = self.db[db_name].find(filter)
        res = []
        for i in find_res:
            del i['_id']
            res.append(i)
        return res

    # read one data from db_name
    def find_one(self, db_name, filter=None):
        if not filter:
            return self.db[db_name].find_one()
        res = self.db[db_name].find_one(filter)
        del res['_id']
        return res

    def update_one(self, db_name, filter, entity):
        return self.db[db_name].update(filter, entity)

    def close(self):
        self.conn.close()


# just a example for reading data
if __name__ == '__main__':
    dao = Dao()
    count = 0
    for i in dao.read_data('user'):
        count += 1
        if count % 10000 == 0:
            print(i)

    # do not forget this
    print(count)
    dao.close()

    print("total len: ", count)
