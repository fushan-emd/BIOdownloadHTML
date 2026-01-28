import streamlit as st
import subprocess
import os
import shutil
import time
from pathlib import Path

# ================= 1. 页面基础配置 =================
st.set_page_config(
    page_title="BIOdownloadHTML",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. 侧边栏：核心设置 =================
with st.sidebar:
    st.header("⚙️ 参数配置")
    
    # --- 【新增】数据库选择 (支持 CRA) ---
    db_display = st.selectbox(
        "数据库来源 (Database)", 
        ["ena", "sra", "cra"], 
        index=0,
        format_func=lambda x: x.upper(), # 让选项显示大写
        help="ENA(欧洲/快), SRA(美国/全), CRA(中国/GSA)"
    )
    
    # 内部参数映射：CRA 在 iseq/kingfisher 中通常叫 gsa
    db_map = {
        "ena": "ena",
        "sra": "sra",
        "cra": "gsa"  # 核心映射
    }
    database = db_map[db_display]

    st.divider()

    # --- 下载位置 ---
    st.write("📂 **存储位置设置**")
    BASE_MOUNT_POINT = "/data"
    
    folder_options = ["➕ 新建文件夹..."]
    try:
        if os.path.exists(BASE_MOUNT_POINT):
            existing_dirs = [
                d.name for d in Path(BASE_MOUNT_POINT).iterdir() 
                if d.is_dir() and not d.name.startswith(".")
            ]
            existing_dirs.sort()
            folder_options.extend(existing_dirs)
    except Exception:
        pass

    selected_folder = st.selectbox("选择目标文件夹", options=folder_options)

    if selected_folder == "➕ 新建文件夹...":
        sub_folder_name = st.text_input("新文件夹名称", value="New_Project")
        sub_folder_name = sub_folder_name.strip().replace(" ", "_")
    else:
        sub_folder_name = selected_folder

    final_output_path = os.path.join(BASE_MOUNT_POINT, sub_folder_name)
    st.info(f"💾 保存至:\n`{final_output_path}`")

    st.divider()

    # --- 性能 ---
    threads = st.slider("线程数", 1, 16, 8)
    use_gzip = st.checkbox("GZIP压缩 (.gz)", value=True)
    convert_fastq = st.checkbox("转FASTQ", value=True)

# ================= 3. 主页面内容 =================
col_title, col_stop = st.columns([0.8, 0.2])
with col_title:
    st.title("🧬 BIOdownloadHTML")
with col_stop:
    # 提示用户如何停止
    st.warning("🛑 如需中止：请点击浏览器右上角的 'Stop' 或直接刷新页面")

st.caption(f"当前模式: **{db_display.upper()}** Database")

input_text = st.text_area(
    "在此粘贴 Accession ID (支持 SRR/ERR/CRR... 每行一个)", 
    height=150,
    placeholder="SRR390728\nCRR123456"
)

status_container = st.empty()

# ================= 4. 下载逻辑 =================
if st.button("🚀 开始下载任务", type="primary"):
    ids = [line.strip() for line in input_text.split('\n') if line.strip()]
    
    if not ids:
        st.warning("⚠️ 请先输入 ID")
    else:
        # 创建目录
        try:
            Path(final_output_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            st.error(f"无法创建目录: {e}")
            st.stop()

        progress_bar = st.progress(0, text="初始化中...")
        total_tasks = len(ids)

        for i, acc_id in enumerate(ids):
            # 状态更新
            status_container.info(f"⏳ ({i+1}/{total_tasks}) 正在从 {db_display.upper()} 下载: **{acc_id}**")
            progress_bar.progress(i / total_tasks, text=f"Processing {acc_id}...")

            task_dir = Path(final_output_path) / acc_id
            task_dir.mkdir(parents=True, exist_ok=True)
            
            # --- 【修复】写入文件时必须加换行符 ---
            temp_input_file = task_dir / "input_temp.txt"
            with open(temp_input_file, "w") as f:
                f.write(acc_id + "\n") 

            # 构建命令 (自动使用 gsa 参数如果选了 cra)
            cmd = [
                "iseq",
                "-i", str(temp_input_file),
                "-o", str(task_dir),
                "-d", database,  # 这里已经是转换过的 gsa 了
                "-t", str(threads),
                "-p", "5"
            ]
            if use_gzip: cmd.append("-g")
            if convert_fastq: cmd.append("-q")

            # 显示日志
            with st.expander(f"查看 {acc_id} 实时日志", expanded=True):
                st.code(" ".join(cmd), language="bash")
                log_box = st.empty()
                log_lines = []

                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, # 把错误流也合并进来
                        text=True,
                        bufsize=1
                    )
                    
                    for line in process.stdout:
                        log_lines.append(line)
                        log_box.code("".join(log_lines[-15:]), language="text")
                    
                    process.wait()

                    if process.returncode == 0:
                        st.success(f"✅ {acc_id} 完成")
                    else:
                        st.error(f"❌ {acc_id} 失败 (Exit: {process.returncode})")
                        # 如果是 CRA 下载失败，提示可能是没找到
                        if database == "gsa":
                            st.caption("💡 提示: CRA 数据有时不稳定，请确认 ID 是否以 CRR/SRP 开头。")

                except Exception as e:
                    st.error(f"Error: {e}")

            if temp_input_file.exists():
                os.remove(temp_input_file)

        progress_bar.progress(1.0, text="任务完成")
        status_container.success(f"🎉 全部结束！数据在: {sub_folder_name}")
        st.balloons()