# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import os
import time

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pptx import Presentation

class AIPPT():

    def __init__(self,APPId,APISecret,Text,templateId):
         # 增加输入验证
        # if not isinstance(Text, str) or len(Text.strip()) < 10:
        #     raise ValueError("文本内容必须为字符串且不少于10个字符")
        self.APPid = APPId
        self.APISecret = APISecret
        self.text = Text
        self.header = {}
        self.templateId = templateId


    #获取签名
    def get_signature(self, ts):
        try:
            # 对app_id和时间戳进行MD5加密
            auth = self.md5(self.APPid + str(ts))
            # 使用HMAC-SHA1算法对加密后的字符串进行加密
            return self.hmac_sha1_encrypt(auth,self.APISecret)
        except Exception as e:
            print(e)
            return None

    def hmac_sha1_encrypt(self, encrypt_text, encrypt_key):
        # 使用HMAC-SHA1算法对文本进行加密，并将结果转换为Base64编码
        return base64.b64encode(hmac.new(encrypt_key.encode('utf-8'), encrypt_text.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')

    def md5(self, text):
        # 对文本进行MD5加密，并返回加密后的十六进制字符串
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    #创建PPT生成任务
    def create_task(self):
        url = 'https://zwapi.xfyun.cn/api/ppt/v2/create'
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        # body= self.getbody(self.text)

        formData = MultipartEncoder(
            fields={
                # "file": (path, open(path, 'rb'), 'text/plain'),  # 如果需要上传文件，可以将文件路径通过path 传入
                # "fileUrl":"",   #文件地址（file、fileUrl、query必填其一）
                # "fileName":"",   # 文件名(带文件名后缀；如果传file或者fileUrl，fileName必填)
                "query": self.text,
                "templateId":f"{self.templateId}", # 模板的ID,从PPT主题列表查询中获取
                "author":"XXXX",    # PPT作者名：用户自行选择是否设置作者名
                "isCardNote" :str(True),   # 是否生成PPT演讲备注, True or False
                "search" :str(False),      # 是否联网搜索,True or False
                "isFigure" :str(True),   # 是否自动配图, True or False
                "aiImage" :"normal"   # ai配图类型： normal、advanced （isFigure为true的话生效）； normal-普通配图，20%正文配图；advanced-高级配图，50%正文配图
            }
        )

        print(formData)

        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": formData.content_type
        }
        self.header = headers
        print(headers)
        response = requests.request(method="POST",url=url, data= formData,headers=headers).text
        print("生成PPT返回结果：",response)
        resp = json.loads(response)
        if(0 == resp['code']):
            return resp['data']['sid']
        else:
            print('创建PPT任务失败')
            return None

    #构建请求body体
    def getbody(self,text):
        body = {
            "query":text,
            "templateId":self.templateId  #  模板ID举例，具体使用 /template/list 查询
        }
        return body
		
		
	#轮询任务进度，返回完整响应信息
    # def get_process(self,sid):
    #     # print("sid:" + sid)
    #     if(None != sid):
    #         response = requests.request("GET",url=f"https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={sid}",headers=self.header).text
    #         print(response)
    #         return response
    #     else:
    #         return None
    def get_process(self, sid):
        """修复后的进度查询方法"""
        if not sid:
            print("⚠️ 无效的任务ID")
            return None

        # 每次请求生成新的签名（关键修复点）
        timestamp = int(time.time())
        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": self.get_signature(timestamp),
            "Content-Type": "application/json"
        }

        url = f"https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={sid}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"轮询状态码：{response.status_code}")
            
            # 处理非JSON响应（关键修复点）
            if not response.text.strip().startswith("{"):
                print(f"⚠️ 无效响应内容：{response.text[:100]}")
                return None
                
            return response.json()
        except Exception as e:
            print(f"轮询失败: {str(e)}")
            return None


    #获取PPT，以下载连接形式返回
    # def get_result(self,task_id):

    #     #创建PPT生成任务
    #     # task_id = self.create_task()
    #     # PPTurl = ''
    #     #轮询任务进度
    #     while(True):
    #         response = self.get_process(task_id)
    #         resp = json.loads(response)
    #         pptStatus = resp['data']['pptStatus']
    #         aiImageStatus = resp['data']['aiImageStatus']
    #         cardNoteStatus = resp['data']['cardNoteStatus']


    #         if('done' == pptStatus and 'done' == aiImageStatus and 'done' == cardNoteStatus):
    #             PPTurl = resp['data']['pptUrl']
    #             break
    #         else:
    #             time.sleep(3)
    #     return PPTurl

    def get_result(self, task_id):
        """改进后的结果获取方法"""
        try:
            max_retries = 40  # 延长到40次（120秒）
            success_pages = 0
            
            for i in range(1, max_retries + 1):
                resp = self.get_process(task_id)
                
                # 增强响应验证
                if not resp or not isinstance(resp, dict) or resp.get("code") != 0:
                    print(f"🔄 第{i}次尝试失败，3秒后重试")
                    time.sleep(3)
                    continue
                    
                data = resp.get("data", {})
                done_pages = data.get("donePages", 0)
                total_pages = data.get("totalPages", 1)
                
                # 新增状态打印（整合ceshi.py的进度显示）
                print(f"\n【PPT生成进度】{time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"📊 当前进度：{min(int(done_pages/total_pages*100), 100)}% ({done_pages}/{total_pages}页)")
                print(f"🏗️ 结构生成: {data.get('pptStatus', 'unknown')}")
                print(f"🖼️ 智能配图: {data.get('aiImageStatus', 'unknown')}")
                print(f"📝 备注生成: {data.get('cardNoteStatus', 'unknown')}")
                
                # 最终状态判断条件优化
                if all(status == "done" for status in [
                    data.get("pptStatus"),
                    data.get("aiImageStatus")
                ]) and data.get("cardNoteStatus") == "done":
                    if (ppt_url := data.get("pptUrl")):
                        print("\n✅ 所有任务已完成！")
                        return ppt_url
                    
                # 当全部页面处理完成时，延长等待时间
                if done_pages >= total_pages:
                    print("⚠️ 所有页面处理完成，等待最终生成...")
                    time.sleep(10)  # 延长到10秒/次
                else:
                    time.sleep(5 if i > 20 else 3)  # 后期延长检查间隔

            print(f"⏱️ 超过{max_retries}次重试仍未完成")
            return None
            
        except Exception as e:
            print(f"⚠️ 获取结果异常: {str(e)}")
            return None

    def getHeaders(self):
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        # body = self.getbody(self.text)

        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": "application/json; charset=utf-8"
        }
        return headers

    def getTheme(self,style="",color="",industry="",pageNum=1,pageSize=1):
        url ="https://zwapi.xfyun.cn/api/ppt/v2/template/list"
        self.header = self.getHeaders()
        body = {
            "payType": "free",
            "style": f"{style}",    # 风格类型： "简约","卡通","商务","创意","国风","清新","扁平","插画","节日"
            "color": f"{color}",   #  颜色类型： "蓝色","绿色","红色","紫色","黑色","灰色","黄色","粉色","橙色"
            "industry": f"{industry}",    # 行业类型： "科技互联网","教育培训","政务","学院","电子商务","金融战略","法律","医疗健康","文旅体育","艺术广告","人力资源","游戏娱乐"	
            "pageNum": f"{pageNum}" ,
            "pageSize": f"{pageSize}"
        }

        response = requests.request("GET", url=url, headers=self.header,json=body)
        # print(response)
        # return response
        data = response.json()
        if data["code"] != 0:
            print(f"❌ 请求失败：{data.get('desc', '未知错误')}")
            return None

        # 结构化输出模板信息
        print(f"\n（第{pageNum}页，每页{pageSize}条）")
        
        for template in data['data']['records']:
            print(f"""
            📑 模板共 {data['data']['total']} 张
            🔖 模板ID：{template['templateIndexId']}
            🏷️ 名称类型：{template.get('templateName', '未命名')} ({template['type']})
            🎨 风格配色：{template['style']} + {template['color']}
            🏭 适用行业：{template['industry'].strip()}
            📸 预览地址：{json.loads(template['detailImage'])}
            """)
            
        return data

    def createOutline(self):
        # if('' ==fileUrl and '' == filePath):
        url ="https://zwapi.xfyun.cn/api/ppt/v2/createOutline"
        body = {
            "query": self.text,
            "language": "cn",
            "search": str(False),  # 是否联网搜索,True or False
        }

        response = requests.post(url=url,json= body,headers=self.getHeaders()).text
        print("生成大纲完成：\n",response)

        return response
        
    
    def create_text_outline(self):
       # if('' ==fileUrl and '' == filePath):
        url ="https://zwapi.xfyun.cn/api/ppt/v2/createOutline"
        formData = MultipartEncoder(
            fields={
                "query": self.text,
                "language": "cn",
                "search": str(False),  # 是否联网搜索,True or False
            }
        )
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": formData.content_type
        }
        # self.header = headers
        # response = requests.post(url=url,data= formData,headers=headers).text
        # print("生成大纲完成：\n",response)

        # return response
        try:
            # 获取并解析JSON响应
            response = requests.post(url, data=formData, headers=headers)
            response.raise_for_status()  # 检查HTTP错误
            print("生成大纲完成：\n",response.json())
            return response.json()  # 直接返回解析后的字典
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return None
        except json.JSONDecodeError:
            print("响应解析失败")
            return None


    def createOutlineByDoc(self,fileName,fileUrl=None,filePath =None ):
        # if('' ==fileUrl and '' == filePath):
        url ="https://zwapi.xfyun.cn/api/ppt/v2/createOutlineByDoc"
        formData = MultipartEncoder(
            fields={
                "file": (filePath, open(filePath, 'rb'), 'text/plain'),  # 如果需要上传文件，可以将文件路径通过path 传入
                "fileUrl":fileUrl,   #文件地址（file、fileUrl必填其一）
                "fileName": fileName,   # 文件名(带文件名后缀；如果传file或者fileUrl，fileName必填)
                "query": self.text,
                "language": "cn",
                "search": str(False),  # 是否联网搜索,True or False
            }
        )
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": formData.content_type
        }
        self.header = headers
        response = requests.post(url=url,data= formData,headers=headers).text
        print("生成大纲完成：\n",response)

        return response

    def createPptByOutline(self,outline):
        url = "https://zwapi.xfyun.cn/api/ppt/v2/createPptByOutline"
        body = {
                "query": self.text,
                "outline":outline,
                "templateId":self.templateId, # 模板的ID,从PPT主题列表查询中获取
                "author":"XXXX",    # PPT作者名：用户自行选择是否设置作者名
                "isCardNote" :True,   # 是否生成PPT演讲备注, True or False
                "search" :False,      # 是否联网搜索,True or False
                "isFigure" :True,   # 是否自动配图, True or False
                "aiImage" :"normal",   # ai配图类型： normal、advanced （isFigure为true的话生效）； normal-普通配图，20%正文配图；advanced-高级配图，50%正文配图

            }
        print(body)

        response = requests.post(url,json=body,headers=self.getHeaders()).text
  
        print("创建生成任务成功：\n",response)
        resp = json.loads(response)
        if (0 == resp['code']):
            return resp['data']['sid']
        else:
            print('创建PPT任务失败')
            return None


