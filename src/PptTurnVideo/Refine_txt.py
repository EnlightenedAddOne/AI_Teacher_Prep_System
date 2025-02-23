import json
from src.utils import text_polishing_prompt, ppt_outline_prompt
from src.llm_integration import LLMFactory


def text_polishing(api_key, original_txt):
    """
    对文本进行润色优化
    :param api_key: DeepSeek API密钥
    :param original_txt: 原始文本
    :return: 优化后的文本列表
    """
    raw_response = None
    try:
        # 初始化 DeepSeek 客户端
        client = LLMFactory.initialize_deepseek(api_key)
        
        # 准备提示词
        prompt = text_polishing_prompt.format(original_text=original_txt)
        system_prompt = "你是一个专业的文本优化助手，严格按照JSON格式输出结果"
        
        # 调用 API
        raw_response = LLMFactory.call_deepseek(client, system_prompt, prompt, model="deepseek-reasoner")
        if not raw_response:
            return []

        # 获取并清洗响应
        cleaned_response = raw_response.strip().replace('```json', '').replace('```', '')
        data = json.loads(cleaned_response)
        return data.get("enhanced", [])

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}\n原始响应: {raw_response if 'raw_response' in locals() else 'None'}")
        return []
    except Exception as e:
        error_msg = f"处理失败: {str(e)}"
        if 'raw_response' in locals():
            error_msg += f"\n原始响应: {raw_response[:200]}"
        print(error_msg)
        return []


def ppt_outline(api_key, subject, topic):
    """
    根据教学设计生成PPT大纲
    :param api_key: DeepSeek API密钥
    :param subject: 学科名称
    :param topic: 课程内容
    :return: PPT大纲字符串
    """
    raw_response = None
    try:
        # 初始化 DeepSeek 客户端
        client = LLMFactory.initialize_deepseek(api_key)
        
        # 准备提示词
        prompt = ppt_outline_prompt.format(subject=subject, topic=topic)
        system_prompt = "你是一个专业的PPT大纲设计专家，严格按照JSON格式输出结果"
        
        # 调用 API
        raw_response = LLMFactory.call_deepseek(client, system_prompt, prompt, model="deepseek-reasoner")
        if not raw_response:
            return ""

        # 获取并清洗响应
        cleaned_response = raw_response.strip().replace('```json', '').replace('```', '')

        # 解析JSON
        data = json.loads(cleaned_response)
        
        # 格式化大纲输出
        outline = f"{data['title']}\n\n"
        for section in data.get('sections', []):
            outline += f"{section['title']}\n"
            for point in section.get('points', []):
                outline += f"    • {point}\n"
            outline += "\n"
        
        return outline

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}\n原始响应: {raw_response if 'raw_response' in locals() else 'None'}")
        return ""
    except Exception as e:
        error_msg = f"API调用异常: {str(e)}"
        if 'raw_response' in locals():
            error_msg += f"\n原始响应: {raw_response[:200]}"
        print(error_msg)
        return ""


