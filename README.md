# sakura-comic-flask

动漫网站后端部分
1. 一个用于追番的动漫网站，实现了动漫视频的更新与展示，用户注册和登录，评论和回复，视频收藏的功能
2. 技术栈，前端： vue3 + vite + element plus, 后端：flask + gunicorn + mysql
3. 预览： http://139.196.138.236:8000/#/

## 下载

`git clone https://github.com/Smile-Cats/sakura-comic-flask.git`

下载后需修改 **config/config.yaml** 下配置信息

数据库建表语句: **config/create_table.sql**

## Docker 运行

cd到 DockerFile 所在的目录下，执行如下命令

构建镜像： `docker build -t sakura_comic:v1.0 .`

运行： `docker run [image_id]`

## gunicorn运行

`gunicorn --config config/gun.conf -D  wsgi_gunicorn:app`
