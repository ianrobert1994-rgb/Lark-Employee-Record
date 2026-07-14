import pymysql

for pw in ["", "root", "password", "admin"]:
    try:
        conn = pymysql.connect(host="localhost", user="root", password=pw, charset="utf8mb4")
        print(f"Connected with password: '{pw}'")
        conn.close()
        break
    except Exception as e:
        print(f"password '{pw}': {e}")
