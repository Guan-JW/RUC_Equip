from django.shortcuts import render,redirect
import json
from django.db import connections
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import os
from pathlib import Path

from django.contrib import auth

BASE_DIR = Path(__file__).resolve().parent.parent

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]


"""我的资料"""
def personal(request):
	context = {}
	manager_id = request.session.get('user')
	if(manager_id):
		cursor = connections['default'].cursor()
		cursor.execute("select * from equipmanager where manager_id = " + manager_id)
		info = dictfetchall(cursor)[0]
		context['info'] = info

		"""
		if request.method == "POST":
			old_pwd = request.POST.get("old_password", None)
			new_pwd = request.POST.get("new_password", None)
			check_pwd = request.POST.get("check_password", None)

			if old_pwd != request.session['password']:
				return HttpResponse('密码验证失败，请重试！')
			
			if new_pwd and new_pwd == check_pwd:
				sql_change = "update user set password = %s where user.userid= %s "
				param = (new_pwd,manager_id)
				cursor.execute(sql_change,param)
				return redirect('/Login/',context={'密码已修改，请重试'})
		"""
		if request.method == "POST":
			old_pwd = request.POST.get("old_password", None)  # 获取旧密码
			new_pwd = request.POST.get("new_password", None)  # 获取新密码
			check_pwd = request.POST.get("check_password", None)  # 核对新密码
		# user = auth.authenticate(request, username=userid, password=old_pwd)
			pwd = request.session['password']
			if old_pwd == pwd:
				if new_pwd and new_pwd == check_pwd:
					cursor.execute('update user set password=%s where userid=%s', (new_pwd, manager_id))
			# cursor.execute('delete from auth_user where username=%s', (userid))
				# User.objects.create_user(username=userid, password=new_pwd)
					cursor.close()
					return redirect('/Login/')
				return HttpResponse('两次密码不一致，请返回重试！')
			return HttpResponse('原始密码错误，请返回重试！')
	return render(request, os.path.join(BASE_DIR, 'templates','equip','personal.html'), context)


"""仪器管理员主页"""
def index(request):
	manager_id = request.session.get('user')
	print(manager_id)
	context= {}
	if(manager_id):
		cursor = connections['default'].cursor()
		cursor.execute("select count(*) bnum from equip e, equip_manage m where status = '故障' and e.equip_id = m.equip_id and m.manager_id = " + manager_id)
		equip_breakdown = dictfetchall(cursor)[0]
		context['breakdown'] = equip_breakdown

		cursor.execute("select count(*) anum from appoint_index a, equip_manage m where a.status = '1' and a.equip_id = m.equip_id and m.manager_id = " + manager_id)
		appointing = dictfetchall(cursor)[0]
		#print(appointing)
		context['appointing'] = appointing
	return render(request, os.path.join(BASE_DIR, 'templates','equip','index.html'),context)


"""仪器预约审批"""
def widgets(request):
	manager_id = request.session.get('user')
	context          = {}
	if(manager_id):
		cursor = connections['default'].cursor()
		command = "select index_id, a.userid student_id, a.course_id, c.name course_name, t.name teacher_name, t.userid teacher_id, s.name user_name, equip_name, a.equip_id equip_id, type, a1.use_date use_date, a1.use_time start_time, a2.use_time+1 end_time, item\
				from appoint_index a, appointment a1, appointment a2, course c, teacher t, student s, equip e, equip_manage em\
				where a.status='1' AND a.course_id=c.id AND c.id=t.course_id AND a.userid=s.userid AND a.equip_id=e.equip_id AND e.equip_id=em.equip_id AND em.manager_id="+manager_id+\
				" AND a.start_id=a1.appointment_id AND a.end_id = a2.appointment_id order by index_id;"
		cursor.execute(command)
		appointing = dictfetchall(cursor)
		for e in appointing:
			e['use_date'] = str(e['use_date'])
		context['appointing'] = appointing

		command = "select index_id, a.userid student_id, a.course_id, c.name course_name, t.name teacher_name, t.userid teacher_id, s.name user_name, equip_name, a.equip_id equip_id, type, a1.use_date use_date, a1.use_time start_time, a2.use_time+1 end_time, item, a.status\
				from appoint_index a, appointment a1, appointment a2, course c, teacher t, student s, equip e, equip_manage em\
				where (a.status='2' OR a.status='-2') AND a.course_id=c.id AND c.id=t.course_id AND a.userid=s.userid AND a.equip_id=e.equip_id AND e.equip_id=em.equip_id AND em.manager_id="+manager_id+\
				" AND a.start_id=a1.appointment_id AND a.end_id = a2.appointment_id order by index_id;"
		cursor.execute(command)
		appointed = dictfetchall(cursor)
		for e in appointed:
			e['use_date'] = str(e['use_date'])
			if e['status'] == '2':
				e['status'] = '通过'
			else:
				e['status'] = '驳回'
		context['appointed'] = appointed
	return render(request, os.path.join(BASE_DIR, 'templates','equip','widgets.html'), context)

