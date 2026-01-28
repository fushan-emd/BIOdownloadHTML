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
注意：

-v F:\:/data 表示将你的 F 盘挂载到容器内。下载的数据会出现在 F:\ 下你指定的文件夹中。

如果你是 Linux/Mac 用户，请使用 -v /your/path:/data。

3. 开始使用
打开浏览器访问：http://localhost:8501

在左侧设置 数据库来源 和 保存文件夹。

输入 Accession ID (如 SRR390728)。

点击 开始下载。