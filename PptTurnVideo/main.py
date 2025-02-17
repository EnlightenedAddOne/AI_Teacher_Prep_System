import re
import time

from gtts import gTTS
import edge_tts
import asyncio
from moviepy import AudioFileClip, ImageSequenceClip, concatenate_videoclips, concatenate_audioclips
import os

from img_ppt import ppt_to_image


# 常用中文声线：
'''
zh-CN-YunxiNeural    - 年轻男声（默认）
zh-CN-YunxiaNeural   - 温暖女声
zh-CN-YunyangNeural  - 播音男声
zh-CN-XiaoxiaoNeural - 甜美女声
zh-CN-XiaoyiNeural   - 活泼女声
'''
async def generate_audio_edge(text, output_file, voice='zh-CN-YunxiNeural'):
    """使用Edge TTS生成音频文件"""
    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,  # 语音选项见下方说明
            rate="+5%",   # 语速调整(-50% ~ +100%)
            volume="+0%"   # 音量调整(-50% ~ +50%)
        )
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"⚠️ 语音生成失败：{str(e)}")
        return False


def generate_audio_files(slide_texts, output_folder):
    """生成所有音频文件（带进度显示）"""
    audio_clips = []
    total = len(slide_texts)
    start_time = time.time()

    # 在函数开头初始化失败计数器
    failed = 0  # 新增变量

    # 创建事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print(f"🎙️ 开始生成音频（共{total}段）")

    for idx, text in enumerate(slide_texts):
        # 进度显示（关键优化点）
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
                task = loop.run_until_complete(
                    generate_audio_edge(text, audio_file)
                )
                if task:
                    success = True
                    print(f"   ✅ 第{retry + 1}次尝试成功")
                    break
            except Exception as e:
                print(f"   ❌ 第{retry + 1}次尝试失败：{str(e)}")

        # 失败处理
        if not success:
            failed += 1  # 统计失败次数
            print(f"   ⚠️ 最终生成失败，使用静音替代")
            silent_clip = AudioFileClip.silent(duration=5)
            silent_clip.write_audiofile(audio_file)

        audio_clips.append(AudioFileClip(audio_file))

    # 生成结果统计
    time_cost = time.time() - start_time
    print(f"\n🎉 音频生成完成！共{total}段")
    print(f"⏱️ 总耗时：{time_cost:.1f}秒")
    print(f"✅ 成功率：{(total - failed) / total * 100:.1f}%")

    return audio_clips

# def generate_audio_files(slide_texts, output_folder):
#     """
#     根据幻灯片内容生成音频文件
#     :param slide_texts: 幻灯片文本列表
#     :param output_folder: 输出音频文件夹
#     :return: 音频文件列表
#     """
#     audio_clips = []
#     for idx, text in enumerate(slide_texts):
#         if not text.strip():  # 如果备注为空，则使用默认文本
#             text = "This slide has no notes."

#         tts = gTTS(text=text, lang='zh')
#         audio_file = os.path.join(output_folder, f"audio_{idx}.mp3")
#         tts.save(audio_file)
#         audio_clips.append(AudioFileClip(audio_file))

#     return audio_clips


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

# 示例调用
output_folder = 'output_images1'
output_video_path = 'output_video.mp4'

