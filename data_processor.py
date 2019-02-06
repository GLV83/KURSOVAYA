from service.db_handle import *
from datetime import datetime, timedelta
import pandas as pd


def add_data(data):
    if not data.get('date'):
        return "Error!"
    dt = datetime.strptime(data.get('date'), "%Y-%m-%d")
    start_week = (dt - timedelta(days=dt.weekday()))
    record = Record.select().where(Record.start_week == start_week)
    if record.count() == 0:
        Record.create(start_week=start_week)
        record = Record.select().where(Record.start_week == start_week)
    record = record.get()
    for i in [data.get('cfo'), data.get('csm')]:
        for j in i:
            if len(i.get(j)):
                record.__dict__['__data__'][j] = i.get(j)
    record.save()
    return "Success!"


def get_data_frame(data):
    start_week, end_week = None, None

    if data.get('start_date') is not None and len(data.get('start_date')) != 0:
        st_dt = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        start_week = st_dt - timedelta(days=st_dt.weekday())

    if data.get('end_date') is not None and len(data.get('end_date')) != 0:
        en_dt = datetime.strptime(data.get('end_date'), "%Y-%m-%d")
        end_week = en_dt - timedelta(days=en_dt.weekday())

    records = Record.select().where(
        (True if start_week is None else Record.start_week >= start_week) &
        (True if end_week is None else Record.start_week <= end_week)).order_by(Record.start_week).dicts()

    return pd.DataFrame(list(records))
