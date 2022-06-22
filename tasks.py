import json
import time

import requests
from comic_sakura.extensions import db
from comic_sakura.utils import logger
from comic_sakura.models import MovType, MovInfo, MovDetail


class SakuraData:
    def __init__(self):
        self.total_page = None
        self.mov_type = None
        self.sakura_list = 'https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=list&pg={page}'
        self.sakura_detail = 'https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=detail&pg={page}'
        self.__init_sakura__()

    def __init_sakura__(self):
        url = self.sakura_list.format(page=1)
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            if self.mov_type is None:
                self.mov_type = data['class']
            if self.total_page is None:
                total = int(data['total'])
                limit_per_page = int(data['limit'])
                self.total_page = (total // limit_per_page) + 1 if total % limit_per_page else total // limit_per_page
        else:
            raise Exception(f"初始化失败: 无法获取数据")

    def insert_mov_type(self):
        db.session.bulk_insert_mappings(
            MovType,
            self.mov_type
        )
        db.session.commit()
        logger.info(f'保存视频类型进入数据库')

    def get_mov_info(self, page=1):
        # 读取url数据并保存到数据库
        url = self.sakura_list.format(page=page)
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            mov_info_list = data['list']
            db.session.bulk_insert_mappings(
                MovInfo,
                mov_info_list
            )
            db.session.commit()
            logger.info(f'mov_list page {page} catched')
        else:
            logger.debug(f"抓取数据失败, code: {response.status_code}")


    def get_mov_detail(self, page=1):
        '''
        抓取 mov detail
        :param page: 页码
        :return:
        '''
        url = self.sakura_detail.format(page=page)
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            mov_detail_list = data['list']
            db.session.bulk_insert_mappings(
                MovDetail,
                mov_detail_list
            )
            db.session.commit()
            logger.info(f'mov_detail page {page} catched')
        else:
            logger.debug(f"抓取数据失败, code: {response.status_code}")

    def crawl_mov_info_all(self):
        for page in range(self.total_page):
            self.get_mov_info(page)

    def crawl_mov_detail_all(self):
        for page in range(self.total_page):
            self.get_mov_detail(page)
