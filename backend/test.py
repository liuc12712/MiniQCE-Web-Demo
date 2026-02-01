import pymysql

conn = pymysql.connect(
    host="localhost",
    user="依据实际更改",
    password="依据实际更改",
    database="message_db",
    charset="utf8mb4"
)

cursor = conn.cursor()

cursor.execute("SELECT 1")
print("数据库连接成功")

conn.close()

