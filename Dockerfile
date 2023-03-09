#基于的基础镜像
FROM python:3.7

#代码添加到code文件夹
ADD . /comic_sakura

# 设置sakura_comic文件夹是工作目录
WORKDIR /comic_sakura

# 安装支持
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple

CMD ["flask", "run", "-h", "0.0.0.0"]