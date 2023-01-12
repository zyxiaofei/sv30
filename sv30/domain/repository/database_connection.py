from infrastructure.dao.sqlite_database import add_db, query_db, update_db, delete_db


def add_database(add_data: list):
    add_db(add_data)


def query_database(cls_name, type_data=0, filter_data=None):
    data = query_db(cls_name, type_data, filter_data)
    return data


def update_database(cls_name, update_data, filter_data=None):
    update_db(cls_name, update_data, filter_data)


def delete_database(cls_name, filter_data=None):
    delete_db(cls_name, filter_data)
