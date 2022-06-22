import logging
import os
import requests
import pymysql
import datetime
import pandas as pd
from sqlalchemy import create_engine
from settings import get_config

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()
pymysql.install_as_MySQLdb()


class DownLoadImgs:
    def __init__(self):
        self._sql_conn = None

    @property
    def sql_conn(self):
        if self._sql_conn is None:
            config = get_config("PRODUCTION")
            self._sql_conn = create_engine(config['SQLALCHEMY_DATABASE_URI'])
        return self._sql_conn

    def get_vod_img_url(self):
        sql = "SELECT distinct vod_id,  vod_name,  vod_pic FROM sakura_movdetail"
        data = pd.read_sql_query(sql, self.sql_conn)
        return data

    def save_img(self, img_content, file_name):
        with open(f'./static/imgs/{file_name}.jpg', 'wb') as f:
            f.write(img_content)

    def save_failed_info(self, info: dict):
        file_name = datetime.datetime.now().strftime("%Y%m%d")
        with open(f'./failed-{file_name}.txt', 'a', encoding='utf-8') as f:
            f.write(f"{info['vod_id']} {info['vod_url']} \n")

    def download_img(self, url, file_name):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.save_img(response.content, file_name)
                logger.info(f'Success: {file_name} - {url}')
            else:
                self.save_failed_info(dict(vod_id=file_name, vod_url=url))
                logger.info(f'Failed: {file_name} - {url}')
        except:
            self.save_failed_info(dict(vod_id=file_name, vod_url=url))
            logger.info(f'Failed: {file_name} - {url}')


    def run(self):
        # data = pd.read_csv('./imgs_url.csv')
        data = d.get_vod_img_url()
        my_imgs = list(file.split('.')[0] for file in os.listdir('./static/imgs'))
        print(my_imgs)
        infos = data.loc[:, ['vod_id', 'vod_pic']].to_dict(orient='records')
        for info in infos:
            if str(info['vod_id']) in my_imgs:
                logger.info(f"fliter: {info['vod_id']}")
            else:
                self.download_img(info['vod_pic'], info['vod_id'])



if __name__ == '__main__':
    d = DownLoadImgs()
    d.run()
    # data = d.get_vod_img_url()
    # data.to_csv('./imgs_url.csv')
