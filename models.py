import datetime

from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy.dialects.mysql import LONGTEXT
from flask import current_app


class MovType(db.Model):
    __tablename__ = 'sakura_movtype'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(20), nullable=False)
    this_type_movies = db.relationship('MovInfo', back_populates='this_mov_type')
    this_type_movie_details = db.relationship('MovDetail', back_populates='this_mov_type')


class MovInfo(db.Model):
    __tablename__ = 'sakura_movinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('sakura_movtype.type_id'))  # 一对多关系,ForeignKey在多侧
    type_name = db.Column(db.String(20), nullable=False)
    vod_en = db.Column(db.Text, nullable=False)
    vod_id = db.Column(db.Integer, primary_key=True)
    vod_name = db.Column(db.Text, nullable=False)
    vod_play_from = db.Column(db.Text)
    vod_remarks = db.Column(db.Text)
    vod_time = db.Column(db.DateTime)
    this_mov_type = db.relationship('MovType', back_populates='this_type_movies')


class MovDetail(db.Model):
    __tablename__ = 'sakura_movdetail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer, db.ForeignKey('sakura_movtype.type_id'))  # 一对多,设置外键
    type_id_1 = db.Column(db.Integer)
    type_name = db.Column(db.String(20))
    vod_actor = db.Column(db.Text)
    vod_area = db.Column(db.Text)
    vod_author = db.Column(db.Text)
    vod_behind = db.Column(db.Text)
    vod_blurb = db.Column(db.Text)
    vod_class = db.Column(db.Text)
    vod_color = db.Column(db.Text)
    vod_content = db.Column(db.Text)
    vod_copyright = db.Column(db.Integer)
    vod_director = db.Column(db.Text)
    vod_douban_id = db.Column(db.Integer)
    vod_douban_score = db.Column(db.String(20))
    vod_down = db.Column(db.Integer)
    vod_down_from = db.Column(db.Text)
    vod_down_note = db.Column(db.Text)
    vod_down_server = db.Column(db.Text)
    vod_down_url = db.Column(db.Text)
    vod_duration = db.Column(db.Text)
    vod_en = db.Column(db.Text)
    vod_hits = db.Column(db.Integer)
    vod_hits_day = db.Column(db.Integer)
    vod_hits_month = db.Column(db.Integer)
    vod_hits_week = db.Column(db.Integer)
    vod_id = db.Column(db.Integer, primary_key=True)
    vod_isend = db.Column(db.Integer)
    vod_jumpurl = db.Column(db.Text)
    vod_lang = db.Column(db.Text)
    vod_letter = db.Column(db.Text)
    vod_level = db.Column(db.Integer)
    vod_lock = db.Column(db.Integer)
    vod_name = db.Column(db.Text)
    vod_pic = db.Column(db.Text)
    vod_pic_screenshot = db.Column(db.Text)
    vod_pic_slide = db.Column(db.Text)
    vod_pic_thumb = db.Column(db.Text)
    vod_play_from = db.Column(db.Text)
    vod_play_note = db.Column(db.Text)
    vod_play_server = db.Column(db.Text)
    vod_play_url = db.Column(LONGTEXT)
    vod_plot = db.Column(db.Integer)
    vod_plot_detail = db.Column(db.Text)
    vod_plot_name = db.Column(db.Text)
    vod_points = db.Column(db.Integer)
    vod_points_down = db.Column(db.Integer)
    vod_points_play = db.Column(db.Integer)
    vod_pubdate = db.Column(db.Text)
    vod_pwd = db.Column(db.Text)
    vod_pwd_down = db.Column(db.Text)
    vod_pwd_down_url = db.Column(db.Text)
    vod_pwd_play = db.Column(db.Text)
    vod_pwd_play_url = db.Column(db.Text)
    vod_pwd_url = db.Column(db.Text)
    vod_rel_art = db.Column(db.Text)
    vod_rel_vod = db.Column(db.Text)
    vod_remarks = db.Column(db.Text)
    vod_reurl = db.Column(db.Text)
    vod_score = db.Column(db.Text)
    vod_score_all = db.Column(db.Integer)
    vod_score_num = db.Column(db.Integer)
    vod_serial = db.Column(db.Text)
    vod_state = db.Column(db.Text)
    vod_status = db.Column(db.Integer)
    vod_sub = db.Column(db.Text)
    vod_tag = db.Column(db.Text)
    vod_time = db.Column(db.DateTime)
    vod_time_add = db.Column(db.Integer)
    vod_time_hits = db.Column(db.Integer)
    vod_time_make = db.Column(db.Integer)
    vod_total = db.Column(db.Integer)
    vod_tpl = db.Column(db.Text)
    vod_tpl_down = db.Column(db.Text)
    vod_tpl_play = db.Column(db.Text)
    vod_trysee = db.Column(db.Integer)
    vod_tv = db.Column(db.Text)
    vod_up = db.Column(db.Integer)
    vod_version = db.Column(db.Text)
    vod_weekday = db.Column(db.Text)
    vod_writer = db.Column(db.Text)
    vod_year = db.Column(db.Text)
    this_mov_type = db.relationship('MovType', back_populates='this_type_movie_details')
    comments = db.relationship('Comment', back_populates='mov_detail', cascade='all, delete-orphan')


class User(db.Model):
    __tablename__ = 'sakura_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))

    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')  # 用户信息被删除后 评论也一起被删除
    collections = db.relationship('UserCollection', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        # 生成hash后的密码
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        # 将hash密码和密码进行比对
        return check_password_hash(self.password_hash, password)


class Comment(db.Model):
    __tablename__ = 'sakura_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    reviewed = db.Column(db.Boolean, default=True)  # 该评论是否通过审核
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('sakura_user.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('sakura_comment.id'))  # 将replied_id定义为外键
    movdetail_id = db.Column(db.Integer, db.ForeignKey('sakura_movdetail.id'))

    user = db.relationship('User', back_populates='comments')
    mov_detail = db.relationship('MovDetail', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')  # 父评论，对应一,父评论被删除子评论也会删除
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])  # 子评论，对应多，remote_side参数指定了自己代表多


class UserCollection(db.Model):
    __tablename__ = 'sakura_user_collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sakura_user.id'))
    movdetail_id_list = db.Column(LONGTEXT)

    user = db.relationship('User', back_populates='collections')
