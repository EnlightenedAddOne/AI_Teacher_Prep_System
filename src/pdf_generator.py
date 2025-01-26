# 处理PDF生成逻辑
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from fastapi import HTTPException


def save_to_pdf(content, title, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    
    # 注册中文字体
    font_path = os.path.join(os.path.dirname(__file__), 'ziti', 'simkai.ttf')
    if not os.path.exists(font_path):
        raise RuntimeError(f"TTF Font file not found: {font_path}")
    
    pdfmetrics.registerFont(TTFont('SimKai', font_path))
    
    c.setFont("SimKai", 12)
    
    # 添加标题
    c.drawString(100, 750, title)
    
    # 添加内容
    text_object = c.beginText(100, 730)
    text_object.setFont("SimKai", 12)
    text_object.textLines(content)
    c.drawText(text_object)
    
    c.save()


def generate_content_and_pdf(contents, titles, filenames):
    pdf_urls = []
    for content, title, filename in zip(contents, titles, filenames):
        # 生成 PDF 文件
        save_to_pdf(content, title, filename)

        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail=f"PDF generation failed for {filename}")

        pdf_urls.append(f"/download/{filename}")

    return pdf_urls
