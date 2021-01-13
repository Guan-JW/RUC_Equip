from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.http import HttpResponseRedirect
import json
from django.contrib.auth import authenticate,login
from django.contrib import auth  # 导入auth模块
import pymysql
import datetime


def dictfetchall(cursor):
    desc = cursor.description
    return[
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def index_teacher( request ):
    print("in function index_teacher and group is",request.session['group'], request.session['user'])
    if request.session['group'] == '2' and request.session['user']:
        teacher_id = request.session['user']
        sql_course = "select course_id from teacher where userid = '%s' " %teacher_id
        cursor = connections['default'].cursor()
        cursor.execute(sql_course)
        course_row = dictfetchall(cursor)
        course = course_row[0]['course_id']
        request.session['course_id'] =course
        return render(request,'teacher/index-teacher.html')
    else:
        print('redirect to login')
        return redirect("/Login/")

def DeleteStudentFromCourse(request):
    sno = request.GET['sno']
    cno = request.session['course_id']
    print('sno：',sno)
    sql_delete = "delete from sc where student_id = %s and course_id = %s "
    param= (sno, cno)
    cursor = connections['default'].cursor()
    cursor.execute(sql_delete, param)
    print("delete", sno, 'form course ',cno)

    response = HttpResponse(json.dumps({"status":1}), content_type ="application/json")
    response["Assess-Control-Allow-Origin"] = "*"
    response["Assess-Control-Allow_Methods"] = "POST,GET,OPTIONS"
    response["Assess-Control-Max-Age"] ="1000"
    response["Access-Control-Allow-Headers"] ="*"
    return response

def AddStudentToCourse(request):
    sname = request.GET['sname']
    sno = request.GET['sno']
    cno = request.session['course_id']

    sql_check = "select * from student where userid=%s and name=%s"
    param_check = (sno,sname)
    cursor = connections['default'].cursor()
    cursor.execute(sql_check, param_check)
    check_row = dictfetchall(cursor)
    if check_row:
        sql_add = "insert into sc(student_id, course_id) values(%s,%s)"
        param = (sno, cno)
        cursor.execute(sql_add, param)
        response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
        response["Assess-Control-Allow-Origin"] = "*"
        response["Assess-Control-Allow_Methods"] = "POST,GET,OPTIONS"
        response["Assess-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        print('信息错误')
        response = HttpResponse(json.dumps({"status": -1}),content_type="application/json")
        response["Assess-Control-Allow-Origin"] = "*"
        response["Assess-Control-Allow_Methods"] = "POST,GET,OPTIONS"
        response["Assess-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def EquipDetails(request):
    equip_id = request.GET['equip_id']
    sql_equip_details = "select * from equip, equipmanager,equip_manage where equip.equip_id ='%s' " \
                        "and equip.equip_id = equip_manage.equip_id " \
                        "and equip_manage.manager_id = equipmanager.manager_id" %equip_id

    cursor = connections['default'].cursor()
    cursor.execute(sql_equip_details)
    equip_details = dictfetchall(cursor)
    context = {}
    print(equip_details[0]);
    context['equip_id'] = equip_details[0]['equip_id']
    context['equip_name'] = equip_details[0]['equip_name']
    context['type'] = equip_details[0]['type']
    context['description'] = equip_details[0]['description']
    context['manager_id'] = equip_details[0]['manager_id']
    context['email'] = equip_details[0]['email']
    context['address'] = equip_details[0]['address']
    context['status'] = equip_details[0]['status']
    context['qualification'] = equip_details[0]['qualification']
    context['check_qualification'] = equip_details[0]['check_qualification']
    context['buy_date'] = equip_details[0]['buy_date']
    return JsonResponse(context)

def CourseManage( request):
    if request.session['user'] and request.session['group']=='2':
        cursor = connections['default'].cursor()
        teacher_id = request.session['user']

        sql_teacher_course = "select teacher.name teacher_name, teacher.email email," \
                             "teacher.userid userid, teacher.title_type title_type, " \
                             " teacher.course_id course_id, course.details details ,course.name course_name" \
                             " from teacher,course " \
                             " where teacher.course_id = course.id and teacher.userid= '%s'" %teacher_id
        sql_student_in_course = "select student.name student_name,student.userid student_id," \
                                " student.session session, student.email student_email " \
                                " from student,sc,teacher" \
                                " where student.userid = sc.student_id " \
                                " and teacher.course_id = sc.course_id " \
                                " and teacher.userid='%s'" %teacher_id
        cursor.execute(sql_teacher_course)
        raw_teacher_course = dictfetchall(cursor)
        cursor.execute(sql_student_in_course)
        raw_student = dictfetchall(cursor)
        context = {}
        context['student'] = raw_student
        context['teacher'] = raw_teacher_course
        return render(request,'teacher/CourseManage.html',context)
    else:
        return redirect("/Login/")

def QueryLog(request):
    if request.session['user'] and request.session['group']=='2':
        cursor = connections['default'].cursor()
        teacher_id = request.session['user']
        sql_query = "select student.name student_name,student.userid student_id,equip.equip_name equip_name, " \
                    "equip.equip_id equip_id, equip_log.start_time start_time,equip_log.end_time end_time," \
                    "equip_log.item item " \
                    "from course,equip,equip_log,sc,student,teacher " \
                    "where course.id = sc.course_id  " \
                    "and student.userid=sc.student_id " \
                    "and equip.equip_id = equip_log.equip_id " \
                    "and teacher.userid='%s' " \
                    "and equip_log.userid = student.userid;" %teacher_id

        cursor.execute(sql_query)
        raw_equip_log = dictfetchall(cursor)
        context= {}
        context['log'] = raw_equip_log
        return render(request, 'teacher/query-log.html',context)
    else:
        return redirect("/Login/")

def QueryInstru(request):
    if request.session['user'] and request.session['group']=='2':
        cursor = connections['default'].cursor()
        sql_equip = "select equip_name,equip_id,type,address,status " \
                    "from equip " \
                    "where equip.status='正常' and equip_id !=-1 order by equip_id"
        cursor.execute(sql_equip)
        raw_equip = dictfetchall(cursor)
        context = {}
        context['equip'] = raw_equip
        return render(request ,'teacher/query-instru.html',context)
    else:
        return redirect("/Login/")

# 预约编号(index_id)、课题组(course_name)、教师、申请人、仪器名、仪器编号、型号规格、使用时间、实验内容、操作
def Check(request):
    if request.session['user'] and request.session['group'] =='2':
        teacher_id = request.session['user']
        course_id = request.session['course_id']
        context = {}
        cursor = connections['default'].cursor()
        # 本课题组下，预约状态为0（等待老师审批）的预约记录
        sql_appointing = "select a.index_id index_id, a.userid student_id, a.course_id course_id, " \
                         "c.name course_name, t.name teacher_name, t.userid teacher_id, " \
                         "s.name user_name, equip_name, a.equip_id equip_id, type, " \
                         "a1.use_date use_date, a1.use_time start_time, a2.use_time+1 end_time, item " \
                         "from appoint_index a, appointment a1, appointment a2," \
                         "course c, teacher t,student s,equip e " \
                         "where a.status ='0' and a.course_id = c.id and c.id = t.course_id " \
                         "and a.userid = s.userid and a.equip_id = e.equip_id and a.course_id = '%s' " \
                         "and a.start_id=a1.appointment_id and a.end_id = a2.appointment_id; " %course_id
        cursor.execute(sql_appointing)
        appointing = dictfetchall(cursor)
        for e in appointing:
            e['use_date'] = str(e['use_date'])
        context['appointing'] = appointing
        print('apponint :',appointing)

        sql_appointed = "select index_id, a.userid student_id, a.course_id,c.name course_name," \
                        "t.name teacher_name, t.userid teacher_id,s.name user_name ,equip_name," \
                        "a.equip_id equip_id, type, a1.use_date use_date, a1.use_time start_time," \
                        "a2.use_time+1 end_time, item,a.status " \
                        "from appoint_index a,appointment a1,appointment a2, course c,teacher t," \
                        "student s,equip e " \
                        "where (a.status ='1' or a.status='-1' or a.status ='2' or a.status ='-2') " \
                        "and t.userid =%s and a.course_id = c.id and a.userid = s.userid and a.equip_id = e.equip_id "\
                        "and a.start_id = a1.appointment_id and a.end_id = a2.appointment_id and a.course_id =%s " \
                        "order by index_id;"
        param=(teacher_id,course_id)
        cursor.execute(sql_appointed,param)
        appointed = dictfetchall(cursor)
        for e in appointed:
            print(e['status'])
            e['use_date'] = str(e['use_date'])
            if e['status'] =='1':
                e['status'] ='通过'
            elif e['status'] =='-4':
                e['status'] = '已撤回'
            else:
                e['status'] ='驳回'
        context['appointed'] = appointed
        return render(request,'teacher/check.html' , context)
    else:
        return redirect("/Login/")

def Agree(request):
    if request.session['user'] and request.session['group'] =='2':
        index_id = request.GET['index_id']
        cursor = connections['default'].cursor()
        cursor.execute("update appoint_index set status = '1' where index_id = \"%s\"" % str(index_id))
        response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        return redirect("/Login")

def Reject(request):
    if request.session['user'] and request.session['group'] =='2':
        index_id = request.GET['index_id']
        cursor = connections['default'].cursor()
        cursor.execute("update appoint_index set status = '-1' where index_id = \"%s\"" % str(index_id))
        response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        return redirect("/Login")

def Login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        name = request.POST.get('userid')
        password = request.POST.get('password')
        # 创建与数据库的链接
        conn = pymysql.connect(host='127.0.0.1', user='root',password='', database='equipment', port=3306,)
        # 拿到一个游标
        cursor = conn.cursor()
        # 执行sql
        cursor.execute('select * from user where userid=%s and password=%s ', (name, password))
        # 获取结果
        ret = dictfetchall(cursor)
        cursor.close()
        conn.close()
        if ret:
            ret = ret[0]['group']
            request.session['user'] = name
            request.session['group'] = ret
            request.session['password'] = password
            if ret == '1':
                return redirect('/student/')
            elif ret == '2':
                return redirect('/teacher/Teacher/')
            elif ret == '3':
                return redirect('/equip/index/')
        else:
            return HttpResponse('用户名或密码错误，请返回重试！')

def Register(request):
    if request.method == "POST":
        print(request.POST)
        user = request.POST.get("userid", None)  # 获取用户名
        pwd = request.POST.get("password", None)  # 获取用户的密码
        check_pwd = request.POST.get("password", None)   #确认用户密码
        name = request.POST.get("name", None)    # 获取姓名
        session = request.POST.get("session", None)   # 获取年级
        gender = request.POST.get("gender", None)    # 获取性别
        email = request.POST.get("email", None)  # 获取邮箱

        if pwd == check_pwd:
            if email.find("@") == -1 or not email.endswith('.com'):
                return HttpResponse('邮箱格式错误，请返回重试！')
            else:
                print(user)

                cursor = connections['default'].cursor()
                sql = "insert into user values(%s,%s,1)"
                # param应该为tuple或者list
                param = (user, pwd)
                # 执行成功n为1
                n = cursor.execute(sql, param)
                if n == 1:
                    sql = "insert into student values(%s,%s,%s,%s,%s)"
                    param = (user, name, session, gender, email)
                    n = cursor.execute(sql, param)
                    if n == 1:
                        cursor.close()
                        return redirect('/Login/')
                else:
                    return HttpResponse('注册新用户失败，请返回重试！')
        else:
            return HttpResponse('两次输入的密码不一致，请返回重试！')
    return render(request, 'Register.html')


def TeacherPersonal(request):
    userid = request.session['user']
    cursor = connections['default'].cursor()
    sql_teacher = "select * from teacher where userid = %s"
    param =(userid)
    print(userid)
    cursor.execute(sql_teacher, param)

    raw = dictfetchall(cursor)
    context = {}
    context['userid'] = raw[0]['userid']
    context['name'] = raw[0]['name']
    context['course_id'] = raw[0]['course_id']
    context['title_type'] = raw[0]['title_type']
    context['gender'] = raw[0]['gender']
    context['email'] = raw[0]['email']

    if request.method == "POST":
        old_pwd = request.POST.get("old_password", None)
        new_pwd = request.POST.get("new_password", None)
        check_pwd = request.POST.get("check_password", None)

        if request.session['user']:
            if old_pwd != request.session['password']:
                return HttpResponse('密码验证失败，请重试！')

            if new_pwd and new_pwd == check_pwd:
                sql_change = "update user set password = %s where user.userid= %s "
                param = (new_pwd,userid)
                cursor.execute(sql_change,param)
                return redirect('/Login/',context={'密码已修改，请重新登陆'})
    return render(request, 'teacher/personal.html', context)


def index(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    cursor = connections['default'].cursor()
    cursor.execute("select * from course where id in (select course_id from sc where (student_id=(select userid from student where userid='%s')))" % str(userid))
    raw = dictfetchall(cursor)
    # print(raw)
    # print(len(raw))
    context = {}
    context['courses_stu'] = raw
    context['len'] = len(raw)   # 课题组个数
    # 用到了userid！！！！！！！！！！！！！！！！！！！！！！！！
    # 还没开始且状态为正的
    cursor.execute("select count(*) lab_num from appoint_index,appointment \
                        where appoint_index.userid='%s' and status in ('0', '1', '2') and appoint_index.start_id = appointment.appointment_id and (appointment.use_time * 3600 + unix_timestamp(appointment.use_date)) > unix_timestamp(now())" % str(userid))
    raw_lab_num = dictfetchall(cursor)
    # print(raw_lab_num)
    context['lab_num'] = raw_lab_num[0]['lab_num']
    # 用到了userid !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    cursor.execute("select count(*) log_num, unix_timestamp(now()) now_time from equip_log\
                        where userid='%s' and  log_status='未完成' and unix_timestamp(start_time) < unix_timestamp(now())" % str(userid))
    raw_unfinished_log = dictfetchall(cursor)
    # print(raw_unfinished_log)
    context['unfinished_log_num'] = raw_unfinished_log[0]['log_num']

    return render(request, 'student/index.html', context)


def Logs(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    cursor = connections['default'].cursor()
    context = {}
    # 使用了学号
    cursor.execute("select log_id, equip.equip_id, course.id course_id, course.name course_name,equip.equip_name, date_format(start_time,'%%Y-%%m-%%d %%H:%%i') start_time, date_format(end_time,'%%Y-%%m-%%d %%H:%%i') end_time, item, e_status\
                        from equip_log, equip,course\
                        where equip_log.equip_id != '-1' and equip_log.equip_id = equip.equip_id and equip_log.course_id = course.id and equip_log.log_status='未完成' and equip_log.userid='%s'\
                        order by start_time ASC" % str(userid))   # 按时间升序排列
    raw = dictfetchall(cursor)
    # 判断实验是否完成
    now = datetime.datetime.now()
    for i in range(len(raw)):
        end_time = datetime.datetime.strptime(raw[i]['end_time'], '%Y-%m-%d %H:%M')
        start_time = datetime.datetime.strptime(raw[i]['start_time'], '%Y-%m-%d %H:%M')
        if now.timestamp() - end_time.timestamp() > 0:  # 已完成
            raw[i]['is_done'] = 1
        elif now.timestamp() - start_time.timestamp() < 0:  # 未开始，不允许未开始的实验编写日志
            raw[i]['is_done'] = -1
        else:   # 进行中
            raw[i]['is_done'] = 0
    # print(raw)
    context['equip_log_undo'] = raw
    # 使用了学号
    cursor.execute("select log_id, equip.equip_id, course.id course_id, course.name course_name,equip.equip_name, date_format(start_time,'%%Y-%%m-%%d %%H:%%i') start_time, date_format(end_time,'%%Y-%%m-%%d %%H:%%i') end_time, item, e_status \
                    from equip_log, equip,course \
                    where equip_log.equip_id != '-1' and equip_log.equip_id = equip.equip_id and userid='%s' and equip_log.course_id = course.id and equip_log.log_status='已提交'\
                    order by log_id DESC" % str(userid))
    raw_done_log = dictfetchall(cursor)
    context['done_log'] = raw_done_log
    return render(request, 'student/log.html', context)


def Log_Edit(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    log_id = request.GET.get("log_id")  # 解析url参数
    cursor = connections['default'].cursor()
    context = {}
    cursor.execute("select equip.equip_id, course.id course_id, course.name course_name,equip.equip_name,date_format(start_time,'%%Y-%%m-%%d %%H:%%i') start_time, date_format(end_time,'%%Y-%%m-%%d %%H:%%i') end_time, item, e_status,teacher.name teacher_name, equip_log.details details\
                    from equip_log, equip,course,teacher \
                    where log_id=%d and equip_log.equip_id = equip.equip_id and equip_log.course_id = course.id and equip_log.course_id=teacher.course_id" % int(log_id))
    raw = dictfetchall(cursor)
    # print(raw)
    context['log_id'] = log_id
    for key in raw[0].keys():
        # print(key)
        context[key] = raw[0][key]
    # context['log'] = raw
    if context['details'] == None:
        # print('is null')
        context['details'] = ''
    return render(request, 'student/log-edit.html', context)

def submit_log(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    # 更新日志
    log_id = request.POST.get("log_id")  # 解析url参数
    details = request.POST.get("details")
    prev_equip_status = request.POST.get("equip_status")
    # print(log_id)
    # print(prev_equip_status, succ_equip_status, details)
    e_status ='正常'
    if prev_equip_status == 'error':
        e_status = '故障'
    cursor = connections['default'].cursor()
    cursor.execute("update equip_log set e_status='%s',log_status='已提交',details='%s' where log_id=%d" % (str(e_status), str(details), int(log_id)))

    response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def Check_Log(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    log_id = request.GET.get("log_id")  # 解析url参数
    # print(log_id)
    cursor = connections['default'].cursor()
    context = {}
    cursor.execute("select equip.equip_id, course.id course_id, course.name course_name,equip.equip_name,date_format(start_time,'%%Y-%%m-%%d') date, date_format(start_time,'%%H:%%i') start_time, date_format(end_time,'%%H:%%i') end_time, item, e_status,teacher.name teacher_name, equip_log.details details from equip_log, equip,course,teacher where log_id=%d and equip_log.equip_id = equip.equip_id and equip_log.course_id = course.id and equip_log.course_id=teacher.course_id" % int(log_id))
    raw = dictfetchall(cursor)
    # print(raw)
    e_state = '正常'
    if raw[0]['e_status'] == '故障':
        e_state = '使用期间出现故障情况'
    raw[0]['e_status'] = e_state
    for key in raw[0].keys():
        context[key] = raw[0][key]
    context['log_id'] = log_id
    # context['done_log'] = raw
    return render(request, 'student/done_log.html', context)


def Calen(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    equip_id = request.GET.get("equip_id")  # 解析url参数
    context = {}
    # print(equip_id)
    cursor = connections['default'].cursor()
    cursor.execute("select name from student where userid='%s'" % str(userid))
    raw_name = dictfetchall(cursor)
    # print(raw_name)
    context['userid'] = userid
    context['user_name'] = raw_name[0]['name']
    context['equip_id'] = equip_id
    cursor.execute("select equip_name, check_qualification from equip where equip_id = '%s'" % str(equip_id))
    raw_equip_name = dictfetchall(cursor)
    context['equip_name'] = raw_equip_name[0]['equip_name']
    context['is_qualify'] = 1
    if raw_equip_name[0]['check_qualification'] == '是':
        cursor.execute("select count(*) qualify_num from qualification where userid='%s' and equip_id='%s'" % (str(userid), str(equip_id)))
        raw_exist = dictfetchall(cursor)
        if raw_exist[0]['qualify_num'] == 0:
            context['is_qualify'] = 0
    # print(context['is_qualify'])


    # 挑选10001号仪器的预约数据，使用了仪器编号
    cursor.execute("select student.name user_name, course.name course_name, Ap1.use_time start_time, Ap2.use_time end_time, unix_timestamp(Ap1.use_date) start_date, unix_timestamp(Ap2.use_date) end_date, item \
                            from appointment Ap1, appointment Ap2, appoint_index, course, student\
                            where Ap1.appointment_id=appoint_index.start_id and Ap2.appointment_id=appoint_index.end_id and appoint_index.status='2' and appoint_index.equip_id='%s' and appoint_index.course_id=course.id and appoint_index.userid=student.userid" % str(equip_id))
    raw_appoint_index = dictfetchall(cursor)
    context['appointment'] = raw_appoint_index

    cursor.execute("select student.name user_name, course.name course_name, Ap1.use_time start_time, Ap2.use_time end_time, unix_timestamp(Ap1.use_date) start_date, unix_timestamp(Ap2.use_date) end_date, item \
                                from appointment Ap1, appointment Ap2, appoint_index, course, student\
                                where Ap1.appointment_id=appoint_index.start_id and Ap2.appointment_id=appoint_index.end_id and appoint_index.status in ('0','1') and appoint_index.equip_id='%s' and appoint_index.course_id=course.id and appoint_index.userid=student.userid" % str(equip_id))
    raw_on_air = dictfetchall(cursor)
    context['appointment_on_air'] = raw_on_air
    # print(raw_on_air)

    cursor.execute("select equip_id, equip_name from equip")
    raw_equip = dictfetchall(cursor)
    #print(raw_equip)
    context['equip'] = raw_equip

    # 使用了user名
    userid = request.session['user']
    cursor.execute("select course.name course_name \
                        from course \
                        where id in (select course_id from sc where (student_id=(select userid from student where userid='%s')))" % str(userid))
    raw_group = dictfetchall(cursor)
    #print(raw_group)
    context['courses'] = raw_group
    return render(request, 'student/calendar.html', context)


def Res(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    cursor = connections['default'].cursor()
    # 使用了user_id!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cursor.execute("select appoint_index.index_id appointment_id, equip_name, course_id, from_unixtime(Ap1.use_time * 3600 + unix_timestamp(Ap1.use_date),'%%Y-%%m-%%d %%h:%%i') start_time, from_unixtime((Ap2.use_time+1) * 3600 + unix_timestamp(Ap2.use_date),'%%Y-%%m-%%d %%h:%%i') end_time, item, appoint_index.status status\
                   from appoint_index, appointment Ap1, appointment Ap2, equip\
                   where appoint_index.status != '-4' and appoint_index.start_id = Ap1.appointment_id and appoint_index.end_id = Ap2.appointment_id and appoint_index.equip_id = equip.equip_id and appoint_index.userid='%s'\
                   order by appointment_id DESC" % str(userid))

    raw = dictfetchall(cursor)
    # print(raw)

    context = {}
    context['res_log'] = raw

    # 使用了userid!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    cursor.execute("select appoint_index.index_id appointment_id, equip_name, course_id, from_unixtime(Ap1.use_time * 3600 + unix_timestamp(Ap1.use_date),'%%Y-%%m-%%d %%h:%%i') start_time, from_unixtime(Ap2.use_time * 3600 + unix_timestamp(Ap2.use_date),'%%Y-%%m-%%d %%h:%%i') end_time, item\
                      from appoint_index, appointment Ap1, appointment Ap2, equip\
                      where appoint_index.status = '-4' and  appoint_index.start_id = Ap1.appointment_id and appoint_index.end_id = Ap2.appointment_id and appoint_index.equip_id = equip.equip_id and appoint_index.userid='%s'\
                      order by appointment_id DESC" % str(userid))
    raw_cancel = dictfetchall(cursor)
    context['cancel_res_log'] = raw_cancel
    return render(request, 'student/Reservation.html', context)


def Arrange(request):
    cursor = connections['default'].cursor()
    stu_id = request.GET['stu_id']
    equip_name = request.GET['equip_name']
    equip_id = request.GET['equip_id']
    course_name = request.GET['course_name']
    start_use_time = request.GET['start_use_time']
    end_use_time = request.GET['end_use_time']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    item = request.GET['item']
    status = 0
    start_timestamp = request.GET['start_timestamp']
    end_timestamp = request.GET['end_timestamp']
    # print('date:')
    # print(start_date, end_date)

    cursor.execute("select from_unixtime(%d) start_time, from_unixtime(%d) end_time" % (int(start_timestamp),int(end_timestamp)))
    raw1 = dictfetchall(cursor)
    # print(raw1)
    start_time = str(raw1[0]['start_time'])
    end_time = str(raw1[0]['end_time'])
    # print(start_time, end_time)

    cursor.execute("select id from course where course.name = '%s'" % str(course_name))
    raw = dictfetchall(cursor)
    course_id = raw[0]['id']

    cursor.execute("select status from equip where equip_id = '%s'" % str(equip_id))
    raw3 = dictfetchall(cursor)
    equip_status = raw3[0]['status']
    # print(equip_status)

    # 插入预约记录
    begin = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    # print(begin, end)
    delta = (end - begin).days
    # print(delta)
    counter = 0
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        # print(i, day)
        # print(str(day).split(' ')[0])
        start_hour = 7
        end_hour = 22
        if i == 0:  # 第一天
            start_hour = start_use_time
        if i == delta:  # 最后一天
            end_hour = end_use_time
        # print(start_hour, end_hour)
        for hour in range(int(start_hour), int(end_hour)):
            cursor.execute("insert into appointment(use_time, use_date) values( %d, '%s')" % (int(hour), str(day).split(' ')[0]))
            counter = counter + 1
    end_id = cursor.lastrowid   # 获取插入的最后一条记录的下标
    start_id = end_id - counter + 1
    # print(start_id, end_id)

    cursor.execute("insert into appoint_index(start_id, end_id, userid, equip_id, course_id, item, status) values(%d, %d, '%s', '%s', %d, '%s', '%s')" % (int(start_id), int(end_id), str(stu_id), str(equip_id), int(course_id), str(item), str(status)))
    appoint_id = cursor.lastrowid
    # 插入实验日志
    cursor.execute("insert into equip_log(equip_id,course_id,appoint_id, start_time,end_time, userid, item, e_status, log_status) values('%s',%d, %d,'%s','%s','%s','%s','%s','未完成')" % (str(equip_id),int(course_id), int(appoint_id), start_time, end_time, str(stu_id),str(item),str(equip_status)))

    response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def save_log(request):
    # 更新日志
    log_id = request.POST.get("log_id")  # 解析url参数
    details = request.POST.get("details")
    prev_equip_status = request.POST.get("equip_status")
    # print(log_id)
    # print(prev_equip_status, succ_equip_status, details)
    e_status ='正常'
    if prev_equip_status == 'error':
        e_status = '故障'
    cursor = connections['default'].cursor()
    cursor.execute("update equip_log set e_status='%s',details='%s' where log_id=%d" % (str(e_status), str(details), int(log_id)))

    response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def cancel_res(request):
    # 撤销预约
    index_id = request.POST.get("index_id")
    print(index_id)
    cursor = connections['default'].cursor()
    cursor.execute("update appoint_index set status = '-4' where index_id = %d" % int(index_id))

    response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def  stu_EquipDetails(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    equip_id = request.GET["equip_id"]
    sql_equip_details = "select * from equip, equipmanager, equip_manage \
                        where equip.equip_id = '%s'\
                        and equip.equip_id = equip_manage.equip_id \
                        and equip_manage.manager_id = equipmanager.manager_id" % equip_id

    cursor = connections['default'].cursor()
    cursor.execute(sql_equip_details)
    equip_details = dictfetchall(cursor)
    # print(equip_details)

    context = {}
    context['equip_id'] = equip_details[0]['equip_id']
    context['equip_name'] = equip_details[0]['equip_name']
    context['type'] = equip_details[0]['type']
    context['description'] = equip_details[0]['description']
    context['manager_id'] = equip_details[0]['manager_id']
    context['email'] = equip_details[0]['email']
    context['address'] = equip_details[0]['address']
    context['status'] = equip_details[0]['status']
    context['qualification'] = equip_details[0]['qualification']
    context['check_qualification'] = equip_details[0]['check_qualification']
    context['buy_date'] = equip_details[0]['buy_date']

    return JsonResponse(context)


def stu_QueryInstru(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    cursor = connections['default'].cursor()
    cursor.execute("select *  from equip where equip_id != '-1' ")
    raw_equip = dictfetchall(cursor)
    context = {}
    context['equip'] = raw_equip
    return render(request, 'student/query-instru.html', context)


def stu_CourseManage(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    course_id = request.GET.get("course_id")  # 解析url参数
    # print(course_id)
    cursor = connections['default'].cursor()

    sql_teacher_course = "select teacher.name teacher_name, teacher.email email," \
                         "teacher.userid userid, teacher.title_type title_type, " \
                         " teacher.course_id course_id, course.details details ,course.name course_name" \
                         " from teacher,course " \
                         " where teacher.course_id = course.id and course.id=%d" % int(course_id)

    sql_student_in_course = "select student.name student_name,student.userid student_id," \
                            " student.session session, student.email student_email " \
                            " from student,sc,teacher" \
                            " where student.userid = sc.student_id " \
                            " and teacher.course_id = sc.course_id " \
                            " and sc.course_id=%d" % int(course_id)
    cursor.execute(sql_teacher_course)
    raw_teacher_course = dictfetchall(cursor)
    cursor.execute(sql_student_in_course)
    raw_student = dictfetchall(cursor)
    # print('student', raw_student)
    context = {}
    context['student'] = raw_student
    context['teacher'] = raw_teacher_course
    return render(request,'student/CourseManage.html',context)

def stu_personal(request):
    userid = request.session['user']
    if userid == 0:
        return redirect('/Login/')
    cursor = connections['default'].cursor()
    context = {}
    cursor.execute('select * from student where userid=%s',(userid))
    raw = cursor.fetchone()
    print(raw)
    print(raw[0])
    context['userid'] = raw[0]
    context['name'] = raw[1]
    context['session'] = raw[2]
    context['gender'] = raw[3]
    context['email'] = raw[4]

    if request.method == "POST":
        old_pwd = request.POST.get("old_password", None)
        new_pwd = request.POST.get("new_password", None)
        check_pwd = request.POST.get("check_password", None)

        if request.session['user']:
            if old_pwd != request.session['password']:
                return HttpResponse('密码验证失败，请重试！')

            if new_pwd and new_pwd == check_pwd:
                sql_change = "update user set password = %s where user.userid= %s "
                param = (new_pwd, userid)
                cursor.execute(sql_change, param)
                return redirect('/Login/', context={'密码已修改，请重试'})

    cursor.close()
    return render(request, 'student/personal.html', context)


def logout(request):
    request.session['user'] = 0
    request.session['group'] = 0
    return redirect("/Login/")

def homepage(request):
    return render(request, 'homepage.html')