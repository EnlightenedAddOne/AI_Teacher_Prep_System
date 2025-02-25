import os
import time
import asyncio
from configs import config
from PptTurnVideo import (natural_sort_key, generate_audio_files,
                          create_video_from_images, ppt_to_image,
                          extract_speaker_notes, main_create_ppt, ppt_outline)


async def create_ppt_videos(api_key, subject, topic, voice_type='年轻男声'):
    """
    生成PPT视频
    :param api_key: DeepSeek API密钥
    :param subject: 学科名称
    :param topic: 课程主题
    :param voice_type: 中文声线类型
    :return: 生成的视频路径
    """
    # 设置固定输出目录
    base_output_dir = r'E:\AIdev\LangChain\host_2\Langchain\output\Ppt-turn-video'
    timestamp = str(int(time.time()))
    output_dir = os.path.join(base_output_dir, f'video_{timestamp}')
    output_video_path = os.path.join(output_dir, "output.mp4")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 设置PPT文件路径
    ppt_path = os.path.join(output_dir, "presentation.pptx")
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # ppt生成
    APPId = config['ppt_xh']['APPId']
    APISecret = config['ppt_xh']['APISecret']
    templateId = "20240731F237950"  # 该模板ID，需要通过getTheme() 方法获取模板列表，然后从中挑选
    
    # ppt大纲
    ppt_outlines = ppt_outline(api_key, subject, topic)
    main_create_ppt(APPId, APISecret, ppt_outlines, templateId, ppt_path)  # ppt_path为生成ppt的存放路径

    # 获取ppt演讲稿内容
    slide_texts = extract_speaker_notes(ppt_path)
    print(slide_texts)

    # 将ppt转换为一张张图片
    ppt_to_image(ppt_path, images_dir)

    # 图片路径列表
    # 应用排序
    image_paths = sorted(
        [os.path.join(images_dir, fname)
         for fname in os.listdir(images_dir)
         if fname.lower().endswith('.png')],
        key=natural_sort_key
    )

    # 打印图片路径列表进行调试
    print("Image Paths:", image_paths)

    # 检查图片路径列表是否为空
    if not image_paths:
        raise ValueError("No image files found in the specified folder.")
    
    # 生成语音文件
    audio_clips = await generate_audio_files(slide_texts, images_dir, voice_type)

    # 创建视频
    create_video_from_images(image_paths, audio_clips, output_video_path)

    return output_video_path


if __name__ == '__main__':
    subject = "计算机网络"
    topic = "网络协议"
    voice_type = "年轻男声"
    deepseek_api_key = "sk-1e4ec15f97a044ab8fca717279a9cbea"
    asyncio.run(create_ppt_videos(api_key=deepseek_api_key, subject=subject, topic=topic, voice_type=voice_type))
