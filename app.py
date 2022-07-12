from typing import Union
import click

from flask import Flask

from comic_sakura.settings import get_config
from comic_sakura.utils.avalon_logger import logger
from comic_sakura.extensions import db, cors, scheduler
from comic_sakura.blueprints.sakura_vod_info import vod_bp
from comic_sakura.blueprints.comment import comment_bp
from comic_sakura.blueprints.auth import auth_bp
from comic_sakura.blueprints.video_collection import vd_col_bp
from comic_sakura.tasks import SakuarDataSchedule


def create_app(env: Union[str, None] = None) -> Flask:
    app = Flask(__name__)
    config = get_config(env)
    app.config.update(config)
    db.init_app(app)
    # csrf.init_app(app)
    cors.init_app(app)
    scheduler.init_app(app)
    register_scheduler_job(scheduler)  # 注册定时任务
    scheduler.start()
    app.register_blueprint(vod_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(vd_col_bp)
    register_commands(app)
    register_process_request(app)
    return app


def register_scheduler_job(scheduler):
    @scheduler.task('cron', id='job_1', day='*', hour='23', minute='59', second='01', misfire_grace_time=60)
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
        from comic_sakura.extensions import db
        from comic_sakura.tasks import SakuraData
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
