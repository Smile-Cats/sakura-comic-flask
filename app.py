from typing import Union
import click

from flask import Flask

from comic_sakura.settings import get_config
from comic_sakura.extensions import db, csrf, cors
from comic_sakura.blueprints.sakura_vod_info import vod_bp


def create_app(env: Union[str, None] = None) -> Flask:
    app = Flask(__name__)
    config = get_config(env)
    app.config.update(config)
    db.init_app(app)
    csrf.init_app(app)
    cors.init_app(app)
    app.register_blueprint(vod_bp)
    register_commands(app)
    return app


def register_commands(app):
    @app.cli.command()
    def init_db():
        from comic_sakura.extensions import db
        from comic_sakura.tasks import SakuraData
        click.echo('Createing Databases')
        db.drop_all()
        db.create_all()
        sk = SakuraData()
        click.echo('Catching mov_type')
        sk.insert_mov_type()
        click.echo('Catching mov_info')
        sk.crawl_mov_info_all()
        click.echo('Catching mov_detail')
        sk.crawl_mov_detail_all()


if __name__ == '__main__':
    app = create_app(env='PRODUCTION')
    app.run(debug=True)