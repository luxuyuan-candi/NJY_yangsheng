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
@app.route('/api/yangsheng/yaoshanbao/goods', methods=['GET'])
def get_goods_list():

    # 连接数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT id, name, cover, brief, price FROM goods WHERE status = 1 ORDER BY id DESC"
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        'code': 0,
        'data': rows
    })

@app.route('/api/yangsheng/yaoshanbao/<int:goods_id>', methods=['GET'])
def get_goods_detail(goods_id):
    # 连接数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT id, name, cover, brief, price, video, description FROM goods WHERE id=%s AND status=1"
    cursor.execute(sql, (goods_id,))
    goods = cursor.fetchone()

    if goods:
        return jsonify({"code": 0, "data": goods})
    else:
        return jsonify({"code": 1, "msg": "商品不存在"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

