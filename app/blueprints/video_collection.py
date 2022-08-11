from flask import Blueprint, request, jsonify, Response, url_for
from ..extensions import db
from ..extensions import auth
from ..models.models import *

vd_col_bp = Blueprint('vd_col_bp', __name__)


@vd_col_bp.route('/collection/show', methods=['GET'])
@auth.login_required
def show_collect_video():
    '''
    返回该用户的所有收藏视频
    :return:
    '''
    user_id = request.args.get('user_id')
    page = int(request.args.get('page', 1))
    user_collection = UserCollection.query.filter_by(user_id=user_id).first()
    collect_vod_list = []
    if user_collection:
        store_vod_list = user_collection.movdetail_id_list.split(';')[:-1]
        collect_movs = MovDetail.query.filter(MovDetail.id.in_(store_vod_list)).\
            order_by(MovDetail.vod_time.desc()).\
            paginate(page=page, per_page=12).items

        for mov in collect_movs:
            collect_vod_list.append(
                dict(vod_id=mov.id, vod_pic=mov.vod_pic,
                     vod_name=mov.vod_name, vod_remarks=mov.vod_remarks))
    return jsonify(data={
            'code': 200,
            'message': '收藏的视频信息',
            'data': collect_vod_list
        })


@vd_col_bp.route('/collection/is_collection', methods=['GET'])
@auth.login_required
def show_is_collect_video():
    '''
    返回该视频是否被收藏
    :return:
    '''
    user_id = request.args.get('user_id')
    vod_id = request.args.get('vod_id')
    user_collection = UserCollection.query.filter_by(user_id=user_id).first()
    if user_collection:
        if vod_id in user_collection.movdetail_id_list:
            return jsonify(data={
                'code': 200,
                'message': '该视频已被收藏',
                'data': 1
            })
    return jsonify(data={
            'code': 200,
            'message': '该视频未被收藏',
            'data': 0
        })


@vd_col_bp.route('/collection/add', methods=['GET'])
@auth.login_required
def add_collect_video():
    '''
    添加收藏视频
    :return:
    '''
    user_id = request.args.get('user_id')
    vod_id = request.args.get('vod_id')
    if user_id and vod_id:
        user_collection = UserCollection.query.filter_by(user_id=user_id).first()
        store_vod_list = [vod_id]
        # 如果有收藏信息则更新 没有则添加
        if user_collection:
            store_vod_list.extend(user_collection.movdetail_id_list.split(';'))
            if vod_id + ';' not in user_collection.movdetail_id_list:
                try:
                    user_collection.movdetail_id_list = user_collection.movdetail_id_list + vod_id + ';'
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise e
        else:
            try:
                user_collection = UserCollection(user_id=user_id, movdetail_id_list=vod_id+';')
                db.session.add(user_collection)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        return jsonify(data={
            'code': 200,
            'message': '视频收藏成功',
            'data': list(set(store_vod_list))
        })
    else:
        return jsonify(data={
            'code': 400,
            'message': '没有要收藏的视频信息'
        })


@vd_col_bp.route('/collection/remove', methods=['GET'])
@auth.login_required
def remove_collect_video():
    '''
    删除要收藏的视频信息
    :return:
    '''
    user_id = request.args.get('user_id')
    vod_id = request.args.get('vod_id')
    if user_id and vod_id:
        user_collection = UserCollection.query.filter_by(user_id=user_id).first()
        store_vod_list = []
        # 如果有收藏信息则更新 没有则返回400
        if user_collection:
            try:
                user_collection.movdetail_id_list = user_collection.movdetail_id_list.replace(vod_id+';', '')
                store_vod_list.extend(user_collection.movdetail_id_list.split(';'))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

            return jsonify(data={
                'code': 200,
                'message': '视频删除收藏成功',
                'data': list(set(store_vod_list))
            })

    return jsonify(data={
            'code': 400,
            'message': '没有要删除收藏的视频信息'
        })


