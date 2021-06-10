import sqlite3



def validate_login(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""select * from users
                    where username='{username}' and password='{password}' """)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if not data:
        return False
    return True




def signup_user(username, password, plan, space_used):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (username,password,plan,space_used) VALUES (?,?,?,?) """,
                   (username, password, plan, space_used))
    conn.commit()
    cursor.close()
    conn.close()







def create_user_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (username text,password text,plan text, space_used number) """)
    conn.commit()
    cursor.close()
    conn.close()





def insert_data(user_id, name, data, data_size, upload_time):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO user_data (user_id,name,data,data_size,upload_time) VALUES (?,?,?,?,?) """,
                   (user_id, name, data, data_size, upload_time))

    conn.commit()
    cursor.close()
    conn.close()


def create_user_data_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user_data (user_id TEXT,name TEXT,data BLOB,data_size number, upload_time TEXT) """)
    conn.commit()
    cursor.close()
    conn.close()




def validate_login(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""select * from users
                    where username='{username}' and password='{password}' """)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if not data:
        return False
    return True


def create_ip_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""create table ip_records (username text, ip text)""")
    conn.commit()
    cursor.close()
    conn.close()


def insert_new_ip(username, ip):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""insert into ip_records values ('{username}','{ip}')""")
    conn.commit()
    cursor.close()
    conn.close()


def delete_ip(ip):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""delete from ip_records where ip='{ip}'""")
    conn.commit()
    cursor.close()
    conn.close()


def erase_ips():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""delete from ip_records""")
    conn.commit()
    cursor.close()
    conn.close()


def get_username_by_ip(ip):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""select username from ip_records where ip='{ip}'""")
    username = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return username


def check_file_belongs(username, filename):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"""select * from user_data where user_id='{username}' and name='{filename}'""")
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if not found:
        return False
    return True


def delete_record_logout(ip):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" delete from ip_records where ip='{ip}'""")
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()


def view_files(username):
    filenames = []
    file_sizes = []
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" select name, data_size from user_data where user_id='{username}';""")
    found = cursor.fetchall()
    for x in found:
        filenames.append(x[0])
        file_sizes.append(x[1])
    conn.commit()
    cursor.close()
    conn.close()
    return filenames, file_sizes


def empty_user_data_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" delete from user_data """)
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()


def check_username_available(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" select username from users where username='{username}'""")
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if not found:
        return True
    return False


def create_table_pro_codes_by_admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" create table pro_codes (admin_username text,pro_code text) """)
    conn.commit()
    cursor.close()
    conn.close()


def add_pro_code(username, pro_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" insert into pro_codes values ('{username}','{pro_code}')""")
    conn.commit()
    cursor.close()
    conn.close()


def update_space_used(username, new_file_spcae):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" update users set space_used=(space_used + {new_file_spcae}) where username='{username}' """)
    conn.commit()
    cursor.close()
    conn.close()


def is_user_not_plan_pro(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" select * from users where plan='pro' and username={username} """)
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if not found:
        return True
    return False


def check_user_space_consumed(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" select * from users where username='{username}' and space_used>102400 """)
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if not found:
        return False
    return True


def is_pro_code_valid(pro_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f""" select * from pro_codes where pro_code='{pro_code}' """)
    found = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if not found:
        return False
    return True

