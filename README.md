# dailyfresh天天生鲜项目
## 项目分析

1. django框架，非前后端分离模式
2. 利用django渲染页面数据
3. 改变了`manage.py`文件位置，其他符合django的目录结构


## 操作顺序
### 基本操作
1. `docker-compose up --build`创建并启动容器
2. `docker-compose up` 启动
### 启动文件位置
1. 数据库组件： `db_handler/docker-compose.yml`   
2. 项目

### 启动项目
1. 启动数据库组件 
```bash
# 启动数据库组件例子：
cd db_handler
docker-compose up --build
```
2. 打开adminer，创建数据库
    - 浏览器打开 `0.0.0.0:4446`
    - 输入服务器、用户名、密码（见settings文件）
    - 创建数据库`dailyfresh`，字符集选择`utf8mb4_unicode_ci`
3. 执行`python manage.py migrate`进行数据库建表
4. 执行`python manage.py createsuperuser`创建超级用户
5. 执行`python manage.py rebuild_index`初始化haystack索引数据
5. 访问http://0.0.0.0:4444/admin/  可进入admin后台
6. 访问首页会报错，因为数据库没有数据。这里loaddata还没写。。。
123
