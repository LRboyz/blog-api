FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

# 拷贝安装python包清单
COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
