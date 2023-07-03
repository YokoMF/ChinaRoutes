FROM python:3.9.13-slim
LABEL  maintainer Xi Siyuan "yokoxsy@msn.com"

WORKDIR /ChinaRoutes
COPY requirements /tmp
RUN cd  /tmp \
    && python -m pip install -r requirements  -i https://mirrors.aliyun.com/pypi/simple/  \
    && rm * \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

COPY  china_ip_list \
      delegated-apnic-latest \
      ipv4-address-space.csv  \
      routes4.conf \
      routes6.conf \
      *.py \
      ./
COPY  modules  ./modules

CMD ["python"]
