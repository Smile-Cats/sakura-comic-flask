import atexit
import click
import logging
import logging.config
import os
import platform
from typing import Union

from flask import Flask

from app.settings import get_config, get_logging_config
from app.utils.avalon_logger import logger
from app.extensions import db, cors, scheduler
from app.blueprints.sakura_vod_info import vod_bp
from app.blueprints.comment import comment_bp
from app.blueprints.auth import auth_bp
from app.blueprints.video_collection import vd_col_bp
from app.task.tasks import SakuarDataSchedule


def create_app(env: Union[str, None] = None) -> Flask:
    app = Flask(__name__)
    config = get_config(env)
    app.config.update(config)
    if not os.path.exists(app.config['LOGGING_PATH']):
        # 日志文件目录
        os.mkdir(app.config['LOGGING_PATH'])
    logging.config.dictConfig(get_logging_config())  # 载入日志配置
    db.init_app(app)
    # csrf.init_app(app)
    cors.init_app(app)
    __scheduler_init(app, scheduler)  # 初始化scheduler 加文件锁 防止多进程下任务重复启动
    app.register_blueprint(vod_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(vd_col_bp)
    register_commands(app)
    register_process_request(app)
    return app


def __scheduler_init(app, scheduler):

    if platform.system() != 'Windows':
        # Linux 环境下
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            register_scheduler_job(scheduler)
            scheduler.start()
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        # Window 环境下
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(app)
            register_scheduler_job(scheduler)
            scheduler.start()
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)


def register_scheduler_job(scheduler):
    @scheduler.task('cron', id='job_1', day='*', hour='10', minute='47', second='01', misfire_grace_time=60)
    def scheduler_update_sakura():
        #  注册 定时任务
        logger.info('Start Update Sakura Data')
        sd = SakuarDataSchedule()
        with scheduler.app.app_context():
            sd.get_sakura_data()
        logger.info('Finish Update Sakura Data')


def register_process_request(app):
    @app.after_request
    def handler_after_request(response):
        # response.headers['Access-Control-Allow-Origin'] = "*"  # 设置允许跨域
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        return response


def register_commands(app):
    @app.cli.command()
    def init_db():
        from extensions import db
        from task.tasks import SakuraData
        click.echo('Createing Databases')
        db.drop_all()
        db.create_all()
        # sk = SakuraData()
        # click.echo('Catching mov_type')
        # sk.insert_mov_type()
        # click.echo('Catching mov_info')
        # sk.crawl_mov_info_all()
        # click.echo('Catching mov_detail')
        # sk.crawl_mov_detail_all()

    @app.cli.command()
    def update_sakura_data():
        from comic_sakura.tasks import SakuarDataSchedule
        click.echo('Updateing Sakura Data')
        sd = SakuarDataSchedule()
        sd.get_sakura_data()


if __name__ == '__main__':
    app = create_app(env='PRODUCTION')
    app.run(host='0.0.0.0', debug=False)
