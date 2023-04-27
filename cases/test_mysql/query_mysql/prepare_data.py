from .mysql import exec_sql

"""
必读:
1. sex的表示中1表示男,2表示女
"""


def delete_all_sheet():
    sql_cmd = """DROP TABLE students ;"""
    exec_sql(sql_cmd)

    sql_cmd = """DROP TABLE teachers ;"""
    exec_sql(sql_cmd)

    sql_cmd = """DROP TABLE courses ;"""
    exec_sql(sql_cmd)

    sql_cmd = """DROP TABLE score ;"""
    exec_sql(sql_cmd)

def create_students_sheet():
    sql_cmd = """
        CREATE TABLE IF NOT EXISTS `students`(
       `s_id` INT UNSIGNED,
       `name` VARCHAR(100) NOT NULL,
       `birth` DATETIME,
       `sex` TINYINT,
       PRIMARY KEY ( `s_id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    exec_sql(sql_cmd)

def create_tearchers_sheet():
    sql_cmd = """
        CREATE TABLE IF NOT EXISTS `teachers`(
       `t_id` INT UNSIGNED,
       `name` VARCHAR(100) NOT NULL,
       PRIMARY KEY ( `t_id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    exec_sql(sql_cmd)

def create_courses_sheet():
    sql_cmd = """
        CREATE TABLE IF NOT EXISTS `courses`(
       `c_id` INT UNSIGNED,
       `name` VARCHAR(100) NOT NULL,
       `t_id` INT UNSIGNED,
       PRIMARY KEY ( `c_id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    exec_sql(sql_cmd)

def create_score_sheet():
    sql_cmd = """
        CREATE TABLE IF NOT EXISTS `score`(
        id INT NOT NULL AUTO_INCREMENT,
       `s_id` INT UNSIGNED,
       `c_id` INT UNSIGNED,
       `score` INT UNSIGNED,
       PRIMARY KEY ( `id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    exec_sql(sql_cmd)

def prepare_students_data():
    student_data = [
        [1001, "学生1001", '1996-12-31 23:59:59', 1],
        [1002, "学生1002", '1996-10-31 23:59:59', 1],
        [1003, "学生1003", '1996-9-22 23:59:59', 1],
        [1004, "学生1004", '1996-2-11 23:59:59', 1],
        [1005, "学生1005", '1996-1-31 23:59:59', 1],
        [1006, "学生1006", '1996-8-31 23:59:59', 1],
        [1007, "学生1007", '1996-5-31 23:59:59', 1],
        [1008, "学生1008", '1996-2-1 23:59:59', 1],
        [1009, "学生1009", '1996-6-22 23:59:59', 1],
        [1010, "学生1010", '1996-4-11 23:59:59', 1],
    ]
    sql_basic = "INSERT INTO students ( s_id, name, birth, sex)  VALUES  ( {}, '{}', '{}', {} );"
    for i in range(len(student_data)):
        item = student_data[i]
        s_id, name, birth, sex = item
        sql_cmd = sql_basic.format(s_id, name, birth, sex)
        exec_sql(sql_cmd)


def prepare_teachers_data():
    teachers_data = [
        [8001, "教师8001"],
        [8002, "教师8002"],
        [8003, "教师8003"],
        [8004, "教师8004"],
        [8005, "教师8005"],
        [8006, "教师8006"],
        [8007, "教师8007"],
        [8008, "教师8008"],
        [8009, "教师8009"],
        [8010, "教师8010"],
    ]
    sql_basic = "INSERT INTO teachers (t_id, name)  VALUES  ( {}, '{}' );"
    for item in teachers_data:
        t_id, name = item
        sql_cmd = sql_basic.format(t_id, name)
        exec_sql(sql_cmd)


def prepare_courses_data():
    courses_data = [
        [6001, "课程6001", 8001],
        [6002, "课程6002", 8002],
        [6003, "课程6003", 8003],
        [6004, "课程6004", 8004],
        [6005, "课程6005", 8005],
        [6006, "课程6006", 8006],
        [6007, "课程6007", 8007],
        [6008, "课程6008", 8008],
        [6009, "课程6009", 8009],
        [6010, "课程6010", 8010],
    ]
    sql_basic = "INSERT INTO courses (c_id, name, t_id)  VALUES  ( {}, '{}', {} );"
    for item in courses_data:
        c_id, name, t_id = item
        sql_cmd = sql_basic.format(c_id, name, t_id)
        exec_sql(sql_cmd)


def prepare_score_data():
    score_data = [
        [1001, 6001, 81],
        [1001, 6002, 80],
        [1001, 6003, 81],
        [1001, 6004, 81],
        # [1001, 6005, 81],  # search_10  构造1号学生和2号学生无重合的课程
        # [1001, 6006, 81],  # search_10  构造1号学生和2号学生无重合的课程
        # [1001, 6007, 81],  # search_10  构造1号学生和2号学生无重合的课程
        # [1001, 6008, 81],  # search_10  构造1号学生和2号学生无重合的课程
        # [1001, 6009, 81],  # search_10  构造1号学生和2号学生无重合的课程
        # [1001, 6010, 81],  # search_10  构造1号学生和2号学生无重合的课程
        # [1002, 6001, 82],  # search_10  构造1号学生和2号学生无重合的课程
        # [1002, 6002, 82],  # search_10  构造1号学生和2号学生无重合的课程
        # [1002, 6003, 82],  # search_10  构造1号学生和2号学生无重合的课程
        # [1002, 6004, 82],  # search_10  构造1号学生和2号学生无重合的课程
        [1002, 6005, 82],
        [1002, 6006, 82],
        [1002, 6007, 82],
        [1002, 6008, 82],
        [1002, 6009, 82],
        [1002, 6010, 82],
        [1003, 6001, 83],
        [1003, 6002, 83],
        [1003, 6003, 83],
        [1003, 6004, 83],
        [1003, 6005, 83],
        [1003, 6006, 83],
        [1003, 6007, 83],
        [1003, 6008, 83],
        [1003, 6009, 83],
        [1003, 6010, 83],
        [1004, 6001, 84],
        [1004, 6002, 84],
        [1004, 6003, 84],
        [1004, 6005, 84],  # search_11 调换一下顺序
        [1004, 6004, 84],  # search_11 调换一下顺序
        [1004, 6006, 84],
        [1004, 6007, 84],
        [1004, 6008, 84],
        [1004, 6009, 84],
        [1004, 6010, 84],
        [1005, 6001, 85],
        [1005, 6002, 84],
        [1005, 6003, 85],
        [1005, 6004, 85],
        [1005, 6005, 85],
        [1005, 6006, 85],
        [1005, 6007, 85],
        [1005, 6008, 85],
        [1005, 6009, 85],
        [1005, 6010, 85],
        [1006, 6001, 86],
        [1006, 6002, 86],
        [1006, 6003, 86],
        [1006, 6004, 86],
        [1006, 6005, 86],
        [1006, 6006, 86],
        [1006, 6007, 86],
        [1006, 6008, 86],
        [1006, 6009, 86],
        [1006, 6010, 86],
        [1007, 6001, 87],
        [1007, 6002, 87],
        [1007, 6003, 87],
        [1007, 6004, 87],
        [1007, 6005, 87],
        [1007, 6006, 87],
        [1007, 6007, 87],
        [1007, 6008, 87],
        [1007, 6009, 87],
        [1007, 6010, 87],
        [1008, 6001, 88],
        [1008, 6002, 88],
        [1008, 6003, 88],
        [1008, 6004, 88],
        [1008, 6005, 88],
        [1008, 6006, 88],
        [1008, 6007, 88],
        [1008, 6008, 88],
        [1008, 6009, 88],
        [1008, 6010, 88],
        [1009, 6001, 89],
        [1009, 6002, 89],
        [1009, 6003, 89],
        [1009, 6004, 89],
        [1009, 6005, 89],
        [1009, 6006, 89],
        [1009, 6007, 89],
        [1009, 6008, 89],
        [1009, 6009, 90],
        # [1009, 6010, 89],   # search_05  注释点这一行,就表示10号学生没学过10号老师的课程
        [1010, 6001, 90],
        [1010, 6002, 90],
        [1010, 6003, 90],
        [1010, 6004, 90],
        [1010, 6005, 90],
        [1010, 6006, 90],
        [1010, 6007, 90],
        [1010, 6008, 90],
        [1010, 6009, 90],
        # [1010, 6010, 90],  # search_05  注释点这一行,就表示10号学生没学过10号老师的课程
    ]
    sql_basic = "INSERT INTO score (s_id, c_id, score)  VALUES  ( {}, {}, {} );"
    for item in score_data:
        s_id, c_id, score = item
        sql_cmd = sql_basic.format(s_id, c_id, score)
        exec_sql(sql_cmd)

