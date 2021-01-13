# RUC_Equip

数据库课程设计，以学生、老师、仪器辅导员三种身份参与的大型仪器预约管理平台。

项目实现使用`python3.7`， `mysql`，`Django`， 其中 $Mysql$ 数据库部分使用 $\text{phpmyadmin}$ 进行图形页面管理。数据库创建语句见 $\text{new.sql}$，可直接导入 $phpmyadmin$ 构建数据库。

#### 安装及部署说明：

**1）** 在/RUC_Equip路径下配置Django环境，Django版本大于2.0。

**2）** 在mysql中导入new.sql,将创建一个名为equipment的数据库。

**3）** 执行python manage.py migrate 以及 python manage.py runserver

```sh
cd RUC_Equip
python manage.py migrate
python manage.py runserver
```

![save.jpg](https://github.com/Guan-JW/RUC_Equip/blob/main/pics/save.jpg?raw=true)

**4）** 进入http://127.0.0.1:8000/homepage 到达本系统主页。

<img src="https://github.com/Guan-JW/RUC_Equip/blob/main/pics/homepage.png?raw=true" alt="homepage.png" style="zoom:67%;" />

 