# 1. 基础镜像
FROM continuumio/miniconda3

# 2. 设置工作目录
WORKDIR /app

# 3. 【核心修复】安装缺失的 Linux 系统工具 (file)
# miniconda3 镜像太精简了，必须手动补上这个工具
RUN apt-get update && \
    apt-get install -y file procps && \
    rm -rf /var/lib/apt/lists/*

# 4. 配置清华源并安装 python 环境
# 直接在内部配置，确保不读取旧缓存
RUN conda config --set ssl_verify false && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    conda config --set show_channel_urls yes && \
    conda create -n bio_env -y python=3.9 iseq pip && \
    conda clean -afy

# 5. 使用 pip 安装 streamlit
RUN /opt/conda/envs/bio_env/bin/pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple

# 6. 设置环境变量
SHELL ["conda", "run", "-n", "bio_env", "/bin/bash", "-c"]
ENV PATH=/opt/conda/envs/bio_env/bin:$PATH

# 7. 复制项目代码
COPY .streamlit .streamlit
COPY app.py .

# 8. 启动
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]