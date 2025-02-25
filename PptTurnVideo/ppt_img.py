import os
import comtypes.client


def ppt_to_image(ppt_path, img_folder):
    """
    将给定的PPT文件中的每一页转换为图片，并保存在指定的文件夹中。
    每转换一张幻灯片为图片后，打印其保存路径。

    :param ppt_path: PPT文件的路径
    :param img_folder: 输出图片文件夹的路径
    """
    # 创建输出文件夹如果不存在的话
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # 连接PowerPoint应用
    powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
    try:
        # 打开指定的PPT
        presentation = powerpoint.Presentations.Open(ppt_path)

        # 循环遍历每一页，并将其保存为图片
        for slide_index, slide in enumerate(presentation.Slides):
            img_path = os.path.join(img_folder, f'{slide_index + 1}.png')
            # 使用Slide的内置属性获取尺寸并导出
            slide.Export(img_path, 'PNG')
            print(f"已保存: {img_path}")  # 打印图片保存路径

        # 关闭PPT
        presentation.Close()
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 退出PowerPoint应用
        powerpoint.Quit()


# 示例调用
ppt_path = os.path.abspath(r'D:\PROJECT\Python\test01\PptTurnVideo\downloaded_file.pptx')
img_folder = os.path.abspath(r'D:\PROJECT\Python\test01\PptTurnVideo\output_images1')
ppt_to_image(ppt_path, img_folder)