# 测试代码
if __name__ == "__main__":
    # 测试用的教学设计示例
    # subject = "计算机网络"
    # topic = "TCP协议"
    # 使用你的API密钥测试
    api_key = "sk-1e4ec15f97a044ab8fca717279a9cbea"  # 替换为实际的API密钥
    # outline = ppt_outline(api_key, subject=subject, topic=topic)
    # print(outline)
    polish_text = [
        '各位同仁、同学们，大家好！今天，我们聚焦于“计算机网络协议课程教学”，一同探索这一技术领域的深邃与广博。网络协议作为信息技术的基石，其重要性不言而喻，它不仅是互联网通信的规则手册，更是构建现代信息社会的桥梁。本课程旨在深入剖析网络协议的原理，通过严谨的教学设计，引领大家系统掌握核心知识与技能，为日后的学术研究或职业生涯奠定坚实基础。让我们携手启航，共赴这场智慧之旅。',
        '在这次的演讲中，我会从网络协议的基础切入，深入探讨各个层次的协议，包括物理层与数据链路层、网络层、传输层、应用层，最后讨论网络安全与相关协议。让我们开始这段探索旅程。',
        '这部分我将深入探讨网络协议的重要性，并概述我们的课程目标成果和结构评估。通过对这些关键点的分析，我们将理解网络协议在现代通信中所扮演的核心角色以及如何有效评估与提升相关课程的学习效果。',
        '这部分将以网络协议重要性为主题展开阐述。网络协议是数据交换与通信规则的基础，保障设备间无缝连接与通信，是互联网运作基石；同时，它促进全球信息流通，实现信息快速准确传递，推动信息共享与全球化交流；另外，网络协议还涉及数据传输安全，通过加密和验证机制保护数据安全性与完整性。',
        '这部分将以三个核心点展开。首先是课程目标成果，学生将掌握网络协议基础，深入学习从物理层到应用层的协议，为后续的网络学习奠定坚实基础。其次是分析与设计网络结构，通过研究不同层次的协议，提高解决实际网络问题的能力。最后是网络安全意识的提升，课程强调网络安全的重要性，教授SSL/TLS、防火墙和VPN技术，增强学生的网络安全意识和防护技能。',
        '这段我将以课程结构评估为核心，展开三个关键维度的剖析。聚焦于课程目标与学习成果，我们的目标是让学生深入理解并掌握计算机网络协议的精髓，通过结合理论讲解与实践操作，确保每位学员能够熟练运用网络协议知识解决实际问题。探讨课程结构与评估方式，本课程精心布局了从基础到高级的知识体系，采用多元化教学手段，包括课堂讲授、实验仿真以及项目驱动，旨在全方位提升学生的专业能力，实现最佳教学质量。着重阐述网络安全与协议的重要性，鉴于当前网络安全形势，我们特别强化了SSL/TLS协议、防火墙配置及VPN技术的教学，以培养学生在网络安全防护领域的敏锐洞察力和实战技能。',
        '这部分我将以网络协议基础为引，简要概述其定义、作用以及在OSI与TCP/IP模型中的应用。同时，我们将探讨分层结构和数据封装的概念，这些都是理解现代网络通信不可或缺的基础知识。',
        '',
        '下面我将介绍OSI模型和TCP/IP模型。OSI模型是开放系统互联参考模型，由国际标准化组织提出，指导不同计算机系统间的通信。而TCP/IP模型是互联网的基础通信协议，包括传输控制协议和网际协议，简化了OSI模型的层次，广泛应用于局域网和广域网中。两者在功能上有所对应，但TCP/IP更侧重于实际应用，简化了理论模型。',
        '这部分我将以“分层与封装”为核心，探讨网络通信架构设计的关键概念。协议分层，作为网络通信的基石，将复杂流程拆解为若干层级，每层专司其职，确保设计与实现的简洁性与有效性。数据封装，则是在发送端各层附加特定头部信息于上层数据之上，形成完整数据包的过程，此环节对保障传输数据的完整性与准确性至关重要。进一步地，对比OSI七层理论模型与TCP/IP四层实际应用模型，两者均秉承分层原则，却在层次数量、功能界定及实施细节上展现出不同风貌，反映了理论指导与实践应用之间的微妙差异。',
        '这部分我们将深入探讨物理层与数据链路层，首先概述物理层的关键作用，然后详细比较以太网与PPP两种主流技术特点，并解析MAC地址帧结构的核心概念。',
        '这部分，我将介绍物理层的核心概念。首先探讨其协议基础，它是网络通信的基石，通过光纤、双绞线等介质实现原始比特流的传输，保障数据有效流动于网络之中。随后关注信号传输模式，区分为基带与宽带传输，适应不同场景需求，直接影响网络速率与传输质量。最后，聚焦于物理层关键设备及接口标准，如网卡、交换机及其采用的RJ45、USB等规范，这些是确保网络高效兼容运作的重要因素。',
        '这部分将以太网与PPP展开讲解。以太网是局域网常用有线网络技术，借由双绞线或光纤传输数据，凭高速度、低成本受青睐。PPP作为连接两节点的通信协议，支持多种网络层协议，具备身份验证、加密及压缩功能。二者相较，以太网适用于局域网高速数据传输，PPP则更契合广域网连接，如家庭互联网接入，应用场景与技术特点各展优势。',
        '这部分，我主要探讨MAC地址的帧结构，首先，我们将明确MAC地址的定义。它是网络设备上用于识别网络接口的独特标识符，是数据链路层的核心要素。接下来，我将强调帧结构的重要性。作为物理网络中数据传输的基本单位，帧结构包含源和目的MAC地址、数据类型及校验信息等关键部分。最后，我将阐述MAC地址与帧结构的紧密联系。每个以太网帧都包含源和目的MAC地址，这些地址在网络上确保数据正确传输，唯一标识了发送者和接收者。',
        '这部分，我们将深入探讨网络层协议的关键领域：从IP协议基础，了解其核心功能与应用；到路由协议类型，解析数据包传输路径的决策机制；再到IP地址子网划分，掌握如何高效管理网络资源。',
        '这部分，我将探讨IP协议的基础。首先是IP协议概述。IP协议作为互联网的根基，承担着在网络中收发数据包的关键角色，其无连接、不可靠的传输特性确保了数据能从源至目的地的有效传递。紧接着，我们对比IPv4与IPv6。IPv4，历史上首个广泛应用的互联网协议版本，因其地址资源有限正逐步让位于IPv6。IPv6不仅提供了更为广阔的地址空间，还增强了安全性，以适应未来互联网的扩展需求。最后，讨论子网划分与路由选择的重要性。子网划分通过将大网络细化为多个小网络，优化网络性能并提升管理效能。而路由选择过程，则是依据目标地址智能地决定数据传输路径，确保数据高效抵达目的地。',
        '这部分我将以路由协议类型为核心，深入探讨网络层的关键机制。路由协议概述：它是网络层的基石，智能地为数据包导航，确保信息在错综复杂的网络脉络中精准、高效传递。接下来，我们将聚焦两种主要的距离矢量路由协议。距离矢量路由协议：这类协议通过周期性交换路由表信息来维持和更新自己的路径选择。尽管实现简便，适用于轻量级网络环境，但它面临计数到无限的问题，需谨慎管理以避免潜在的路由循环。链路状态路由协议：相比之下，链路状态协议通过广播链路状态至所有路由器，构建一个全面的网络拓扑图，特别适合大规模部署。其优势在于快速收敛能力和内置防环机制。',
        '这部分我将以IP地址子网划分为主题，展开三方面内容讲解。首先是子网掩码的作用，它区分IP地址的网络与主机部分，保障数据准确转发。其次是子网划分的方法，通过借用主机位创建多个子网，提升IP利用率与管理灵活性。最后是CIDR表示法的优势，其利用可变长度子网掩码，缩减路由表，提高现代互联网的路由效率。',
        '这部分，我们将深入探讨传输层协议中的关键组成部分——TCP与UDP。我们不仅会解析它们在网络通信中的核心作用，还将深入了解TCP的三次握手、四次挥手机制以及端口号和套接字的工作原理，这些都是构建稳定数据传输的基石。',
        '',
        '这部分，我将以TCP协议中的“三次握手”与“四次挥手”机制为核心，展开阐述。首先，TCP三次握手，作为建立可靠连接的关键步骤，通过三次数据包的交换，确保了客户端与服务器双方均已就绪，能够稳定、有效地进行数据传输。这一过程不仅验证了通信双方的接收和发送能力，还协商了初始序列号，为后续数据的可靠传输奠定了坚实的基础。接下来，我们探讨TCP的“四次挥手”机制。当通信会话需要终止时，四次挥手机制发挥作用，确保了所有待处理的数据均已发送完成，并优雅地关闭了连接。这一机制保证了数据传输的完整性和连接的平稳终止。',
        '这部分，我将深入探讨这一核心概念。首先，聚焦于端口号的功能，它在网络通讯中扮演着标识服务的关键角色，确保数据包精准抵达目的应用。随后，我们将定义套接字这一术语，它作为网络编程的基石，代表了通信过程的起点或终点，由IP与端口共同定位。最后剖析二者间的紧密联系，即套接字如何利用端口号区分不同网络服务，保障信息的正确传输与接收。',
        '下面我将深入探讨应用层协议，重点讲解HTTP与HTTPS如何保障网络通信安全，DNS与DHCP在互联网寻址与配置中的关键作用，以及电子邮件协议如何支撑现代通信的核心需求。',
        '### 标题：理解HTTP与HTTPS的关键要点这部分我将以HTTP协议基础、HTTPS的安全增强以及从HTTP到HTTPS的转变为核心内容，展开详细阐述。HTTP作为一种无状态的应用层协议，主要负责在Web浏览器和服务器之间传输超文本数据，其定义的请求与响应格式构成了互联网信息交换的基础。而HTTPS，作为HTTP的安全版本，通过引入SSL/TLS加密层，显著增强了数据传输的安全性与完整性，有效抵御了中间人攻击及数据窃取风险。随着网络安全意识的日益增强，众多网站正逐步从HTTP迁移至HTTPS，这一转变不仅极大地提升了用户数据的安全性，还成为了优化搜索引擎结果的重要因素。',
        '',
        '这部分，我们将探讨电子邮件协议，重点了解SMTP、POP3与IMAP的核心功能。那么这一页，我们从SMTP协议基础说起。SMTP，全称简单邮件传输协议，作为电子通信的基石，其核心职责在于构建发件人至收件人邮箱间的桥梁，确保信息跨越网络，从源头抵达终点，完成邮件的有效投递。接下来，我们聚焦于POP3协议功能。邮局协议第三版，即POP3，赋予了用户从服务器下载邮件至本地设备的权力。此机制不仅实现了邮件的离线阅读自由，更通过允许本地删除已下载邮件以释放服务器存储，优化了资源管理效率。而当我们谈及IMAP协议特点，一个旨在提升灵活性与同步性的现代解决方案映入眼帘。不同于POP3的是，IMAP让用户能够在多台设备间无缝查看同一邮箱内的所有邮件，无需逐一下载，真正实现了跨平台的实时同步，完美契合了当今移动互联时代的多元需求。',
        '这部分我将探讨网络安全与协议的核心内容，从网络安全的基本概述开始，深入到SSL/TLS协议的重要性，再到防火墙和VPN技术的关键作用，为大家揭示如何构建更加安全的网络环境。',
        '这段我将以网络安全的重要性作为开篇，阐述其在数字化时代的基石地位。网络安全，这一融合了先进技术、周密流程与严谨政策的领域，是保障信息资产免受未授权访问、泄露及破坏的第一道防线。它不仅关乎数据的完整性，更确保信息的机密性与服务的不间断性。那么这一页，我们将聚焦于网络威胁的多样性，它们是数字环境中不容忽视的挑战。从恶意软件如病毒和木马，到精心设计的钓鱼攻击，这些威胁手段层出不穷，旨在窃取数据、干扰运营乃至造成严重的经济损失。深入理解这些威胁的本质，是构筑有效防御体系的前提。下面我将介绍防御策略与最佳实践的核心要点。强化密码管理政策、保持软件的最新状态以及持续的安全教育培训，构成了提升网络安全的基础框架。此外，采用多层防御机制，通过层层把关，为组织构建起一道更为坚固的安全屏障，从而在复杂多变的威胁面前，展现出更强的韧性与应对能力。',
        '这部分我将以SSL/TLS协议为主题展开阐述。首先介绍其概述，它是保障互联网加密通信的安全协议，连接传输层与应用层，确保数据保密完整。接着说明工作原理，凭借公私钥实现加密解密，兼具身份验证与消息完整性核查功能。最后谈谈应用，广泛应用于电商、邮件、社交等网络场景，营造安全可靠环境。',
        '这部分我将以防火墙与VPN技术为核心，展开深入探讨。首先，我们来剖析防火墙的工作原理。它如同一位严谨的网络守卫，时刻监控进出网络的每一个数据包，严格依据预先设定的精密安全规则体系，对数据流进行精准的甄别与管控。通过允许合法、合规的数据流顺畅通行，而毫不留情地阻止那些存在潜在风险的数据流进入内部网络，从而构筑起一道坚不可摧的安全防线，有效抵御来自外部网络的各种威胁与攻击，切实保障内部网络环境的稳定与安全。接着，我们来了解一下 VPN 技术概述。VPN，即虚拟私人网络，其核心技术在于能够在纷繁复杂的公共网络环境之上，巧妙且稳固地搭建起一条专属的加密通道。这一加密通道宛如一座隐蔽的桥梁，使分散于各地的远程用户在确保数据传输高度安全的前提下，得以顺利地接入企业内部资源。无论是敏感数据的传递，还是远程办公的需求，均能凭借此技术得到可靠保障。最后，谈谈防火墙与 VPN 的结合应用。当这二者携手协作时，便能发挥出“1+1>2”的强大效能。一方面，借助 VPN 技术所提供的便捷远程访问功能，满足用户随时随地获取企业资源的实际需求；另一方面，防火墙则在此过程中持续强化网络安全层级，严格把控入口权限，确保只有那些经过预先授权的合法用户能够成功突破防线，接触到敏感且关键的信息资源，进一步筑牢企业网络安全的坚实壁垒。',
        '尊敬的各位，本次演讲围绕《计算机网络协议课程教学》展开，涵盖了从基础到应用的各层次协议及网络安全。希望通过此次分享，大家能对网络协议有更深入的理解和应用。感谢大家的聆听与支持！']
    test = text_polishing(api_key, polish_text)
    print(test)
