from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import ollama
import time

app = Flask(__name__)
CORS(app)

last_request_time = {}
REQUEST_INTERVAL = 5

@app.route("/message", methods=["POST"])
def receive_message():
    user_ip = request.remote_addr
    now = time.time()

    if now - last_request_time.get(user_ip, 0) < REQUEST_INTERVAL:
        return jsonify({"error": "请 5 秒后再发送"}), 429

    last_request_time[user_ip] = now

    if not request.is_json:
        return jsonify({"error": "JSON only"}), 400

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # 数据库连接配置
    db = pymysql.connect(
        host="localhost",
        user="依据实际更改",
        password="依据实际更改",
        database="message_db",
        charset="utf8mb4"
    )

    # 安全写入数据库（参数化，防 SQL 注入）
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO messages (name, email, message, ip)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, message, user_ip))
            db.commit()
        print("新留言已写入数据库")

    except Exception as e:
        db.rollback()
        print("数据库错误：", e)
        return jsonify({"error": "server error"}), 500
    finally:
        db.close()

    return jsonify({"status": "ok"})

REQUEST_INTERVAL1 = 10  # 秒
last_request_time1 = {}  # {ip: timestamp}

def is_rate_limited(ip):
    now = time.time()
    last_time = last_request_time1.get(ip, 0)

    if now - last_time < REQUEST_INTERVAL1:
        return True, int(REQUEST_INTERVAL1 - (now - last_time))

    last_request_time1[ip] = now
    return False, 0

# ======================
# MiniQCE 接口
# ======================
@app.route("/miniqce", methods=["POST"])
def miniqce_chat():
    user_ip = request.remote_addr
    data = request.get_json(silent=True)

    if not data or "content" not in data:
        return jsonify({
            "reply": "请求格式错误。"
        })

    content = data["content"].strip()
    print(content)
    # ---- 限流判断 ----
    limited, wait_time = is_rate_limited(user_ip)
    if limited:
        return jsonify({
            "reply": f"请间隔10秒再使用哦~（还需等待 {wait_time} 秒）"
        })

    # ---- 构造 Prompt ----
    if content == "一键介绍":
        prompt = "你好哦~，你是谁呀？请尽量简单介绍一下这个网站和站长吧~"
    else:
        prompt = content

    # ---- 调用 Ollama ----
    try:
        response = ollama.chat(
            model="miniqce",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        reply_text = response["message"]["content"]

    except Exception as e:
        reply_text = f"模型调用失败：{str(e)}"

    return jsonify({
        "reply": reply_text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
