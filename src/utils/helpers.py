# 工具函数文件
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],  # 或者指定允许的域名列表
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
