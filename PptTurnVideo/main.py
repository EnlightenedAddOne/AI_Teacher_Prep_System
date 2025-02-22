import os
from PptTurnVideo.creat_vido import natural_sort_key, generate_audio_files, create_video_from_images
from PptTurnVideo.ppt_img import ppt_to_image
from PptTurnVideo.ppt_txt import extract_speaker_notes
from PptTurnVideo.xfPPT import main_create_ppt


# 示例调用
def main():
    # 文件路径
    output_folder = 'output_images1'
    output_video_path = 'output_video.mp4'
    ppt_path = 'downloaded_file.pptx'


    # ppt生成
    # APPId和APISecret从控制台获取
    APPId = "5f1edb16"
    APISecret = "d50e3011f50b9aa6b14f46b75dfda974"
    templateId = "20240731F237950"  # 该模板ID，需要通过getTheme() 方法获取模板列表，然后从中挑选
    # ppt大纲
    ppt_outline = """
                TCP协议概述
                TCP与OSI模型
                三次握手与四次挥手
                核心机制（分段、流量控制、拥塞控制、错误控制）
                实际应用与常见问题
                总结与对比
    """
    main_create_ppt(APPId, APISecret, ppt_outline,templateId,ppt_path) #ppt_path为生成ppt的存放路径


    # 获取ppt演讲稿内容
    slide_texts = extract_speaker_notes(ppt_path)
    # print(slide_texts)

    """**************这里应该调用ai对演讲稿进行润色**************"""

    # 将ppt转换为一张张图片
    ppt_to_image(ppt_path, output_folder)

    # 图片路径列表
    # 应用排序
    image_paths = sorted(
        [os.path.join(output_folder, fname)                                                                                                      
         for fname in os.listdir(output_folder)
         if fname.lower().endswith('.png')],
        key=natural_sort_key
    )

    # 打印图片路径列表进行调试
    print("Image Paths:", image_paths)

    # 检查图片路径列表是否为空
    if not image_paths:
        print("No image files found in the specified folder.")
    else:
        # 生成语音文件
        audio_clips = generate_audio_files(slide_texts, output_folder)

        # 创建视频
        create_video_from_images(image_paths, audio_clips, output_video_path)

        # 清理临时音频文件
        # for idx in range(len(slide_texts)):
        #     os.remove(os.path.join(output_folder, f'audio_{idx}.mp3'))


if __name__ == '__main__':
    main()