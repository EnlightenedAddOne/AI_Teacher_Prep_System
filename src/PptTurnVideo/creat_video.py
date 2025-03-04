# 合成视频
import os
import re
import time

import edge_tts
import numpy as np
from moviepy import AudioFileClip, ImageSequenceClip, concatenate_audioclips

# 声线映射字典
VOICE_TYPE_MAPPING = {
    "年轻男声": "zh-CN-YunxiNeural",
    "温暖女声": "zh-CN-YunxiaNeural",
    "播音男声": "zh-CN-YunyangNeural",
    "甜美女声": "zh-CN-XiaoxiaoNeural",
    "活泼女声": "zh-CN-XiaoyiNeural"
}


def get_edge_voice_type(voice_type: str) -> str:
    """
    获取Edge TTS使用的声线代码
    :param voice_type: 中文声线名称
    :return: Edge TTS声线代码
    :raises ValueError: 如果声线类型不支持
    """
    if voice_type not in VOICE_TYPE_MAPPING:
        valid_voices = list(VOICE_TYPE_MAPPING.keys())
        raise ValueError(f"不支持的声线类型。支持的声线类型: {', '.join(valid_voices)}")
    return VOICE_TYPE_MAPPING[voice_type]


async def generate_audio_edge(text, output_file, voice='年轻男声'):
    """
    使用Edge TTS生成音频文件
    :param text: 要转换的文本
    :param output_file: 输出文件路径
    :param voice: 中文声线名称
    :return: 是否成功
    """
    try:
        edge_voice = get_edge_voice_type(voice)
        communicate = edge_tts.Communicate(
            text=text,
            voice=edge_voice,
            rate="+5%",  # 语速调整(-50% ~ +100%)
            volume="+0%"  # 音量调整(-50% ~ +50%)
        )
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"⚠️ 语音生成失败：{str(e)}")
        return False


def create_silent_audio(duration, output_file):
    """生成指定时长的静音音频文件"""
    # 创建一个持续时间为duration秒的静音音频数组
    sample_rate = 44100
    np.zeros(int(duration * sample_rate))

    # 使用 moviepy 创建音频剪辑
    audio = ImageSequenceClip([np.zeros((1, 1, 3))], fps=1).set_duration(duration)
    audio = audio.set_audio(None)  # 确保没有音频

    # 保存为音频文件
    audio.write_audiofile(output_file, fps=sample_rate)
    return AudioFileClip(output_file)


async def generate_audio_files(slide_texts, output_folder, voice_type='年轻男声'):
    """
    生成所有音频文件（带进度显示）
    :param slide_texts: 幻灯片文本列表
    :param output_folder: 输出文件夹
    :param voice_type: 中文声线名称
    :return: 音频片段列表
    """
    audio_clips = []
    total = len(slide_texts)
    start_time = time.time()
    failed = 0  # 失败计数器

    print(f"🎙️ 开始生成音频（共{total}段）")
    print(f"🎤 使用声线: {voice_type}")

    for idx, text in enumerate(slide_texts):
        # 进度显示
        progress = f"[{idx + 1}/{total}]".ljust(8)
        percent = (idx + 1) / total * 100
        print(f"\n{progress} 📌 第{idx + 1}段音频生成中（{percent:.1f}%）...")

        if not text.strip():
            text = "此幻灯片无备注内容"

        audio_file = os.path.join(output_folder, f"audio_{idx}.mp3")

        # 带重试机制的生成
        success = False
        for retry in range(3):
            try:
                print(f"   🔄 尝试第{retry + 1}次生成...")
                success = await generate_audio_edge(text, audio_file, voice=voice_type)
                if success:
                    print(f"   ✅ 第{retry + 1}次尝试成功")
                    break
            except Exception as e:
                print(f"   ❌ 第{retry + 1}次尝试失败：{str(e)}")

        # 失败处理
        if not success:
            failed += 1
            print(f"   ⚠️ 最终生成失败，使用静音替代")
            # 使用5秒的静音音频替代
            audio_clips.append(create_silent_audio(5, audio_file))
        else:
            audio_clips.append(AudioFileClip(audio_file))

    # 生成结果统计
    time_cost = time.time() - start_time
    print(f"\n🎉 音频生成完成！共{total}段")
    print(f"⏱️ 总耗时：{time_cost:.1f}秒")
    print(f"✅ 成功率：{(total - failed) / total * 100:.1f}%")

    return audio_clips


def create_video_from_images(image_paths, audio_clips, output_video_path):
    if not image_paths:
        raise ValueError("No image files found in the specified folder.")

    durations = [audio.duration for audio in audio_clips]

    # 确保图片数量与音频数量匹配
    if len(image_paths) != len(durations):
        raise ValueError(f"Mismatch between number of images ({len(image_paths)}) and audio clips ({len(durations)}).")

    # 创建图片序列剪辑
    clip = ImageSequenceClip(image_paths, durations=durations)

    # 合并所有音频片段
    final_audio = concatenate_audioclips(audio_clips)

    # 将图片序列剪辑转换为视频剪辑并添加音频
    final_clip = clip.with_audio(final_audio)

    # 输出视频
    final_clip.write_videofile(output_video_path, codec='libx264')


# 自然排序函数（处理纯数字文件名）
def natural_sort_key(file_path):
    """提取文件名中的数字进行排序"""
    filename = os.path.basename(file_path)
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else filename