def agree(request):
	manager_id = request.session.get('user')
	if(manager_id):
		index_id = request.GET['index_id']
		cursor = connections['default'].cursor()
		cursor.execute("update appoint_index set status = '2' where index_id = \"%s\"" % str(index_id))
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

def reject(request):
	manager_id = request.session.get('user')
	if(manager_id):
		index_id = request.GET['index_id']
		cursor = connections['default'].cursor()
		cursor.execute("update appoint_index set status = '-2' where index_id = \"%s\"" % str(index_id))
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")


"""我管理的仪器"""
# 仪器清单
def tables(request):
	manager_id = request.session.get('user')
	context          = {}
	if(manager_id):
		cursor = connections['default'].cursor()
		cursor.execute("select * from equip e, equip_manage m where e.equip_id = m.equip_id and m.manager_id = " + manager_id + " order by e.equip_id;")
		equip_details = dictfetchall(cursor)
	
		cursor.execute("select * from equip e, equip_manage m where status = '故障' and e.equip_id = m.equip_id and m.manager_id = " + manager_id + " order by e.equip_id;")
		equip_breakdown = dictfetchall(cursor)

		context['equip'] = equip_details
		context['breakdown'] = equip_breakdown
	return render(request, os.path.join(BASE_DIR, 'templates','equip','tables.html'),context)

# 故障
def breakdown(request):
	manager_id = request.session.get('user')
	if(manager_id):
		equip_id = request.GET['equip_id']
		cursor = connections['default'].cursor()
		cursor.execute("update Equip set status = '故障' where equip_id = \"%s\"" % str(equip_id))
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 已修复
def repair(request):
	manager_id = request.session.get('user')
	if(manager_id):
		equip_id = request.GET['equip_id']
		cursor = connections['default'].cursor()
		cursor.execute("update Equip set status = '正常' where equip_id = \"%s\"" % str(equip_id))
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 报废，删除仪器信息
def scrap(request):
	manager_id = request.session.get('user')
	if(manager_id):
		equip_id = request.GET['equip_id']
		cursor = connections['default'].cursor()
		#cursor.execute("delete from equip_manage where equip_id = \"%s\"" % str(equip_id))
		cursor.execute("delete from Equip where equip_id = \"%s\"" % str(equip_id))
		
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 仪器详情
def detail(request):
	#if(request.user.is_authenticated())：
	#	print(request.user.username)
	#else：
	#	print("找不到登录用户")
	manager_id = request.session.get('user')
	context          = {}
	if(manager_id):
		equip_id = request.GET['equip_id']
		request.session['equip_id'] = equip_id
		cursor = connections['default'].cursor()
		cursor.execute("select * from Equip where equip_id = \"%s\"" % str(equip_id))
		equip_detail = dictfetchall(cursor)
		context['equip_id'] = equip_detail[0]['equip_id']
		context['equip_name'] = equip_detail[0]['equip_name']
		context['type'] = equip_detail[0]['type']
		context['address'] = equip_detail[0]['address']
		context['description'] = equip_detail[0]['description']
		context['qualification'] = equip_detail[0]['qualification']
		context['check_qualification'] = equip_detail[0]['check_qualification']
		context['buy_date'] = equip_detail[0]['buy_date']
		context['status'] = equip_detail[0]['status']

		#cursor.execute("select q.userid,name from qualification q, student s \
		#				where equip_id = " + str(equip_id)
		#				+" and s.userid = q.userid;")
		#student = dictfetchall(cursor)
		#context['student'] = student
		#print(context['student'])
	return JsonResponse(context)

