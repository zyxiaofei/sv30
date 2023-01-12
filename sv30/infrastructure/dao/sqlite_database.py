from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from infrastructure.config.config import Config


config = Config()
database_name = config.get_database_name().get("database_name")
engine = create_engine(
    'sqlite:///{database_name}'.format(database_name=database_name), connect_args={"check_same_thread": False},
    encoding='utf8', echo=False, echo_pool=False,
    pool_recycle=3600, pool_pre_ping=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 创建Session类实例
session = Session()

# 增
"""
add_data =[Model1,Model2]
"""


def add_db(add_data: list):
    session.add_all(add_data)
    session.commit()
    session.close()


# 查
"""
filter_data={Model.Table==value， Model.Table1==value1}
"""


def query_db(model_cls, type_data=0, filter_data=None):
    if filter_data is None:
        filter_data = {}
    if type_data == 0:
        data = session.query(model_cls).filter(*filter_data).all()
    elif type_data == 1:
        data = session.query(model_cls).filter(*filter_data).first()
    else:
        print('err,查询类型错误')
        data = None
    # session.close()
    return data


# 改
"""
update_data={Table: value}
"""


def update_db(model_cls, update_data, filter_data=None):
    if filter_data is None:
        return None
    res = session.query(model_cls).filter(*filter_data).first()

    for attr, value in res.__dict__.items():
        if attr in update_data.keys():
            setattr(res, attr, update_data[attr])
    # 确认修改
    session.commit()
    session.close()


# 删
def delete_db(model_cls, filter_data=None):
    if filter_data is None:
        filter_data = {}
    # 要删除需要先将记录查出来
    del_user = session.query(model_cls).filter(*filter_data).all()
    # 将用户记录删除
    for del_data in del_user:
        session.delete(del_data)
        # 确认删除
        session.commit()
    session.close()
