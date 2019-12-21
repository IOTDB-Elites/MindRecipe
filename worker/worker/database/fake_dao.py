# fake dao for test
class Dao:
    def insert_many(self, db_name, data_list):
        return True

    # clear database
    def clear_database(self, db_name, filter=None):
        return True

    # read data from db_name
    def read_data(self, db_name, filter=None):
        return [{}]

    # read one data from db_name
    def find_one(self, db_name, filter=None):
        return {'uid': '1', 'name': '23'}

    def update_one(self, db_name, filter, entity):
        return {'ok': 1, 'nModified': 1, 'n': 1, 'updatedExisting': True}

    def close(self):
        return True
