import os
import comtypes.client


def ppt_to_image(ppt_path, image_folder):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    ppt_path = os.path.join(script_dir, f"{ppt_path}")
    image_folder = os.path.join(script_dir, f"{image_folder}")

    # 检查并创建目标文件夹
    if not os.path.exists(image_folder):
        try:
            os.makedirs(image_folder)
            print(f"Created directory: {image_folder}")
        except Exception as e:
            print(f"Failed to create directory {image_folder}: {e}")
            return

    # 连接到PowerPoint应用
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1  # 设置PowerPoint可见

    try:
        # 打开指定的PPT文件
        presentation = powerpoint.Presentations.Open(ppt_path)

        # 循环遍历每一张幻灯片，并保存为图片
        for slide_index, slide in enumerate(presentation.Slides):
            output_path = os.path.join(image_folder, f"{slide_index + 1}.png")
            print(f"Exporting slide {slide_index + 1} to {output_path}")
            slide.Export(output_path, "PNG")

        # 关闭PPT和PowerPoint应用
        presentation.Close()
    except Exception as e:
        print(f"Error processing PPT file: {e}")
    finally:
        powerpoint.Quit()


# 使用示例
if __name__ == "__main__":
    ppt_to_image(r"D:\PROJECT\Python\test01\PptTurnVideo\深入理解TCP协议.pptx", "output_images1")

