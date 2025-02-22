import os
import comtypes.client


def ppt_to_image(ppt_path, image_folder):
    # 增强型文件检查
    if not os.path.exists(ppt_path):
        print(f"错误：PPT文件不存在 - {ppt_path}")
        print("请检查：")
        print("1. 使用绝对路径（如 D:\\file.pptx）")
        print("2. 路径不要超过260个字符")
        print("3. 避免使用中文和特殊符号")
        return

    # 强化输出目录处理
    try:
        # 转换为标准化的绝对路径
        image_folder = os.path.abspath(image_folder)

        # 创建目录并设置权限
        if not os.path.exists(image_folder):
            os.makedirs(image_folder, exist_ok=True)
            # 设置完全控制权限（Windows有效）
            os.chmod(image_folder, 0o777)
            print(f"已创建可写目录：{image_folder}")

        # 验证目录可写性
        if not os.access(image_folder, os.W_OK):
            raise PermissionError(f"拒绝写入：{image_folder}")

    except Exception as e:
        print(f"目录准备失败：{str(e)}")
        print("解决方案：")
        print("1. 尝试简单路径（如 D:\\output）")
        print("2. 右键以管理员身份运行")
        print("3. 关闭杀毒软件临时测试")
        return

    # 初始化PowerPoint实例
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1  # 保持可见用于调试

    try:
        print(f"正在打开：{ppt_path}")
        presentation = powerpoint.Presentations.Open(ppt_path)

        # 验证幻灯片
        if presentation.Slides.Count == 0:
            print("警告：空PPT文件")
            return

        # 增强型导出循环
        for idx in range(1, presentation.Slides.Count + 1):
            # 使用原始字符串处理路径
            output_path = os.path.join(image_folder, fr"{idx}.png")
            print(f"正在导出第 {idx} 张 -> {output_path}")

            try:
                # 显式释放资源后导出
                presentation.Slides(idx).Export(output_path, "PNG")
            except Exception as e:
                print(f"导出失败：{str(e)}")
                print("应急方案：")
                print(f"1. 尝试手动创建目录：{image_folder}")
                print("2. 使用8.3短路径格式（cmd输入 dir /x 查看）")
                continue

        print("导出完成！")
        presentation.Close()

    except Exception as e:
        print(f"\n致命错误：{str(e)}")
        print("终极解决方案：")
        print("1. 将PPT另存为新副本")
        print("2. 使用纯英文路径（如 C:\\ppt）")
        print("3. 安装Office 2016+版本")
    finally:
        powerpoint.Quit()
        print("已清理PowerPoint进程")


# 测试用例（使用最简路径）
if __name__ == "__main__":
    # 示例路径（推荐格式）
    test_ppt = r"D:\PROJECT\Python\test01\PptTurnVideo\downloaded_file.pptx"
    output_dir = "output_images1"

    ppt_to_image(test_ppt, output_dir)