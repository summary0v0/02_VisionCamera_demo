import datetime

import requests
from PyQt5.QtCore import Qt
import pymysql
from typing import Optional, List, Dict
import hashlib
from datetime import datetime

# from utils import get_scale_and_id_by_url
from common.utils import get_scale_and_id_by_url
# 数据库连接配置
config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",         # MySQL用户名
    "password": "123456",      # MySQL密码
    "database": "stone_db", # MySQL数据库名称
    "charset": "utf8mb4"
}

# 【进入加工前的扫描枪】更新scale_url、operator_user_id、cutting_status和cutting_start_time；查询processing_type和thickness
def process_stone_item_from_url(url, operator_user_id = 1):
    try:
        # 1. 请求 URL 获取数据
        data = get_scale_and_id_by_url(url)
        composite_id = data.get("composite_id")
        scale_url = data.get("scale_url")

        # 2. 数据库操作
        conn = pymysql.connect(**config)
        with conn.cursor() as cursor:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 合并更新 scale_url, cutting_start_time, cutting_status, operator_user_id
            sql = """
                UPDATE stone_items
                SET scale_url=%s,
                    cutting_start_time=%s,
                    cutting_status=1,
                    operator_user_id=%s
                WHERE composite_identifier=%s
            """
            cursor.execute(sql, (scale_url, now, operator_user_id, composite_id))

            # 查询 processing_type 和 thickness
            sql_select = "SELECT processing_type, thickness FROM stone_items WHERE composite_identifier=%s"
            cursor.execute(sql_select, (composite_id,))
            result = cursor.fetchone()
            if result:
                processing_type, thickness = result
            else:
                processing_type, thickness = None, None

            conn.commit()
        conn.close()

        return composite_id, scale_url, processing_type, thickness

    except Exception as e:
        print(f"[错误] process_stone_item_from_url 出现异常: {e}")
        return None, None, None, None

# 【进入分拣机前的扫描枪】根据ID拿到箱号
def get_box_number_by_composite(composite_identifier: str):
    """根据 composite_identifier 查询 box_number"""
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT box_number FROM stone_items WHERE composite_identifier=%s"
            cursor.execute(sql, (composite_identifier,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
    finally:
        conn.close()

# 【进入分拣机前的扫描枪】更新石材状态
def update_cutting_status(composite_identifier: str, status: int = 2):
    """更新 cutting_end_time 和 cutting_status"""
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = """
                UPDATE stone_items
                SET cutting_end_time=%s, cutting_status=%s
                WHERE composite_identifier=%s
            """
            cursor.execute(sql, (now_str, status, composite_identifier))
            conn.commit()
    finally:
        conn.close()

# 【扫描数据】根据时间范围查询扫描数据
def query_stone_measurements(start_time: str, end_time: str):
    """
    根据时间范围查询石材的设计尺寸、扫描尺寸及图片信息

    :param start_time: 查询开始时间 (格式: 'YYYY-MM-DD HH:MM:SS')
    :param end_time:   查询结束时间 (格式: 'YYYY-MM-DD HH:MM:SS')
    :return:           查询结果的字典列表
    """
    sql = """
        SELECT 
            si.production_order_number AS production_order_number,
            si.number_prefix AS number_prefix,
            si.number AS number,
            si.length AS design_length,
            si.width AS design_width,
            sm.scan_length AS scan_length,
            sm.scan_width AS scan_width,
            sm.original_url AS original_url,
            sm.created_at AS scan_time
        FROM stone_items si
        JOIN stone_measurements sm 
            ON si.composite_identifier = sm.composite_identifier
        WHERE sm.created_at BETWEEN %s AND %s
        ORDER BY sm.created_at ASC
    """

    conn = pymysql.connect(**config)
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (start_time, end_time))
            results = cursor.fetchall()
        return results
    finally:
        conn.close()

# 【切割数据】时间范围查询切割数据
def get_cutting_records(start_date: str, end_date: str) -> List[Dict]:
    """
    查询指定时间范围内的切割记录，切割时间不为空。

    :param start_date: 起始时间字符串，格式 'YYYY-MM-DD'
    :param end_date: 结束时间字符串，格式 'YYYY-MM-DD'
    :return: 列表，每条字典包含操作人员中文名、所属项目、尺寸、切割米数、状态、切割时间、图号、箱号等信息
    """
    sql = """
    SELECT
        u.fullname AS operator_fullname,
        v.project_name,
        v.length,
        v.width,
        v.thickness,
        v.cutting_meters,
        v.square_area,
        CASE v.cutting_status
            WHEN -1 THEN '异常'
            WHEN 0 THEN '待切割'
            WHEN 1 THEN '切割中'
            WHEN 2 THEN '已完成'
            ELSE '未知'
        END AS cutting_status,
        v.cutting_end_time AS cutting_time,
        v.drawing_page AS drawing_number,
        v.box_number
    FROM v_complete_stone_info v
    LEFT JOIN users u ON v.operator_user_id = u.id
    WHERE v.cutting_end_time IS NOT NULL
      AND v.cutting_end_time BETWEEN %s AND %s
    ORDER BY v.cutting_end_time;
    """

    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (start_date, end_date))
            return cursor.fetchall()
    finally:
        connection.close()