# 更新
def update(request):
	manager_id = request.session.get('user')
	if(manager_id):
		target = request.GET['target']
		equip_id = request.GET['equip_id']
		equip_name = request.GET['equip_name']
		equip_type = request.GET['type']
		address = request.GET['address']
		description = request.GET['description']
		qualification = request.GET['qualification']
		check_qualification = request.GET['check_qualification']
		buy_date = request.GET['buy_date']

		cursor = connections['default'].cursor()
		#cursor.execute("update equip_manage set equip_id = \"%s\" where equip_id = \"%s\";" % (str(equip_id),str(target)))
		cursor.execute("update Equip set equip_id = \"%s\",\
						equip_name = \"%s\",\
						type = \"%s\",\
						address = \"%s\",\
						description = \"%s\",\
						qualification = \"%s\",\
						check_qualification = \"%s\",\
						buy_date = \"%s\" \
						where equip_id = \"%s\";" 
						% (str(equip_id),
						str(equip_name),
						str(equip_type),
						str(address),
						str(description),
						str(qualification),
						str(check_qualification),
						str(buy_date),
						str(target)))
		# equip_manage表由CASCADE级联自动修改
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 仪器使用资格导入
def check(request):
	manager_id = request.session.get('user')
	if(manager_id):
		sno = request.GET['sno']
		equip_id = request.GET['equip_id']
		value = '("' + sno + '","' + equip_id + '")'

		cursor = connections['default'].cursor()
		cursor.execute("insert into qualification values %s;" % value)
		# equip_manage表由CASCADE级联自动修改
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 仪器使用资格撤销
def withdraw(request):
	manager_id = request.session.get('user')
	if(manager_id):
		sno = request.GET['sno']
		equip_id = request.GET['equip_id']

		cursor = connections['default'].cursor()
		cursor.execute("delete from qualification where userid = " + str(sno) + " and equip_id = " + str(equip_id))
		# equip_manage表由CASCADE级联自动修改
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 查看仪器使用资格
def qualification(request):
	manager_id = request.session.get('user')
	context          = {}
	if(manager_id):
		equip_id = request.session.get('equip_id')
		cursor = connections['default'].cursor()
		cursor.execute("select q.userid,name from qualification q, student s \
						where equip_id = " + str(equip_id)
						+" and s.userid = q.userid;")
		student = dictfetchall(cursor)
		context['equip_id'] = equip_id
		context['student'] = student
		return render(request, os.path.join(BASE_DIR, 'templates','equip','qualification.html'),context)
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")

# 插入
def insert(request):
	manager_id = request.session.get('user')
	if(manager_id):
		equip_id = request.GET['equip_id']
		equip_name = request.GET['equip_name']
		equip_type = request.GET['type']
		address = request.GET['address']
		description = request.GET['description']
		qualification = request.GET['qualification']
		check_qualification = request.GET['check_qualification']
		buy_date = request.GET['buy_date']
		status = "正常"
		value = '("' + equip_id + '","'\
				+ equip_name + '","'\
				+ equip_type + '","'\
				+ address + '","'\
			 	+ description + '","'\
				+ qualification + '","'\
				+ check_qualification + '","'\
				+ buy_date + '","'\
				+ status + '")'
		value_em = '("' + equip_id + '","' + manager_id + '")'
		cursor = connections['default'].cursor()
		cursor.execute("insert into equip values %s;" % value)
		cursor.execute("insert into equip_manage values %s;" % value_em)
		response = HttpResponse(json.dumps({"status":1}),content_type="application/json")
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse(json.dumps({"status":0}),content_type="application/json")


"""仪器使用日志"""
def log(request):
	manager_id = request.session.get('user')
	context          = {}
	if(manager_id):
		cursor = connections['default'].cursor()
		command = "select log_id, equip_name, l.equip_id equip_id, e_status, start_time, end_time, l.userid, s.name user_name, c.name course_name, l.item, l.details \
				from equip_log l, equip e, equip_manage em, course c, student s \
				where log_status='已提交' AND l.equip_id=e.equip_id AND l.equip_id=em.equip_id AND em.manager_id="+manager_id+\
				" AND l.course_id=c.id AND l.userid=s.userid order by log_id desc;"
		cursor.execute(command)
		equip_log = dictfetchall(cursor)
		for e in equip_log:
			e['start_time'] = str(e['start_time'])
			e['end_time'] = str(e['end_time'])
		context['equip_log'] = equip_log
	return render(request, os.path.join(BASE_DIR, 'templates','equip','log.html'),context)


"""仪器查询"""
def query_instru(request):
	cursor = connections['default'].cursor()
	sql_equip = "select equip_name,equip_id,type,address,status from equip where equip_id != '-1' order by equip_id"
	cursor.execute(sql_equip)
	raw_equip = dictfetchall(cursor)
	context = {}
	context['equip'] = raw_equip
	return render(request ,os.path.join(BASE_DIR, 'templates','equip','query-instru.html'),context)

def query_details(request):
	equip_id = request.GET['equip_id']
	sql_equip_details ="select * from equip,equipmanager,equip_manage where equip.equip_id ='%s' " \
	                   "and equip.equip_id = equip_manage.equip_id " \
	                   "and equip_manage.manager_id = equipmanager.manager_id " %equip_id

	cursor = connections['default'].cursor()
	cursor.execute(sql_equip_details)
	equip_details = dictfetchall(cursor)
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