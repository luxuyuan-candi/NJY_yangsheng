# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# MySQL 配置
db_config = {
    'host': 'my-mysql.default.svc.cluster.local',        # 或者 MySQL 容器 IP / service 名称
    'port': 3306,
    'user': 'root',
    'password': 'zhongyao_root',
    'database': 'yangsheng',
    'charset': 'utf8mb4'
}

# GET /api/video/list?type=gongfa
@app.route('/api/yangsheng/yangshengshiping/video/list', methods=['GET'])
def video_list():
    video_type = request.args.get('type')
    if not video_type:
        return jsonify({'code': 1, 'msg': '缺少 type 参数'}), 400

    # 连接数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT id, title, shortdesc, imagesrc, duration, level, `desc`, videosrc
        FROM video
        WHERE type=%s
        ORDER BY id ASC
    """
    cursor.execute(sql, (video_type,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': rows
    })

@app.route('/api/yangsheng/yangshengshiping/video/detail', methods=['GET'])
def video_detail():
    video_id = request.args.get('id')

    if not video_id:
        return jsonify({'code': 1, 'msg': '缺少 id 参数'}), 400

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT 
            id,
            title,
            shortdesc,
            imagesrc,
            duration,
            level,
            `desc`,
            videosrc,
            type
        FROM video
        WHERE id = %s
        LIMIT 1
    """
    cursor.execute(sql, (video_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return jsonify({'code': 1, 'msg': '视频不存在'}), 404

    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': row
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

