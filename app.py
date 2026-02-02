import streamlit as st
import subprocess
import os
import shutil
from pathlib import Path

# ================= 1. 页面基础配置 =================
st.set_page_config(
    page_title="BIOdownload v1.3",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. 侧边栏：核心设置 =================
with st.sidebar:
    st.markdown("### 🧬 BIOdownload")
    st.success("**Current Version:** v1.3 (Stable)")
    st.divider()
    
    st.header("⚙️ 参数配置")
    
    db_display = st.selectbox(
        "数据库来源 (Database)", 
        ["ena", "sra", "cra"], 
        index=0,
        format_func=lambda x: x.upper(),
        help="ENA(欧洲/快), SRA(美国/全), CRA(中国/GSA)"
    )
    
    db_map = {"ena": "ena", "sra": "sra", "cra": "gsa"}
    database = db_map[db_display]

    st.divider()

    st.write("📂 **存储位置设置**")
    BASE_MOUNT_POINT = "/data"
    
    # 自动获取已存在的项目文件夹
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

    # 最终输出路径
    final_output_path = os.path.join(BASE_MOUNT_POINT, sub_folder_name)
    st.info(f"💾 宿主机存储路径:\n`{final_output_path}`")

    st.divider()

    threads = st.slider("并行线程 (Threads)", 1, 16, 8)
    use_gzip = st.checkbox("GZIP压缩 (.gz)", value=True)
    convert_fastq = st.checkbox("转FASTQ (-q)", value=True)

# ================= 3. 主页面内容 =================
st.title("🧬 BIOdownloadHTML")
st.caption(f"当前模式: **{db_display.upper()}** | 项目目录: `{sub_folder_name}`")

input_text = st.text_area(
    "粘贴 Accession ID (每行一个)", 
    height=150,
    placeholder="SRP549461\nSRR123456"
)

status_container = st.empty()

# ================= 4. 下载逻辑 =================
if st.button("🚀 开始下载任务", type="primary"):
    # 严格清理输入的 ID
    ids = [line.strip() for line in input_text.splitlines() if line.strip()]
    
    if not ids:
        st.warning("⚠️ 请输入有效的 ID")
    else:
        # 确保根目录存在
        root_path = Path(final_output_path)
        root_path.mkdir(parents=True, exist_ok=True)

        progress_bar = st.progress(0, text="准备中...")
        
        for i, acc_id in enumerate(ids):
            status_container.info(f"⏳ ({i+1}/{len(ids)}) 正在处理: **{acc_id}**")
            progress_bar.progress(i / len(ids), text=f"正在下载 {acc_id}...")

            # --- 【关键修复】临时文件存放在 /tmp，不干扰下载目录 ---
            temp_input_file = Path(f"/tmp/input_{acc_id}.txt")
            with open(temp_input_file, "w", encoding="utf-8") as f:
                f.write(acc_id + "\n") 

            # 构建 iseq 命令
            # 注意：-o 指向父目录，iseq 会自动在里面创建 acc_id 文件夹
            cmd = [
                "iseq",
                "-i", str(temp_input_file),
                "-o", str(root_path),
                "-d", database,
                "-t", str(threads),
                "-p", "5"
            ]
            if use_gzip: cmd.append("-g")
            if convert_fastq: cmd.append("-q")

            with st.expander(f"📦 查看 {acc_id} 下载实时日志", expanded=True):
                st.code(" ".join(cmd), language="bash")
                log_box = st.empty()
                log_lines = []

                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1
                    )
                    
                    for line in process.stdout:
                        log_lines.append(line)
                        # 实时显示最后 8 行日志
                        log_box.code("".join(log_lines[-8:]), language="text")
                    
                    process.wait()

                    # --- 下载后验证 ---
                    # 检查是否有新文件夹生成，并列出文件
                    check_dir = root_path / acc_id
                    if check_dir.exists():
                        files = [f for f in check_dir.iterdir() if f.is_file()]
                        if files:
                            file_list = "\n".join([f"- {f.name} ({f.stat().st_size // (1024*1024)} MB)" for f in files])
                            st.success(f"✅ {acc_id} 下载成功！\n文件列表：\n{file_list}")
                        else:
                            st.error(f"❌ {acc_id} 文件夹已创建，但未发现文件。")
                    else:
                        st.error(f"❌ 未能创建下载目录 {acc_id}")

                except Exception as e:
                    st.error(f"运行时错误: {e}")
                finally:
                    if temp_input_file.exists():
                        os.remove(temp_input_file)

        progress_bar.progress(1.0, text="所有任务已完成")
        status_container.success(f"🎉 任务已全部结束！请检查您的存储位置。")
        st.balloons()
