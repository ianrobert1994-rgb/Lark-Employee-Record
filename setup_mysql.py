import pymysql

conn = pymysql.connect(host="localhost", user="root", password="root", charset="utf8mb4")
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS lark_attendance")
cur.execute("USE lark_attendance")

cur.execute("""CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) DEFAULT '',
    english_name VARCHAR(100) DEFAULT '',
    email VARCHAR(100) DEFAULT '',
    mobile VARCHAR(50) DEFAULT '',
    department VARCHAR(100) DEFAULT '',
    department_id VARCHAR(50) DEFAULT '',
    job_title VARCHAR(100) DEFAULT '',
    employee_type VARCHAR(20) DEFAULT 'staff',
    avatar_url TEXT,
    status VARCHAR(20) DEFAULT 'active',
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS attendance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) DEFAULT '',
    employee_type VARCHAR(20) DEFAULT 'worker',
    work_date VARCHAR(20) NOT NULL,
    time_in VARCHAR(20) DEFAULT '--',
    time_out VARCHAR(20) DEFAULT '--',
    status VARCHAR(20) DEFAULT 'absent',
    photo_in TEXT,
    photo_out TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

conn.commit()
conn.close()
print("Database and tables created successfully")
