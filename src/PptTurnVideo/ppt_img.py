import os
import subprocess
import time
import sys
import traceback


def check_libreoffice():
    """检查是否安装了LibreOffice"""
    try:
        # Windows系统
        if sys.platform == "win32":
            # 检查常见的安装路径
            common_paths = [r"C:\Program Files\LibreOffice\program\soffice.exe"]
            for path in common_paths:
                if os.path.exists(path):
                    return path
            return None
        else:
            # Linux/Mac系统
            result = subprocess.run(['which', 'soffice'], capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def kill_libreoffice_processes():
    """终止所有LibreOffice进程"""
    try:
        if sys.platform == "win32":
            subprocess.run(['taskkill', '/F', '/IM', 'soffice.exe', '/IM', 'soffice.bin'], 
                         capture_output=True)
        else:
            subprocess.run(['killall', 'soffice.bin'], capture_output=True)
    except Exception:
        pass


def ppt_to_image(ppt_path, image_folder):
    """
    使用LibreOffice将PPT转换为图片
    转换过程：PPT -> PDF -> PNG
    """
    try:
        # 获取绝对路径
        abs_ppt_path = os.path.abspath(ppt_path)
        abs_image_folder = os.path.abspath(image_folder)
        
        print(f"PPT文件路径: {abs_ppt_path}")
        print(f"输出文件夹: {abs_image_folder}")

        # 检查文件是否存在
        if not os.path.exists(abs_ppt_path):
            print(f"错误：PPT文件不存在 - {abs_ppt_path}")
            return

        # 检查LibreOffice
        soffice_path = check_libreoffice()
        if not soffice_path:
            print("错误：未找到LibreOffice，请先安装LibreOffice")
            return

        # 创建输出目录
        os.makedirs(abs_image_folder, exist_ok=True)

        # 确保没有LibreOffice进程在运行
        kill_libreoffice_processes()
        time.sleep(1)  # 等待进程完全终止

        try:
            # 使用LibreOffice转换PPT为PDF
            print("正在将PPT转换为PDF...")
            
            # 构建LibreOffice命令
            if sys.platform == "win32":
                cmd = [
                    soffice_path,
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', abs_image_folder,
                    abs_ppt_path
                ]
            else:
                cmd = [
                    'soffice',
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', abs_image_folder,
                    abs_ppt_path
                ]

            # 执行转换命令
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(f"转换失败: {stderr.decode()}")
                return

            # 检查PDF是否生成
            pdf_path = os.path.join(abs_image_folder, 
                                  os.path.splitext(os.path.basename(abs_ppt_path))[0] + '.pdf')
            if not os.path.exists(pdf_path):
                print("PDF文件生成失败")
                return

            print("PDF转换完成，开始转换为图片...")

            # 使用pdftoppm转换PDF为图片
            if sys.platform == "win32":
                # Windows下使用pdftoppm（需要安装poppler）
                poppler_path = r"E:\AIdev\LangChain\poppler-24.08.0\Library\bin"  # 根据实际安装路径修改
                if not os.path.exists(poppler_path):
                    print("请先安装poppler-windows：")
                    print("下载地址：https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0")
                    return
                
                cmd = [
                    os.path.join(poppler_path, 'pdftoppm'),
                    '-png',  # 输出PNG格式
                    '-r', '300',  # 设置DPI为300，提高图片质量
                    pdf_path,
                    os.path.join(abs_image_folder, 'slide')
                ]
            else:
                # Linux/Mac下直接使用pdftoppm
                cmd = [
                    'pdftoppm',
                    '-png',
                    '-r', '300',  # 设置DPI为300，提高图片质量
                    pdf_path,
                    os.path.join(abs_image_folder, 'slide')
                ]

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(f"图片转换失败: {stderr.decode()}")
                return

            # 重命名输出文件（pdftoppm生成的文件名格式为slide-01.png, slide-02.png等）
            for old_name in sorted(os.listdir(abs_image_folder)):
                if old_name.startswith('slide-') and old_name.endswith('.png'):
                    new_name = f"{int(old_name[6:-4])}.png"
                    old_path = os.path.join(abs_image_folder, old_name)
                    new_path = os.path.join(abs_image_folder, new_name)
                    os.rename(old_path, new_path)
                    print(f"已生成: {new_path}")

            # 删除临时PDF文件
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

            print("\n转换完成！")
            print(f"输出目录: {abs_image_folder}")

        finally:
            # 清理LibreOffice进程
            kill_libreoffice_processes()

    except Exception as e:
        print(f"\n处理PPT时出错: {str(e)}")
        print("详细错误信息:")
        print(traceback.format_exc())
        print("\n请检查：")
        print("1. 是否已安装LibreOffice")
        print("2. 是否已安装poppler（用于PDF转图片）")
        print("3. 文件路径是否正确")
        print("4. 是否有足够的系统权限")


if __name__ == "__main__":
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置测试文件路径
    test_ppt = os.path.join(current_dir, "downloaded_file.pptx")
    output_dir = os.path.join(current_dir, "output_images")
    
    print(f"当前目录: {current_dir}")
    print(f"PPT文件: {test_ppt}")
    print(f"输出目录: {output_dir}\n")
    
    ppt_to_image(test_ppt, output_dir)
