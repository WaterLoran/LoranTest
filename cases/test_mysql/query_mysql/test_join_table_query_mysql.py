from .mysql import exec_sql
from .prepare_data import *
import pytest
"""
必读:
1. sex的表示中1表示男,2表示女
"""


def clean_databases_before_exec_sql():
    """
    本部分代码已经移动到conftest中,将会在每次执行用例的时候先去执行,如果autouse为True时,将会自动执行
    :return:
    """
    # 如果不存在这些表,那么久创建这些表
    delete_all_sheet()

    create_students_sheet()
    create_courses_sheet()
    create_tearchers_sheet()
    create_score_sheet()

    # 添加学生数据
    prepare_students_data()
    prepare_teachers_data()
    prepare_courses_data()
    prepare_score_data()
    pass


def test_search_01():
    # # 1、查询课程编号为“6001”的课程比“6002”的课程成绩高的所有学生的学号（重点）
    sql_cmd = """
    select s1.s_id
    from score s1
    join score s2
    on s1.s_id = s2.s_id
    where s1.c_id = '6001' and s2.c_id = '6002' and s1.score > s2.score
    """
    exec_sql(sql_cmd)


def test_search_02():
    # 2、查询平均成绩大于60分的学生的学号和平均成绩（简单，第二道重点）
    sql_cmd = """
        select s_id, avg(score)
        from score
        group by s_id
        having avg(score) > 85
        """
    exec_sql(sql_cmd)

def test_search_03():
    #  3、所有成绩小于60分的学生信息
    sql_cmd = """
        select * 
        from students s 
        where s.s_id not in (
            select sc.s_id
            from score sc
            where sc.score > 85
        )
    """
    exec_sql(sql_cmd)


def test_search_04():
    # 4、查询平均成绩小于60分的学生的学号的平均成绩，考虑没参加考试的情况
    """
    最后需要哦使用group by来分组,然后才能去取平均值
    :return:
    """
    sql_cmd = """
            select s.s_id, avg(ifnull(sc.score, 0)) as new_avg
            from students s
            join score sc
            on s.s_id = sc.s_id
            where s.s_id not in (
                select s_id 
                from score 
                group by s_id
                having avg(score) > 86
            )
            group by s.s_id 
            """
    exec_sql(sql_cmd)

def test_search_05():
    # 5、查询没学过“教师8001”老师课的学生的学号、姓名（重点）
    """
    最后需要使用group by来分组,然后才能去取平均值
    :return:
    """
    sql_cmd = """
        select st.s_id, st.name
        from students st
        where st.s_id not in (
            select sc.s_id  
            from courses c 
            join teachers t
            on c.t_id = t.t_id
            join score sc   
            on sc.c_id = c.c_id  
            where t.name = "教师8010"
        )              
    """
    exec_sql(sql_cmd)


def test_search_06():
    # 6、查询学过“张三”老师所教的所有课的同学的学号、姓名（重点）
    sql_cmd = """
        select st.s_id, st.name
        from students st
        where st.s_id in (
            select sc.s_id  
            from courses c 
            join teachers t
            on c.t_id = t.t_id
            join score sc   
            on sc.c_id = c.c_id  
            where t.name = "教师8010"
        )              
    """
    exec_sql(sql_cmd)


def test_search_07():
    # 7、查询学过编号为“01”的课程并且也学过编号为“02”的课程的学生的学号、姓名（重点）
    sql_cmd = """
        select s_id, name
        from students 
        where s_id in (
            select s1.s_id
            from score s1
            where s1.c_id = "6009"
        ) 
        and s_id in (
            select s1.s_id
            from score s1
            where s1.c_id = "6010"
        )         
    """
    exec_sql(sql_cmd)


def test_search_08():
    # 8、查询学过编号为“6009”的课程但没有学过编号为“6010”的课程的学生的学号、姓名（重点）
    sql_cmd = """
        select s_id, name
        from students 
        where s_id in (
            select s1.s_id
            from score s1
            where s1.c_id = "6009"
        ) 
        and s_id not in (
            select s1.s_id
            from score s1
            where s1.c_id = "6010"
        )  
    """
    exec_sql(sql_cmd)


def test_search_09():
    #  9、查询没有学全所有课的学生的学号、姓名(重点)
    sql_cmd = """
        select s_id, name
        from students 
        where s_id not in (
            select s_id
            from score 
            group by s_id 
            having count(c_id) = (select count(c_id) from courses)
        )
    """
    exec_sql(sql_cmd)


def test_search_10():
    # 10、查询至少有一门课与学号为“1001”的学生所学课程相同的学生的学号和姓名（重点）
    """
    distinct 表示去重
    :return:
    """
    sql_cmd = """
        select distinct s.s_id, name 
        from students s 
        join score sc 
        on sc.s_id = s.s_id 
        where sc.c_id in 
        (
            select sc.c_id 
            from score sc 
            where sc.s_id = 1001 
        ) 
        and s.s_id != '1001'
    """
    exec_sql(sql_cmd)

def test_search_11():
    # 11、查询和“1004”号同学所学课程完全相同的其他同学的学号(重点)
    """
    # 原链接答案不对,group_concat 是直接连接,并不排序,但此处场景需要排序先
    GROUP_CONCAT(DISTINCT expression
    ORDER BY expression
    SEPARATOR sep);
    //更多请阅读：https://www.yiibai.com/mysql/group_concat.html
    :return:
    """
    sql_cmd = """
        select s_id 
        from score 
        group by s_id 
        having group_concat(c_id order by c_id) = (
            select group_concat(c_id order by c_id)
            from score
            where s_id = 1004
        )
        and s_id != 1004
    """
    exec_sql(sql_cmd)


