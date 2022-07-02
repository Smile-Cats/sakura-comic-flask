from flask import Blueprint, request, jsonify, Response, url_for
from typing import List
from comic_sakura.extensions import auth
from comic_sakura.models import *


comment_bp = Blueprint('comment_bp', __name__)


@comment_bp.route('/show/comment/<int:vod_id>')
def show_comments(vod_id):
    '''
    展示评论信息
    :param vod_id:
    :return:
    '''
    def get_all_replies(reply_comments: List[Comment], result: List):
        for comment in reply_comments:
            reply = dict(user_name=comment.user.name, id=comment.id,
                         reply_user_name=comment.replied.user.name,
                         body=comment.body, time=comment.timestamp.strftime('%Y-%m-%d'))
            result.append(reply)
            if comment.replies:
                get_all_replies(comment.replies, result)

    comments = Comment.query.filter(Comment.movdetail_id == vod_id).order_by(Comment.timestamp.desc())
    comment_list = []
    for comment in comments:
        c = dict(user_name=comment.user.name, body=comment.body,
                 time=comment.timestamp.strftime('%Y-%m-%d'), id=comment.id)
        reply_list = []
        get_all_replies(comment.replies, reply_list)
        c['reply_list'] = reply_list
        comment_list.append(c)
    return jsonify(data={
        'code': 200,
        'data': comment_list,
        'message': '评论获取成功'
    })


@comment_bp.route('/publish/comment/<int:vod_id>', methods=['POST'])
@auth.login_required
def post_comments(vod_id):
    '''
    发表评论
    :param vod_id:
    :return:
    '''
    json_data = request.json
    if not json_data:
        return jsonify(data={
            'code': 400,
            'message': '请输入评论内容'
        })
    body = json_data.get('body', None)
    user_id = json_data.get('user_id', None)
    if body and user_id:
        try:
            comment = Comment(body=body, user_id=user_id, movdetail_id=vod_id)
            db.session.add(comment)
            db.session.commit()
            return jsonify(data={
                'code': 200,
                'message': '评论发布成功'
            })
        except Exception as e:
            db.session.rollback()
            raise e
    return jsonify(data={
        'code': 400,
        'message': '请输入评论内容'
    })


@comment_bp.route('/reply/comment/<int:comment_id>', methods=['POST'])
@auth.login_required
def reply_comment(comment_id):
    '''
    回复评论
    :param comment_id:
    :return:
    '''
    comment = Comment.query.get(comment_id)
    if comment:
        json_data = request.json
        body = json_data.get('body', None)
        user_id = json_data.get('user_id', None)
        try:
            r_comment = Comment(body=body, user_id=user_id, replied_id=comment_id)
            db.session.add(r_comment)
            db.session.commit()
            return jsonify(data={
                'code': 200,
                'message': '评论回复成功'
            })
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        return jsonify(data={
            'code': 400,
            'message': '此评论已不存在'
        })

