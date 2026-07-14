import pymysql
import pymysql.cursors

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "lark_attendance",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_db():
    return pymysql.connect(**DB_CONFIG)


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL DEFAULT '',
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


def insert_employees(employees):
    conn = get_db()
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO employees
            (user_id, name, english_name, email, mobile, department, department_id, job_title, employee_type, avatar_url, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name=VALUES(name), english_name=VALUES(english_name), email=VALUES(email),
            mobile=VALUES(mobile), department=VALUES(department), department_id=VALUES(department_id),
            job_title=VALUES(job_title), employee_type=VALUES(employee_type),
            avatar_url=VALUES(avatar_url), status=VALUES(status)
    """, employees)
    conn.commit()
    conn.close()


def clear_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees")
    conn.commit()
    conn.close()


def query_employees(full_name=None, department=None, employee_type=None):
    conn = get_db()
    cur = conn.cursor()
    sql = "SELECT * FROM employees WHERE 1=1"
    params = []

    if full_name:
        sql += " AND (name LIKE %s OR english_name LIKE %s)"
        params.extend([f"%{full_name}%", f"%{full_name}%"])
    if department:
        sql += " AND department = %s"
        params.append(department)
    if employee_type:
        sql += " AND employee_type = %s"
        params.append(employee_type)

    sql += " ORDER BY name ASC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_employee_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM employees")
    total = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM employees WHERE employee_type='staff'")
    staff_count = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM employees WHERE employee_type='worker'")
    worker_count = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM employees WHERE status='active'")
    active = cur.fetchone()["cnt"]
    conn.close()
    return {"total": total, "staff": staff_count, "workers": worker_count, "active": active}


def insert_records(records):
    conn = get_db()
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO attendance_records
            (employee_id, employee_name, department, employee_type, work_date, time_in, time_out, status, photo_in, photo_out)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, records)
    conn.commit()
    conn.close()


def clear_records():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM attendance_records")
    conn.commit()
    conn.close()


def clear_records_by_date(date_from, date_to):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM attendance_records WHERE work_date >= %s AND work_date <= %s", (date_from, date_to))
    conn.commit()
    conn.close()


def query_records(date_from=None, date_to=None, full_name=None, department=None, employee_type=None):
    conn = get_db()
    cur = conn.cursor()
    sql = "SELECT * FROM attendance_records WHERE 1=1"
    params = []

    if date_from:
        sql += " AND work_date >= %s"
        params.append(date_from)
    if date_to:
        sql += " AND work_date <= %s"
        params.append(date_to)
    if full_name:
        sql += " AND employee_name LIKE %s"
        params.append(f"%{full_name}%")
    if department:
        sql += " AND department = %s"
        params.append(department)
    if employee_type:
        sql += " AND employee_type = %s"
        params.append(employee_type)

    sql += " ORDER BY work_date DESC, employee_name ASC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT employee_id) as cnt FROM attendance_records")
    total = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM attendance_records WHERE status='present'")
    present = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM attendance_records WHERE status='late'")
    late = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM attendance_records WHERE status='absent'")
    absent = cur.fetchone()["cnt"]
    cur.execute("SELECT COUNT(*) as cnt FROM attendance_records WHERE status='leave'")
    leave = cur.fetchone()["cnt"]
    conn.close()
    return {"total": total, "present": present, "late": late, "absent": absent, "leave": leave}
