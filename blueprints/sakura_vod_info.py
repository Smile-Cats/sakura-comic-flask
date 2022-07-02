from flask import Blueprint, request, jsonify, Response, url_for
import os
from comic_sakura.models import *

vod_bp = Blueprint('vod_bp', __name__)

mov_type_dict = {
    1: [1, 6, 7, 8, 9, 10, 11, 12, 20, 21, 22, 34],
    2: [2, 13, 14, 15, 16, 23, 24, 25],
    3: [3, 26, 27, 28, 29],
    4: [4, 30, 31, 32, 33, 22],
    5: [5, 17, 18],
    0: [1, 2, 3, 4, 5]
}


@vod_bp.route('/vod_list', methods=['GET'])
def get_vod_list():
    '''
    通过查询条件返回数据
    :return: json
    '''
    page = int(request.args.get('page', 1))  # 查询的页数
    mov_type = int(request.args.get('movtype', 0))  # 视频的类型, 一级类型
    mov_type_list = mov_type_dict.get(mov_type)  # 通过一级类型查询到的视频二级类型
    vod_area = request.args.get('vod_area')  # 查询参数 视频地址
    type_name = request.args.get('vod_class')  # 查询参数 视频二级类型
    vod_year = request.args.get('vod_year')  # 查询参数 视频年份
    keyword = request.args.get('keyword')  # 关键词
    # if page > 10:
    #     return jsonify([])
    # 有type_name查type_name 没有查type_id_list
    if type_name:
        movs = MovDetail.query.filter(MovDetail.type_name == type_name)
    else:
        movs = MovDetail.query.filter(MovDetail.type_id.in_(mov_type_list))

    if vod_area:
        if vod_area != 'more':
            movs = movs.filter(MovDetail.vod_area == vod_area)
        else:
            movs = movs.filter(
                MovDetail.vod_area.notin_(["中国", "内地", "美国", "日本", "韩国", "英国", "法国", "香港", "泰国"]))

    if vod_year:
        if vod_year != 'more':
            movs = movs.filter(MovDetail.vod_year == vod_year)
        else:
            movs = movs.filter(
                MovDetail.vod_year.notin_(
                    ["2023", "2022", "2021", "2020", "2019", "2018", "2017",
                     "2016", "2015", "2014", "2013", "2012", "2011", "2010"]))

    if keyword:
        movs = movs.filter(MovDetail.vod_name.like(f"%{keyword}%"))

    movs = movs.order_by(MovDetail.vod_time.desc()).paginate(page=page, per_page=12).items

    vod_list = []
    for mov in movs:
        # vod_list.append(
        #     dict(vod_id=mov.vod_id, vod_pic=url_for('vod_bp.get_img_info', img=f"{mov.vod_id}.jpg", _external=True),
        #          vod_name=mov.vod_name, vod_remarks=mov.vod_remarks))
        vod_list.append(
            dict(vod_id=mov.id, vod_pic=mov.vod_pic,
                 vod_name=mov.vod_name, vod_remarks=mov.vod_remarks))
    return jsonify(vod_list)


@vod_bp.route('/vod_detail', methods=['GET'])
def get_vod_detail():
    '''
    通过查询条件返回数据
    :return: json
    '''
    vod_id = request.args.get('vod_id', 0)
    mov = MovDetail.query.filter(MovDetail.id == vod_id).first()
    if mov:
        if mov.vod_content:
            mov.vod_content = mov.vod_content.replace('<p>', '') \
                .replace('</p>', '').replace('<span>', '').replace('</span>', '')
        if mov.vod_play_url:
            pay_url_dict = {}
            for play_url_set in mov.vod_play_url.split('#'):
                k, v = play_url_set.split('$')
                pay_url_dict[k] = v
            mov.vod_play_url = pay_url_dict
        result = dict(mov.__dict__)
        del result['_sa_instance_state']
        return jsonify(dict(code=200, data=result, msg='success'))
    else:
        return jsonify(dict(code=400, msg='failed'))


@vod_bp.route('/imgs/<img>', methods=['GET'])
def get_img_info(img):
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    filepath = os.path.join(basedir, f"static/imgs/{img}")
    if not os.path.isfile(filepath):
        filepath = os.path.join(basedir, "static/imgs/12.jpg")
    with open(filepath, 'rb') as f:
        img = f.read()
    resp = Response(img, mimetype="image/jpeg")
    return resp