# 【扫描数据页面】原始图片和量尺图片URL
import pymysql

# 主要功能是根据一个复合标识符（composite_identifier）连接到 MySQL 数据库，查询并返回与该标识符相关的量尺图片 URL 和原始图片 URL。
def query_image_urls(composite_identifier):
    """
    根据 composite_identifier 查询量尺图片和原始图片 URL
    返回字典：{"scale_url": ..., "original_url": ...}
    """
    config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "111",
        "database": "stone_db",
        "charset": "utf8mb4"
    }

    sql = """
    SELECT si.scale_url, sm.original_url
    FROM stone_items si
    LEFT JOIN stone_measurements sm
        ON si.composite_identifier = sm.composite_identifier
    WHERE si.composite_identifier = %s
    """

    result = None
    try:
        conn = pymysql.connect(**config)
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (composite_identifier,))
            result = cursor.fetchone()  # 返回字典
    except Exception as e:
        print(f"查询出错: {e}")
    finally:
        if conn:
            conn.close()

    return result

# 【扫描数据页面】时间范围查询扫描数据
# stone_measurements (sm): 存储扫描测量的原始数据（如扫描图 URL、创建时间、扫描长宽）
# stone_items (si): 存储与测量数据相关的物品信息（如实际长宽、生产订单号、编号前缀和编号）
def query_measurements(start_date, end_date):
    # SQL 时间范围查询语句
    sql = """
    SELECT 
        sm.original_url,
        sm.created_at,
        sm.scan_length,
        sm.scan_width,
        si.length, 
        si.width,
        si.production_order_number,
        si.number_prefix,
        si.number
    FROM stone_measurements sm
    JOIN stone_items si 
        ON sm.composite_identifier = si.composite_identifier   #
    WHERE sm.created_at BETWEEN %s AND %s;
    """

    # 建立连接
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (start_date, end_date))
            results = cursor.fetchall()
            return results
    finally:
        connection.close()

# 【扫描数据页面】查询当天扫描数量和总扫描数量
def get_scan_counts():
    sql = """
    SELECT 
        COUNT(CASE WHEN DATE(created_at) = CURDATE() THEN 1 END) AS today_count,
        COUNT(*) AS total_count
    FROM stone_measurements;
    """
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchone()
    finally:
        connection.close()

# 【扫描数据页面】查询当天扫描面积和总扫描面积
def get_scan_areas():
    sql = """
    SELECT
        ROUND(SUM(CASE WHEN DATE(created_at) = CURDATE() 
                       THEN (scan_length * scan_width) / 1000000 END), 2) AS today_area,
        ROUND(SUM((scan_length * scan_width) / 1000000), 2) AS total_area
    FROM stone_measurements;
    """
    connection = pymysql.connect(**config)
    try:
        # 返回值为一个字典
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)                # 在数据库中执行前面定义的 SQL 查询语句
            # fetchone() 方法获取这一行结果并将其返回
            return cursor.fetchone()           #  若没有数据或某个聚合结果为 NULL，对应字典值可能为 None，调用处需做好空值处理。
    finally:
        connection.close()

# 【切割数据页面】 时间范围查询切割数据
def query_cutting_records(start_time, end_time):
    sql = """
    SELECT 
        si.cutting_start_time,
        u.username AS operator_username,
        si.length,
        si.width,
        si.thickness,
        sid.cutting_meters,
        si.square_area,
        si.cutting_status,
        po.project_name,
        si.box_number,
        si.drawing_page
    FROM stone_items si
    LEFT JOIN users u 
        ON si.operator_user_id = u.id
    LEFT JOIN stone_item_details sid
        ON si.composite_identifier = sid.composite_identifier
    LEFT JOIN production_orders po
        ON si.production_order_number = po.production_order_number
    WHERE si.cutting_start_time BETWEEN %s AND %s
      AND si.cutting_end_time IS NOT NULL;
    """
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (start_time, end_time))
            return cursor.fetchall()
    finally:
        connection.close()

# 【缺陷检测数据页面】查询最新的切割数据
def get_latest_defect_info():
    sql = """
    SELECT 
        si.number_prefix,
        si.number,
        sps.total_defects,
        sps.missing_corners,
        sps.stains,
        sps.cracks
    FROM stone_processing_status sps
    JOIN stone_items si
        ON sps.composite_identifier = si.composite_identifier
    WHERE sps.id IN (
        SELECT MAX(id)
        FROM stone_processing_status
        GROUP BY composite_identifier
    )
    ORDER BY sps.created_at DESC;
    """
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()

