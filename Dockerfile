# 从镜像站点拷贝基础系统
FROM docker.1ms.run/library/python:3.10-slim-bullseye

ENV TZ Asia/Taipei

# 工作目录
WORKDIR /app

# 省的说我给人删了不备份
RUN touch /etc/apt/sources.list
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 换源！！
RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list


# 下个 Git
RUN apt-get update && apt-get install -y git && \
    # 清理 apt 缓存
    rm -rf /var/lib/apt/lists/*

# 克隆伶伦仓库
RUN git clone https://gitee.com/TriM-Organization/Linglun-Converter.git

# 创建 Python 虚拟环境
RUN python3 -m venv /app/venv

# 处理依赖
RUN . /app/venv/bin/activate && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    /app/venv/bin/python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade "Musicreater[full]" TrimLog requests zhDateTime "setuptools<80"

# 切换到克隆下来的仓库目录
WORKDIR /app/Linglun-Converter

# 设置容器启动时执行的默认命令，使用虚拟环境中的 python
CMD ["/app/venv/bin/python3", "llc_cli.py"]