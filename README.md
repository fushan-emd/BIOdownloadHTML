# 🧬 BIOdownloadHTML

**基于 Docker 的生物数据自动化下载平台 (SRA / ENA / CRA-GSA)**

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

BIOdownloadHTML 是一个轻量级、可视化的生物信息数据下载工具。它封装了 `iseq` 核心，解决了生信小白在 Windows 上配置环境难、命令行操作复杂的问题。

## ✨ 主要功能

- **小白友好**：纯图形化 Web 界面，无需敲代码。
- **多源支持**：
  - 🇺🇸 **SRA (NCBI)**: 美国数据库，数据最全。
  - 🇪🇺 **ENA (EBI)**: 欧洲数据库，下载速度通常较快。
  - 🇨🇳 **CRA (CNGB)**: 国家基因库 (GSA)，支持 CRR/SRP 等数据。
- **自动处理**：自动完成下载、SRA 转 FASTQ、GZIP 压缩全流程。
- **断点续传**：支持网络中断后的自动恢复。
- **环境隔离**：基于 Docker，不污染本地环境，即开即用。

---

## 🚀 快速开始 (推荐：Docker 方式)

只要你的电脑装了 Docker Desktop，只需一行命令即可运行。

### 1. 安装 Docker
请前往 [Docker 官网](https://www.docker.com/products/docker-desktop/) 下载并安装 Docker Desktop。

### 2. 启动软件
打开 **Windows PowerShell** (不是 WSL)，运行以下命令：

```powershell
# 假设你想把数据下载到 F 盘 (请根据实际情况修改盘符)
docker run -p 8501:8501 -v F:\:/data boyanwan/biodownload:latest
```
📝 注意：

-v F:\:/data 表示将你的 F 盘挂载到容器内。下载的数据会出现在 F:\ 下你指定的文件夹中。

Linux/Mac 用户，请使用： docker run -p 8501:8501 -v $(pwd):/data boyanwan/biodownload:latest

3. 开始使用
打开浏览器访问：http://localhost:8501

在左侧设置 数据库来源 和 保存文件夹。

输入 Accession ID (如 SRR390728)。

点击 开始下载。

### ⚡ Windows 用户懒人脚本 (.bat)
Windows 用户可以在本地创建一个名为 启动下载器.bat 的文件，粘贴以下内容。以后只需双击该文件即可自动运行，无需输入命令。

```bat
@echo off
title BIOdownloadHTML Launcher
echo Pulling latest updates...
docker pull boyanwan/biodownload:latest
echo.
set /p drive="请输入要保存数据的盘符 (例如 F 或 D): "
echo.
echo 正在启动服务... 请稍后打开 http://localhost:8501
docker run --rm -p 8501:8501 -v %drive%:\:/data boyanwan/biodownload:latest
pause
```

---

## 🛠️ 源码安装 (开发者模式)
如果你熟悉 Python/Conda 且不想使用 Docker，可以从源码运行。

前置要求
Python 3.9+

Conda (Miniconda/Anaconda)

⚠️ 注意：Windows 直接运行源码可能会遇到 iseq 依赖缺失问题，强烈建议使用 WSL 或 Docker。

安装步骤
1. 克隆仓库

```Bash
git clone [https://github.com/boyanwan/BIOdownloadHTML.git](https://github.com/boyanwan/BIOdownloadHTML.git)
cd BIOdownloadHTML
```

2. 创建环境

```Bash
# 使用清华源加速
conda config --add channels [https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/)
conda config --add channels [https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/)

# 创建环境并安装依赖
conda create -n bio_env python=3.9 iseq pip -y
conda activate bio_env
pip install streamlit
```
3. 运行应用

```Bash
streamlit run app.py
```

---

## ❓ 常见问题 (FAQ)
Q1: 为什么下载完成后文件夹是空的？

A: 这通常是网络原因导致无法连接到目标数据库。

请尝试在侧边栏切换数据库（例如从 ENA 切换到 SRA）。

检查该 ID 是否存在于你选择的数据库中。

Q2: CRA (CNGB) 数据怎么下载？

A: 在侧边栏数据库选择 CRA。请注意，CRA 下载使用的是 gsa 接口，ID 通常以 CRR 或 SRP 开头。

Q3: 如何停止正在进行的下载？

A: 点击网页右上角的 "Stop" 按钮，或者直接刷新网页（F5），后台进程会自动终止。

Q4: 我可以用它下载受控数据 (dbGaP) 吗？

A: 不支持。本工具仅支持公开数据（Public Data）。受控数据需要特定的密钥和权限，请使用官方 prefetch 工具。

---

📄 License
本项目基于 MIT License 开源。