def test_search_12():
    # 12、查询没学过"张三"老师讲授的任一门课程的学生姓名(重点，能做出来）
    sql_cmd = """
        select s_id, name
        from students
        where s_id not in (
            select s_id 
            from score sc
            join courses c 
            on sc.c_id = c.c_id
            join teachers t 
            on t.t_id = c.t_id
            where t.name = "教师8010"
        )
    """
    exec_sql(sql_cmd)


def test_search_13():
    # 13、查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩（重点）
    sql_cmd = """
        select sc.s_id, s.name, avg(score) as 平均分
        from score sc
        join students s 
        on sc.s_id = s.s_id 
        group by s.s_id 
        having count(if(sc.score < 85, 1, null)) >= 2
    """
    exec_sql(sql_cmd)


def test_search_14():
    # 14、按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩(重重点)
    sql_cmd = """

    """
    exec_sql(sql_cmd)


def test_search_15():
    # 15、查询各科成绩最高分、最低分和平均分：以如下形式显示：
    # # 课程ID，课程name，最高分，最低分，平均分，及格率，中等率，优良率，优秀率
    # #（及格为>=60，中等为：70-80，优良为：80-90，优秀为：>=90） (超级重点)
    sql_cmd = """
        select sc.c_id, c.name, max(score), min(score), avg(score),
        count(if(score >= 60, 1, null)) / count(score) as 及格率,
        count(if(score >= 70 and score < 80, 1, null)) / count(score) as 中等率,
        count(if(score >= 80 and score <= 100, 1, null)) / count(score) as 优秀率
        from score sc
        join courses c 
        on sc.c_id = c.c_id 
        group by sc.c_id 
    """
    exec_sql(sql_cmd)


def test_search_16():
    # 16、查询所有课程的成绩第2名到第3名的学生信息及该课程成绩（重要）
    sql_cmd = """

    """
    exec_sql(sql_cmd)


def test_search_17():
    # 17、查询学生平均成绩及其名次（重点）
    sql_cmd = """

    """
    exec_sql(sql_cmd)


def test_search_18():
    # 18、查询各科成绩前三名的记录（不考虑成绩并列情况）（重点）
    sql_cmd = """

    """
    exec_sql(sql_cmd)


def test_search_19():
    # 19、查询所有学生的课程及分数情况（重点,同上）
    sql_cmd = """
    # select s_id, 
    # max(case when c_id = 6001 then else null end) 1001,
    # max(case when c_id = 6002 then else null end) 1002,
    # max(case when c_id = 6003 then else null end) 1003
    # from score
    # group by s_id
    """
    exec_sql(sql_cmd)


def test_search_20():
    # 20、查询任何一门课程成绩在70分以上的姓名、课程名称和分数（重点） 注：不用group by
    sql_cmd = """
    select s.name, c.name, score
    from score sc
    join students s 
    on sc.s_id = s.s_id
    join courses c 
    on sc.c_id = c.c_id
    where s.s_id not in (
        select s_id 
        from score
        where score < 85
    ) order by s.name
    """
    exec_sql(sql_cmd)


def test_search_21():
    # 21、查询选修“张三”老师所授课程的学生中成绩最高的学生姓名及其成绩（重要top）
    # #（成绩最高学生可能有n个，应该用嵌套查到最高成绩再查成绩等于最高成绩的学生信息）
    sql_cmd = """
        select s.s_id, s.name, score 
        from courses c
        join teachers t 
        on t.t_id = c.t_id
        join score sc 
        on sc.c_id = c.c_id 
        join students s 
        on s.s_id = sc.s_id 
        where t.name = "教师8009"
        and score =  (
            select score 
            from courses c
            join teachers t 
            on t.t_id = c.t_id
            join score sc 
            on sc.c_id = c.c_id 
            where t.name = "教师8009"
            order by score desc 
            limit 1
        )    
    """
    exec_sql(sql_cmd)


def test_search_22():
    # 22、查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩 （重点）
    sql_cmd = """
        select sc1.* 
        from score sc1
        join score sc2
        on sc1.s_id = sc2.s_id
        and sc1.c_id != sc2.c_id
        and sc1.score = sc2.score
    """
    exec_sql(sql_cmd)


def test_search_23():
    # 23、查询各学生的年龄（精确到月份）
    sql_cmd = """
        select name, round(datediff(now(), birth)/365, 1)
        from students
    """
    exec_sql(sql_cmd)


def test_search_24():
    # 24、查询没学过“张三”老师讲授的任一门课程的学生姓名
    sql_cmd = """
        select * 
        from students s 
        where s.s_id not in (
            select sc.s_id
            from score sc
            join courses c 
            on sc.c_id = c.c_id 
            join teachers t 
            on t.t_id = c.t_id 
            where t.name = "教师8001"
        )
    """
    exec_sql(sql_cmd)


if __name__ == '__main__':
    # 如果不存在这些表,那么久创建这些表
    delete_all_sheet()

    create_students_sheet()
    create_courses_sheet()
    create_tearchers_sheet()
    create_score_sheet()

    # 添加学生数据
    prepare_students_data()
    prepare_teachers_data()
    prepare_courses_data()
    prepare_score_data()

