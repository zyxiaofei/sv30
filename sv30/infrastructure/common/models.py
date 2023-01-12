from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Date, Float
from infrastructure.common.uuid_code import get_uuid


Base = declarative_base()


class MeasureDataFormation(Base):
    """视频时间"""

    __tablename__ = 'measure_data_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    measure_times = Column(Integer, default=1, comment='当日当前测定次数')
    current_measure_data = Column(JSON, comment='测定值')
    last_current_measure_data = Column(Float, comment='最终测定值')
    measure_date = Column(Date, comment='测定日期')
    measure_duration = Column(Integer, default=30, comment='测定时长')
    measure_start_time = Column(DateTime(timezone=True), comment='开始时间')
    measure_end_time = Column(DateTime(timezone=True), comment='结束时间')
    measure_type = Column(Integer, default=1, comment='测定类型')  # 0 自动 1 手动
    warning_sign = Column(Integer, default=1, comment='预警报警')  # 0 异常 1 正常
    read_sign = Column(Integer, default=1, comment='已读标识')  # 0 未读 1 已读


class TimerSetting(Base):
    """定时器设置"""

    __tablename__ = 'timer_setting'
    uuid = Column(String(36), default=get_uuid, unique=True, primary_key=True, index=True, comment='唯一业务id')
    sedimentation_time = Column(Integer, default=30, comment='自定义沉淀时间')
    beginning_time = Column(String, comment='开始时间')
    ending_time = Column(String, comment='结束时间')
    enable_type = Column(Integer, default=1, comment='启用类型')  # 0 自动 1 手动


class WarningSign(Base):
    """报警设置"""
    __tablename__ = 'warning_sign'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    minimum = Column(Integer, comment='预警下限')
    maximum = Column(Integer, comment='预警上限')
