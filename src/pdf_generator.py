# 处理PDF生成逻辑
import os
import re

from fastapi import HTTPException
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame


def register_font(font_name, font_path):
    if not os.path.exists(font_path):
        raise RuntimeError(f"TTF Font file not found: {font_path}")
    pdfmetrics.registerFont(TTFont(font_name, font_path))


def save_to_pdf(content, title, filename):
    # 设置保存路径
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'PDF')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    c = canvas.Canvas(filepath, pagesize=letter)

    # 注册中文字体
    font_path = os.path.join(os.path.dirname(__file__), '..', 'ziti', 'simkai.ttf')
    register_font('SimKai', font_path)

    # 获取样式表
    styles = getSampleStyleSheet()
    
    # 定义标题样式
    title_style = ParagraphStyle(
        name='Title',
        fontName='SimKai',
        fontSize=24,
        leading=30,
        textColor='black',
        alignment=1,  # 居中对齐
        spaceAfter=15,  # 减小标题后的间距
        spaceBefore=5,  # 进一步减小标题上边距
    )
    
    # 定义一级标题样式
    heading1_style = ParagraphStyle(
        name='Heading1',
        fontName='SimKai',  
        fontSize=18,
        leading=27,
        textColor='black',
        alignment=0,  # 左对齐
        spaceAfter=12,
    )

    # 定义二级标题样式  
    heading2_style = ParagraphStyle(
        name='Heading2',
        fontName='SimKai',
        fontSize=16, 
        leading=24,
        textColor='black',
        alignment=0,
        spaceAfter=12,
    )
    
    # 定义三级标题样式
    heading3_style = ParagraphStyle( 
        name='Heading3',
        fontName='SimKai',
        fontSize=14,
        leading=21, 
        textColor='black',
        alignment=0,
        spaceAfter=12,
    )
    
    # 定义四级标题样式
    heading4_style = ParagraphStyle(
        name='Heading4',
        fontName='SimKai',
        fontSize=14,
        leading=18,
        textColor='black', 
        alignment=0,
        spaceAfter=12,
    )

    # 定义正文样式
    normal_style = ParagraphStyle(
        name='Normal',
        fontName='SimKai',
        fontSize=14,
        leading=18,
        textColor='black',
        alignment=0,
        firstLineIndent=24,  # 首行缩进2个字符
        spaceAfter=12,
    )

    # 定义页码样式
    page_number_style = ParagraphStyle(
        name='PageNumber',
        fontName='SimKai',
        fontSize=10,
        alignment=1,  # 居中对齐
        textColor='gray',
    )

    def add_page_number(canvas, doc):
        page_number = canvas.getPageNumber()
        text = f"第 {page_number} 页"
        p = Paragraph(text, page_number_style)
        w, h = p.wrap(frame_width, 10*mm)
        p.drawOn(canvas, (frame_width - w) / 2, 10*mm)

    # 页面设置
    margin = 0.5 * inch  # 页边距
    frame_width = letter[0] - 2 * margin 
    frame_height = letter[1] - 2 * margin

    # 创建框架
    frame = Frame(margin, margin + 5*mm, frame_width, frame_height - 35*mm)  # 调整框架位置和高度

    # 处理标题
    title_paragraph = Paragraph(title, title_style)

    # 处理内容
    def process_markdown(text):
        # 处理markdown格式
        # 加粗
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # 斜体
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # 处理标题
        text = re.sub(r'^#\s+(.*?$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        text = re.sub(r'^##\s+(.*?$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^###\s+(.*?$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^####\s+(.*?$)', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        # 去除行首的"-"号
        text = re.sub(r'^\s*-\s+', '', text, flags=re.MULTILINE)
        return text

    def create_paragraph(text, style):
        # 创建段落
        processed_text = process_markdown(text)
        return Paragraph(processed_text, style)

    paragraphs = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('# '):
            paragraphs.append(create_paragraph(line[2:], heading1_style))
        elif line.startswith('## '):
            paragraphs.append(create_paragraph(line[3:], heading2_style))
        elif line.startswith('### '):
            paragraphs.append(create_paragraph(line[4:], heading3_style))
        elif line.startswith('#### '):
            paragraphs.append(create_paragraph(line[5:], heading4_style))
        else:
            paragraphs.append(create_paragraph(line, normal_style))

    # 绘制内容
    frame.add(title_paragraph, c)
    add_page_number(c, frame)

    for paragraph in paragraphs:
        if not frame.add(paragraph, c):
            add_page_number(c, frame)
            c.showPage()
            frame = Frame(margin, margin + 5*mm, frame_width, frame_height - 35*mm)
            frame.add(paragraph, c)
    
    add_page_number(c, frame)  # 为最后一页添加页码
    c.showPage()  # 确保最后一页也生成

    c.save()


def content_to_pdf(contents, titles, filenames):
    pdf_urls = []
    for content, title, filename in zip(contents, titles, filenames):
        # 调用 save_to_pdf 函数生成 PDF
        save_to_pdf(content, title, filename)

        filepath = os.path.join(os.path.dirname(__file__), '../output/PDF', filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail=f"PDF generation failed for {filename}")

        pdf_urls.append(f"/download/{filename}")

    return pdf_urls
