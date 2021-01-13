"""RUC_Equip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import views_equip

urlpatterns = [
    # 登陆与注册
    path('Register/',views.Register),
    path('register/',views.Register),
    path('Login/', views.Login),
    path('logout/', views.logout),
    path('homepage/',views.homepage),

    # Teacher
    path('teacher/Teacher/', views.index_teacher),
    # 课题组管理
    path('teacher/CourseManage/', views.CourseManage),
    path('teacher/DeleteStudentFromCourse/',views.DeleteStudentFromCourse),
    path('teacher/AddStudentToCourse/', views.AddStudentToCourse),
    # 预约审批
    path('teacher/Check/', views.Check),
    path('teacher/Agree/', views.Agree),
    path('teacher/Reject/', views.Reject),
    # 日志查询与仪器查询
    path('teacher/QueryLog/', views.QueryLog),
    path('teacher/QueryInstru/', views.QueryInstru),
    path('teacher/EquipDetails/', views.EquipDetails),
    # 个人主页
    path('teacher/TeacherPersonal/',views.TeacherPersonal),

    # Equip
    path('equip/personal/', views_equip.personal),
    path('equip/index/', views_equip.index),
    # 预约审批
    path('equip/widgets/', views_equip.widgets),
    path('equip/agree/', views_equip.agree),
    path('equip/reject/', views_equip.reject),
    # 我管理的仪器
    path('equip/tables/', views_equip.tables),  # 我管理的仪器
    path('equip/repair/', views_equip.repair),  # 已修复
    path('equip/scrap/', views_equip.scrap),  # 报废，删除仪器信息
    path('equip/breakdown/', views_equip.breakdown),  # 故障
    path('equip/detail/', views_equip.detail),  # 仪器详细信息
    path('equip/update/', views_equip.update),  # 更新
    path('equip/check/', views_equip.check),  # 仪器使用资格导入
    path('equip/withdraw/', views_equip.withdraw),  # 仪器使用资格撤销
    path('equip/qualification/', views_equip.qualification), # 查看仪器使用资格
    path('equip/insert/', views_equip.insert),  # 插入
    # 仪器使用日志
    path('equip/log/', views_equip.log),
    # 仪器查询
    path('equip/query/', views_equip.query_instru),
    path('equip/query_details/', views_equip.query_details),


    #student
    path('student/', views.index),
    path('logs/', views.Logs),
    path('log_edit/', views.Log_Edit),
    path('done_log/', views.Check_Log),
    path('calendar/', views.Calen),
    path('arrange/', views.Arrange),
    path('reservation_log/', views.Res),
    path('submit_log/', views.submit_log),
    path('save_log/', views.save_log),
    path('cancel_res/', views.cancel_res),
    path('stu_query_instru/', views.stu_QueryInstru),
    path('stu_equip_details/', views.stu_EquipDetails),
    path('EquipDetails/', views.stu_EquipDetails),
    path('stu_Group/', views.stu_CourseManage),
    #path('Login/', views.Login),
    #path('Register/', views.Register),
    path('stu_personal/', views.stu_personal),
    #path('register/', views.Register),


]
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]
