import os
import pandas as pd
import random
from datetime import datetime
from constants import *


def save_report(df: pd.DataFrame):
    filename = '{0}/fs/reports/{1}'.format(os.getcwd(),
                                           'report-{0}.csv'.format(datetime.now().strftime('%Y-%m-%d-%H.%M.%S')))
    filename = os.path.normpath(filename)
    df.drop(['created', 'updated'], axis=1, inplace=True)
    df.rename(columns=GRAPTH_TYPES, inplace=True)
    df.rename(columns={'start_week': 'Начало недели'}, inplace=True)
    df.to_csv(filename, sep=';', encoding='windows-1251', index=False)
    return filename.split('\\')[-1]


def save_plot(fig):
    filename = '{0}/fs/grapths/{1}'.format(os.getcwd(),
                                           'grapth-{0}.png'.format(random.randint(0, 99999999999)))
    filename = os.path.normpath(filename)
    fig.savefig(filename)
    return filename.split('\\')[-1]


def get_url(type: str, filename: str):
    return '/file/{0}/{1}'.format(type, filename)


for fs_dir in ['grapths', 'reports']:
    fs_dir = '{0}/fs/{1}/'.format(os.getcwd(), fs_dir)
    for file in os.listdir(fs_dir):
        file_path = os.path.join(fs_dir, file)
        os.unlink(file_path)

