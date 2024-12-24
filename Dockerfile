FROM tensorflow/tensorflow:2.18.0-gpu
LABEL GitRepo=#GIT_URL

ENV DEBIAN_FRONTEND=noninteractive
ENV app_env=test
WORKDIR /app

ADD requirements.txt ./


RUN pip install --default-timeout=600 -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
RUN pip install numpy==1.26.4 --default-timeout=600 -i https://mirrors.aliyun.com/pypi/simple/
COPY . .



RUN mkdir -p logs

ENV TZ Asia/Shanghai
# 暴露应用程序监听的端口
EXPOSE 11000