# 【用户信息页面】删除用户信息
def delete_user(target_username: str, current_user_role: str):
    connection = pymysql.connect(**config)  # 不改 config
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # 这里指定
            cursor.execute("SELECT role FROM users WHERE username=%s", (target_username,))
            result = cursor.fetchone()
            if not result:
                return False, f"用户 {target_username} 不存在"
            target_role = result["role"]

            # 权限判断
            if current_user_role == "superadmin":
                if target_role not in ("admin", "productor", "undefined"):
                    return False, "superadmin 不能删除同级或更高级别用户"
            elif current_user_role == "admin":
                if target_role not in ("productor", "undefined"):
                    return False, "admin 不能删除同级或更高级别用户"
            else:
                return False, "权限不足"

            # 删除用户
            cursor.execute("DELETE FROM users WHERE username=%s", (target_username,))
            connection.commit()
            return True, f"用户 {target_username} 已删除"
    finally:
        connection.close()

# 【用户信息页面】查询用户信息（除了密码）
def get_all_users():
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 查询除 password_hash 外的所有字段，包括 fullname
            cursor.execute("""
                SELECT username, fullname, role, created_at, updated_at, lastLogin_at
                FROM users
            """)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


# 【用户信息页面】更新用户信息（增加修改 fullname）
def update_user(target_username: str, current_user_role: str,
                new_password_hash: Optional[str] = None,
                new_role: Optional[str] = None,
                new_fullname: Optional[str] = None):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT role, fullname FROM users WHERE username=%s", (target_username,))
            result = cursor.fetchone()
            if not result:
                return False, f"用户 {target_username} 不存在"
            target_role = result["role"]
            target_fullname = result["fullname"]

            # 权限判断
            if current_user_role == "superadmin":
                if target_role == "superadmin":
                    return False, "superadmin 不能修改同级或更高级别用户"
            elif current_user_role == "admin":
                if target_role in ("admin", "superadmin"):
                    return False, "权限不足，无法修改该用户"
            else:
                return False, "权限不足"

            # 构建 SQL 动态更新
            updates = []
            params = []
            log_parts = []

            if new_password_hash:
                updates.append("password_hash=%s")
                params.append(new_password_hash)
                log_parts.append("密码已修改")

            if new_role:
                if new_role not in ("admin", "productor", "undefined"):
                    return False, "输入权限值错误，只能修改为admin/productor/undefined其中之一"
                updates.append("role=%s")
                params.append(new_role)
                log_parts.append(f"权限：{target_role} → {new_role}")

            if new_fullname:
                updates.append("fullname=%s")
                params.append(new_fullname)
                log_parts.append(f"姓名：{target_fullname} → {new_fullname}")

            if not updates:
                return False, "没有要修改的字段"

            sql = f"UPDATE users SET {', '.join(updates)} WHERE username=%s"
            params.append(target_username)
            cursor.execute(sql, params)
            connection.commit()

            log_msg = "、".join(log_parts)
            return True, f"用户更新{target_username}成功", f"用户 {target_username} 信息更新成功，修改了：{log_msg}"
    finally:
        connection.close()


# 【登录页面】
# TODO 密码可加密也可不加密
def hash_password(password: str):
    # return hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password

# 【登录页面】登录验证
def check_login(username, password):
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            # 查询用户密码和角色
            sql = "SELECT password_hash, role FROM users WHERE username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                stored_hash, role = result
                if stored_hash == hash_password(password):
                    if role == 'undefined':
                        return 0
                    # 密码正确，更新最后登录时间
                    cursor.execute(
                        "UPDATE users SET lastLogin_at=%s WHERE username=%s",
                        (datetime.now(), username)
                    )
                    conn.commit()

                    # 根据角色返回不同值

                    return 1
            # 用户不存在或密码错误
            return -1
    finally:
        conn.close()

# 【登录页面】查询用户角色
def get_user_role(username: str):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT role FROM users WHERE username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return result["role"]  # 返回角色字符串，例如 'admin'
            return None  # 用户不存在
    finally:
        connection.close()

# 【登录页面】注册用户
def register_user(username, password, fullname, role='undefined'):
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            # 检查用户名是否存在
            cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                return False
            # 使用 SHA256 哈希密码
            password_hash = hash_password(password)
            sql = "INSERT INTO users (username, password_hash, fullname, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, password_hash, fullname, role))
            conn.commit()
            return True
    finally:
        conn.close()


# 【登录页面】修改密码
def change_password(username, old_password, new_password):
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if result and result[0] == hash_password(old_password):
                new_hash = hash_password(new_password)
                cursor.execute("UPDATE users SET password_hash=%s WHERE username=%s", (new_hash, username))
                conn.commit()
                return True
            return False
    finally:
        conn.close()




if __name__ == "__main__":
    # 1.【扫描数据页面】时间范围查询数据
    # 【扫描数据页面】查询时间范围例子
    start_date_eg = "2025-09-01"
    end_date_eg = "2025-09-30"

    data = query_measurements(start_date_eg, end_date_eg)
    if data:
        for row in data:
            print(row)
    else:
        print("没有查询到数据")

