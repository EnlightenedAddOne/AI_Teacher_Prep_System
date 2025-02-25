# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import os
import time

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class AIPPT():

    def __init__(self, APPId, APISecret, Text, templateId):
        self.APPid = APPId
        self.APISecret = APISecret
        self.text = Text
        self.header = {}
        self.templateId = templateId

    # 获取签名
    def get_signature(self, ts):
        try:
            # 对app_id和时间戳进行MD5加密
            auth = self.md5(self.APPid + str(ts))
            # 使用HMAC-SHA1算法对加密后的字符串进行加密
            return self.hmac_sha1_encrypt(auth, self.APISecret)
        except Exception as e:
            print(e)
            return None

    def hmac_sha1_encrypt(self, encrypt_text, encrypt_key):
        # 使用HMAC-SHA1算法对文本进行加密，并将结果转换为Base64编码
        return base64.b64encode(
            hmac.new(encrypt_key.encode('utf-8'), encrypt_text.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')

    def md5(self, text):
        # 对文本进行MD5加密，并返回加密后的十六进制字符串
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    # 创建PPT生成任务
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
                "templateId": "20240718489569D",  # 模板的ID,从PPT主题列表查询中获取
                "author": "XXXX",  # PPT作者名：用户自行选择是否设置作者名
                "isCardNote": str(True),  # 是否生成PPT演讲备注, True or False
                "search": str(False),  # 是否联网搜索,True or False
                "isFigure": str(True),  # 是否自动配图, True or False
                "aiImage": "normal"
                # ai配图类型： normal、advanced （isFigure为true的话生效）； normal-普通配图，20%正文配图；advanced-高级配图，50%正文配图
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
        response = requests.request(method="POST", url=url, data=formData, headers=headers).text
        print("生成PPT返回结果：", response)
        resp = json.loads(response)
        if (0 == resp['code']):
            return resp['data']['sid']
        else:
            print('创建PPT任务失败')
            return None

    # 构建请求body体
    def getbody(self, text):
        body = {
            "query": text,
            "templateId": self.templateId  # 模板ID举例，具体使用 /template/list 查询
        }
        return body

    # 轮询任务进度，返回完整响应信息
    def get_process(self, sid):
        # print("sid:" + sid)
        if (None != sid):
            response = requests.request("GET", url=f"https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={sid}",
                                        headers=self.header).text
            print(response)
            return response
        else:
            return None

    # 获取PPT，以下载连接形式返回
    def get_result(self, task_id):

        # 创建PPT生成任务
        # task_id = self.create_task()
        # PPTurl = ''
        # 轮询任务进度
        while (True):
            response = self.get_process(task_id)
            resp = json.loads(response)
            pptStatus = resp['data']['pptStatus']
            aiImageStatus = resp['data']['aiImageStatus']
            cardNoteStatus = resp['data']['cardNoteStatus']

            if ('done' == pptStatus and 'done' == aiImageStatus and 'done' == cardNoteStatus):
                PPTurl = resp['data']['pptUrl']
                break
            else:
                time.sleep(3)
        return PPTurl

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

    def getTheme(self):
        url = "https://zwapi.xfyun.cn/api/ppt/v2/template/list"
        self.header = self.getHeaders()
        body = {
            "payType": "not_free",
            # "style": "简约",    # 支持按照类型查询PPT 模板
            # "color": "红色",   #  支持按照颜色查询PPT 模板
            # "industry": "教育培训",    # 支持按照颜色查询PPT 模板
            "pageNum": 2,
            "pageSize": 10
        }

        response = requests.request("GET", url=url, headers=self.header).text
        print(response)
        return response

    def createOutline(self):
        # if('' ==fileUrl and '' == filePath):
        url = "https://zwapi.xfyun.cn/api/ppt/v2/createOutline"
        body = {
            "query": self.text,
            "language": "cn",
            "search": str(False),  # 是否联网搜索,True or False
        }

        response = requests.post(url=url, json=body, headers=self.getHeaders()).text
        print("生成大纲完成：\n", response)

        return response

    def createOutlineByDoc(self, fileName, fileUrl=None, filePath=None):
        # if('' ==fileUrl and '' == filePath):
        url = "https://zwapi.xfyun.cn/api/ppt/v2/createOutlineByDoc"
        formData = MultipartEncoder(
            fields={
                "file": (filePath, open(filePath, 'rb'), 'text/plain'),  # 如果需要上传文件，可以将文件路径通过path 传入
                "fileUrl": fileUrl,  # 文件地址（file、fileUrl必填其一）
                "fileName": fileName,  # 文件名(带文件名后缀；如果传file或者fileUrl，fileName必填)
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
        response = requests.post(url=url, data=formData, headers=headers).text
        print("生成大纲完成：\n", response)

        return response

    def createPptByOutline(self, outline):
        url = "https://zwapi.xfyun.cn/api/ppt/v2/createPptByOutline"
        body = {
            "query": self.text,
            "outline": outline,
            "templateId": self.templateId,  # 模板的ID,从PPT主题列表查询中获取
            "author": "XXXX",  # PPT作者名：用户自行选择是否设置作者名
            "isCardNote": True,  # 是否生成PPT演讲备注, True or False
            "search": False,  # 是否联网搜索,True or False
            "isFigure": True,  # 是否自动配图, True or False
            "aiImage": "normal",
            # ai配图类型： normal、advanced （isFigure为true的话生效）； normal-普通配图，20%正文配图；advanced-高级配图，50%正文配图

        }
        print(body)

        response = requests.post(url, json=body, headers=self.getHeaders()).text
        print("创建生成任务成功：\n", response)
        resp = json.loads(response)
        if (0 == resp['code']):
            return resp['data']['sid']
        else:
            print('创建PPT任务失败')
            return None

def download_ppt(url, ppt_path=None):  # 修改默认值为None
    # 设置默认路径（当前目录+时间戳）
    if not ppt_path:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        ppt_path = os.path.join(os.getcwd(), f"presentation_{timestamp}.pptx")
    
    # 确保目录存在
    os.makedirs(os.path.dirname(ppt_path), exist_ok=True)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(ppt_path, "wb") as file:
            file.write(response.content)
            
        print(f"文件已保存到：{os.path.abspath(ppt_path)}")
        return os.path.abspath(ppt_path)  # 返回绝对路径
        
    except Exception as e:
        print(f"下载失败：{str(e)}")
        return None

# def main_create_ppt(APPId, APISecret, ppt_outline, templateId, ppt_path=None):  # 修改默认参数
#     demo = AIPPT(APPId, APISecret, ppt_outline, templateId)
#     taskid = demo.create_task()
#     result = demo.get_result(taskid)
#
#     if result:
#         saved_path = download_ppt(result, ppt_path)
#         if saved_path:
#             print(f"✅ PPT已保存到：{saved_path}")
#             return saved_path
#     print("❌ PPT生成失败")
#     return None

def main_create_ppt(APPId,APISecret,ppt_outline,templateId,ppt_path=None):
    demo = AIPPT(APPId,APISecret,ppt_outline,templateId)
    taskid = demo.create_task()
    result = demo.get_result(taskid)
    print("生成的PPT请从此地址获取：\n" + result)
    download_ppt(result,ppt_path)

if __name__ == '__main__':
    # 控制台获取
    APPId = "5f1edb16"
    APISecret = "d50e3011f50b9aa6b14f46b75dfda974"

    # 查询PPT主题列表
    # demo1 = AIPPT(APPId,APISecret,'','')
    # templateId = demo1.getTheme() # 获取模板列表
    # print("支持模板列表：\n",templateId)
    templateId = "20240718489569D"  # 该模板ID，需要通过getTheme() 方法获取模板列表，然后从中挑选

    # 流程一：根据描述或者文档直接生成PPT；(流程一、流程二代码不能同时打开)
    # # 流程一开始
    Text = "请帮我写一份PPT： 介绍下今年到目前位置的公司经营状况"
    main_create_ppt(APPId,APISecret,Text, templateId,r"D:\PROJECT\Python\test01\ceshi.pptx")
    # download_ppt("https://bjcdn.openstorage.cn/xinghuo-privatedata/zhiwen/2025-02-22/341c01a7-de57-4e56-acfe-242ac04ab7c4/669fa4a5e2b7410e9e456288e0d4bc1e.pptx",r"D:\PROJECT\Python\test01\ceshi.pptx")

    # result = demo.get_result(taskid)
    # print("生成的PPT请从此地址获取：\n" + result)