def download_ppt(url,ppt_path="downloaded_file.pptx"):
    response = requests.get(url)
    with open(f"{ppt_path}", "wb") as file:
        file.write(response.content)
    print("文件下载完成")

def main_create_ppt(APPId,APISecret,ppt_outline,templateId,ppt_path=''):
    demo = AIPPT(APPId,APISecret,ppt_outline,templateId)
    taskid = demo.create_task()
    result = demo.get_result(taskid)
    print("生成的PPT请从此地址获取：\n" + result)
    download_ppt(result,ppt_path)

if __name__ == '__main__':
    #控制台获取 
    APPId = "5f1edb16"
    APISecret = "d50e3011f50b9aa6b14f46b75dfda974"

    # 查询PPT主题列表
    # demo1 = AIPPT(APPId,APISecret,'','')
    # templateId = demo1.getTheme(color="蓝色",pageNum=1,pageSize=2) # 获取模板列表
    # print("支持模板列表：\n",templateId)
    templateId = "20240731F237950"  # 该模板ID，需要通过getTheme() 方法获取模板列表，然后从中挑选

    #流程一：根据描述或者文档直接生成PPT；(流程一、流程二代码不能同时打开)
    # # 流程一开始
    presentation_request = """
                TCP协议概述
                TCP与OSI模型
                三次握手与四次挥手
                核心机制（分段、流量控制、拥塞控制、错误控制）
                实际应用与常见问题
                总结与对比
    """
    main_create_ppt(APPId,APISecret,presentation_request,templateId)




    #流程二： 先生成大纲(支持上传文本)，再通过大纲生成PPT；(流程一、流程二代码不能同时打开)

    # # 流程二开始
    # title = "秋分时节的农业管理策略"   #设定大纲主题
    # # filename = "text.md" # 需要根据文档上传时，请填写文档路径；要求：字数不得超过8000字，文件限制10M。上传文件支持pdf(不支持扫描件)、doc、docx、txt、md格式的文件。
    # # filePath = r"D:\PROJECT\Python\test01\PptTurnVideo\text.md" # 文件路径，也可以通过fileurl 字段上传对象存储地址，具体见方法：createOutlineByDoc

    # demo = AIPPT(APPId, APISecret, title, templateId)
    # res = demo.createOutlineByDoc(fileName="text.md",filePath=r"D:\PROJECT\Python\test01\PptTurnVideo\text.md")

    # # data = json.loads(res)
    # outline = res["data"]["outline"]
    # taskid = demo.createPptByOutline(outline)
    # print("**********************************************")
    # print(taskid)
    # # 流程二结束

    # result = demo.get_result(taskid)
    # print("生成的PPT请从此地址获取：\n" + result)














    # # 直接通过文本生成
    # presentation_request = """
    # 请帮我制作关于区块链技术的PPT，需要包含：
    # 1. 区块链基本原理（去中心化、分布式账本）
    # 2. 关键技术组成（哈希算法、共识机制）
    # 3. 主要应用场景（金融、供应链）
    # 4. 发展趋势分析
    # 要求：每页配相关技术示意图，使用科技蓝配色方案
    # """

    # try:
    #     # 初始化实例
    #     generator = AIPPT(APPId, APISecret, presentation_request, templateId)
        
    #     # 生成大纲
    #     print("🔄 正在生成大纲...")
    #     outline_data = generator.create_text_outline()
        
    #     # 添加类型检查
    #     if not isinstance(outline_data, dict):
    #         print("❌ 响应格式异常")
    #         exit(1)
            
    #     if outline_data.get("code") != 0:
    #         error_msg = outline_data.get("desc", "未知错误")
    #         print(f"❌ 大纲生成失败: {error_msg}")
    #         exit(1)
            
    #     # 安全获取大纲数据
    #     outline = outline_data.get("data", {}).get("outline")
    #     if not outline:
    #         print("❌ 大纲数据缺失")
    #         exit(1)
            
    #     print("✅ 大纲生成成功！结构如下：")
    #     # print(json.dumps(outline, indent=2, ensure_ascii=False))
    #     print(outline)
        
    #     # 创建PPT任务
    #     print("\n🔄 正在提交PPT生成任务...")
    #     task_id = generator.createPptByOutline(outline)
    #     if not task_id:
    #         print("❌ 任务提交失败")
    #         exit(1)
            
    #     # 获取结果
    #     print(f"\n📦 任务ID: {task_id}")
    #     print("⏳ 正在生成PPT，预计需要1-3分钟...")
    #     final_url = generator.get_result(task_id)
    #     print(f"\n🎉 PPT生成完成！下载地址：\n{final_url}")
        
    # except Exception as e:
    #     print(f"\n⚠️ 程序运行异常: {str(e)}")