# 假设你有一个包含每张幻灯片备注文本的列表
slide_texts = ["大家好，今天我们将一起深入探讨 TCP 协议，从基础到应用进行全面解析。TCP 协议作为互联网的核心协议之一，对于理解网络通信至关重要。我是今天的汇报人 XXXX，希望在这次分享中，能带给大家对 TCP 协议更深入的认识和理解。",
"在今天的分享中，我们将按照以下目录展开讨论：1. TCP 协议概述 2. TCP 与 OSI 模型 3. 三次握手与四次挥手 4. 核心机制 5. 实际应用与常见问题 6. 总结与对比",
"首先，我们来了解一下 TCP 协议的基本概念。TCP（传输控制协议）是互联网协议套件中的核心协议之一，负责确保数据包在传输过程中的完整和可靠性。它通过一系列复杂的机制，保证数据在传输过程中不会丢失、重复或乱序。TCP 协议的可靠性使其成为网络通信中不可或缺的一部分。",
"TCP 协议对应于 OSI 模型的传输层，它为应用层提供端到端的通信服务，确保数据的有序和无差错传输。在 OSI 模型中，传输层的主要职责是为应用层提供可靠的数据传输服务，而 TCP 协议正是这一层的核心实现。通过三次握手建立连接，四次挥手终止连接，TCP 协议确保了通信双方的同步和数据传输的可靠性。",
"TCP 协议在 OSI 模型中主要对应于传输层，负责端到端的通信和数据流控制，确保数据包从源端正确无误地到达目标端。传输层的主要职责是为应用层提供可靠的数据传输服务，而 TCP 协议通过其复杂的机制，如分段、流量控制、拥塞控制和错误控制，确保了这一目标的实现。三次握手和四次挥手过程进一步增强了 TCP 连接的可靠性。",
"在 OSI 模型中，TCP 协议对应于传输层，这一层的主要职责是为应用层提供可靠的数据传输服务。传输层通过端到端的通信和数据流控制，确保数据包从源端正确无误地到达目标端。TCP 协议通过三次握手建立连接，四次挥手终止连接，确保通信双方的同步和数据传输的可靠性。这种层次对应关系使得 TCP 协议在互联网通信中扮演着至关重要的角色。",
"接下来，我们详细了解一下三次握手的过程。三次握手是 TCP 连接建立的关键过程，通过客户端和服务器之间的三次报文交换来实现。第一次握手是由客户端向服务器发送一个带有 SYN 标志的报文，表示请求建立连接；第二次握手是服务器收到客户端的请求后，向客户端发送一个带有 SYN-ACK 标志的报文，表示同意建立连接并同步序列号；第三次握手是客户端再向服务器发送一个带有 ACK 标志的报文，确认收到了服务器的响应。这一过程确保了双方都已准备好并能够进行数据传输。",
"在三次握手过程中，双方还会交换初始序列号，用于后续的数据传输中对数据包的顺序进行正确排序和确认。完成三次握手后，TCP 连接从 CLOSED 状态转换到 ESTABLISHED 状态，此时数据可以开始双向传输，标志着可靠通信的开始。这一过程确保了数据传输的有序性和可靠性，为后续的通信奠定了基础。",
"四次挥手是 TCP 协议中用于终止通信连接的过程，通过发送和确认四个报文来优雅地关闭连接。在四次挥手过程中，不仅涉及传输数据的结束，还包括了对网络资源的释放和对远端主机的断开通知，确保网络资源的有效利用。四次挥手的设计旨在确保通信双方都能完成数据的发送和接收，避免因连接突然中断而导致的数据丢失问题。",
"TCP 协议的核心机制包括分段、流量控制、拥塞控制和错误控制，这些机制共同工作以确保数据的可靠传输和网络的稳定性。分段机制将数据包分割成更小的单元，每个分段独立传输并在接收端重组，确保数据传输的可靠性和效率。流量控制机制通过滑动窗口协议来调整数据的发送速率，避免接收方因处理能力不足而造成数据丢失。拥塞控制策略通过调整拥塞窗口大小来应对网络拥堵，保障数据传输的稳定性和效率。错误控制机制通过校验和、自动重传请求等手段来检测和纠正数据传输过程中的错误，保证数据的完整性和准确性。",
"分段处理是 TCP 协议中的一个重要机制。TCP 协议通过分段将数据包分割成更小的单元，每个分段独立传输并在接收端重组，确保数据传输的可靠性和效率。在发送数据前，TCP 协议会根据网络状况将数据分段，每段添加序号和校验信息，接收端按序重组，保证数据完整性。分段机制允许 TCP 在网络拥塞或错误发生时，仅重传受损的分段而非整个数据包，有效提升传输效率和网络利用率。",
"流量控制机制通过滑动窗口协议来实现，确保发送方不会因接收方处理能力不足而造成数据丢失，有效平衡网络负载。TCP 协议通过滑动窗口协议来调整数据的发送速率，根据接收方的处理能力和网络状况动态调整窗口大小。拥塞控制是 TCP 流量控制的核心，通过调整拥塞窗口大小来应对网络拥堵，保障数据传输的稳定性和效率。慢启动与拥塞避免策略进一步优化了流量控制，确保网络资源的有效利用。",
"拥塞控制是 TCP 协议中的核心机制之一，通过调节数据发送速率来避免网络过载，确保数据传输的稳定性和效率。TCP 采用多种拥塞控制算法，如慢启动、拥塞避免和快速重传等，动态调整窗口大小以适应网络状况，优化资源利用。面对网络环境的不确定性，TCP 的拥塞控制面临诸多挑战，包括如何快速响应网络变化和减少数据包丢失，持续优化算法是关键。",
"错误控制机制通过校验和来确保数据在传输过程中的完整性，任何数据的损坏都能被接收端检测到，从而请求重新发送。当 TCP 检测到数据传输错误时，会自动启动重传机制，无需用户干预，确保数据包最终准确无误地到达目的地。TCP 还采用累积确认和选择性确认两种策略来处理错误，有效提高了网络通信的可靠性和效率。",
"TCP 协议在网络通信中有着广泛的应用。在网络通信优化方面，TCP 协议通过三次握手建立连接和四次挥手断开连接的机制，确保数据传输的稳定性和可靠性。在数据流管理方面，利用 TCP 的核心机制如分段、流量控制和拥塞控制，可以有效地管理网络中的数据流，避免数据丢失和网络拥堵，提高传输效率。在错误检测与恢复方面，TCP 协议内置的错误控制机制能够检测到数据传输过程中可能出现的错误，并采取相应的措施进行数据重传或恢复，保证数据的完整性。",
"在网络通信中，TCP 协议的应用场景非常广泛。通过三次握手建立连接和四次挥手断开连接的机制，TCP 协议确保了数据传输的稳定性和可靠性。利用 TCP 的核心机制如分段、流量控制和拥塞控制，可以有效地管理网络中的数据流，避免数据丢失和网络拥堵，提高传输效率。TCP 协议内置的错误控制机制能够检测到数据传输过程中可能出现的错误，并采取相应的措施进行数据重传或恢复，保证数据的完整性。",
"在实际应用中，TCP 协议可能会遇到一些常见问题。数据包丢失是 TCP 通信中常见的问题之一，它可能由网络拥堵、硬件故障等原因引起，导致信息不完整，需通过重传机制保证数据的完整性。高延迟是 TCP 连接常见问题之一，主要由长距离传输、路由效率低下或服务器负载过重引起，严重影响实时应用的性能。TCP 连接中断通常由网络不稳定或设备故障引起，表现为数据传输突然中止，影响应用的连续性和用户体验。",
"综上所述，TCP 协议具有诸多显著特点。它通过三次握手建立连接，确保数据传输的可靠性。它还使用分段、流量控制和错误控制机制来保证数据的完整性和顺序性。在流量控制方面，TCP 采用滑动窗口协议，根据接收方的处理能力调整发送速率，有效避免网络拥塞，提高传输效率。在拥塞控制方面，当网络出现拥塞时，TCP 通过减少拥塞窗口大小来降低数据发送速度，以缓解网络压力，保证网络的稳定性和可靠性。",
"TCP 协议的可靠性是其最显著的特点之一。通过三次握手建立连接，确保数据传输的可靠性。它还使用分段、流量控制和错误控制机制来保证数据的完整性和顺序性。在流量控制方面，TCP 采用滑动窗口协议，根据接收方的处理能力调整发送速率，有效避免网络拥塞，提高传输效率。在拥塞控制方面，当网络出现拥塞时，TCP 通过减少拥塞窗口大小来降低数据发送速度，以缓解网络压力，保证网络的稳定性和可靠性。",
"与其他协议相比，TCP 协议具有明显的优势。TCP 提供可靠、有序和无差错的数据传输，而 UDP 则是一个不可靠的协议，它允许数据包以任何顺序到达，且不保证数据的完整性。HTTP 协议通常使用 TCP 作为传输层协议，因为 TCP 的可靠性确保了网页内容能够完整无误地从服务器传输到客户端。虽然 FTP 可以使用 TCP 或 UDP，但大多数实现选择 TCP 以保证文件传输的可靠性，避免数据在传输过程中丢失或损坏。",
"感谢大家的聆听，希望今天的分享能够让大家对 TCP 协议有更深入的了解。如果大家有任何问题或需要进一步的讨论，欢迎随时与我交流。谢谢！"]

# slide_texts = [
#     f"这是第{i}张幻灯片的内容。"for i in range(1,11)
# ]
# print(slide_texts)

# ppt_to_image(r"D:\PROJECT\Python\test01\downloaded_file.pptx", output_folder)

# 图片路径列表
# 应用排序
image_paths = sorted(
    [os.path.join(output_folder, fname)
     for fname in os.listdir(output_folder)
     if fname.lower().endswith('.png')],
    key=natural_sort_key
)
# # 增加调试信息
# print(f"🔄 正在读取目录：{os.path.abspath(output_folder)}")
# print(f"📂 目录内容：{os.listdir(output_folder)}")
#
# image_paths = sorted(
#     [os.path.join(output_folder, fname)
#      for fname in os.listdir(output_folder)
#      if fname.lower().endswith('.png')]  # 统一小写判断
# )

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
