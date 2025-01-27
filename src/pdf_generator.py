# 处理PDF生成逻辑
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from fastapi import HTTPException


def register_font(font_name, font_path):
    if not os.path.exists(font_path):
        raise RuntimeError(f"TTF Font file not found: {font_path}")
    pdfmetrics.registerFont(TTFont(font_name, font_path))


def save_to_pdf(content, title, filename):
    # 字号定义
    FONT_SIZE_XIAOER = 20  # 小二号
    FONT_SIZE_SANHAO = 18  # 三号
    FONT_SIZE_XIAOSAN = 16  # 小三
    FONT_SIZE_SIHAO = 14  # 四号（正文）
    FONT_SIZE_XIAOWU = 9  # 小五号（页码）

    # 设置保存路径
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'teaching_designs', 'pdf')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    c = canvas.Canvas(filepath, pagesize=letter)

    # 注册中文字体
    font_path = os.path.join(os.path.dirname(__file__), 'ziti', 'simkai.ttf')
    register_font('SimKai', font_path)

    # 设置字体大小为小四号(12pt)
    font_size = 12
    c.setFont("SimKai", font_size)

    # 页面设置
    margin_left = 50
    margin_right = 50
    max_width = letter[0] - margin_left - margin_right

    # 设置1.5倍行间距
    base_line_height = font_size  # 基础行高等于字体大小
    line_spacing = 1.5  # 1.5倍行距
    line_height = base_line_height * line_spacing

    # 计算每页最大行数
    page_top_margin = 100  # 页面顶部留白
    max_lines_per_page = int((letter[1] - page_top_margin) / line_height) - 1

    def split_text_to_lines(text, max_width):
        """将文本分割成适合页面宽度的多行"""
        lines = []
        paragraphs = text.split('\n')
        
        def process_line(line, add_indent=False):
            """处理单行文本，根据宽度进行换行"""
            if add_indent:
                line = '    ' + line
            words = list(line)
            current_line = ""
            for word in words:
                test_line = current_line + word
                if c.stringWidth(test_line, "SimKai", FONT_SIZE_SIHAO) <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            
            if not paragraph:
                continue
                
            # 检查是否为加粗或斜体文本
            if '**' in paragraph or '*' in paragraph:
                text = paragraph.replace('**', '').replace('*', '')
                process_line(text)
                continue
                
            # 检查是否为markdown标题
            if paragraph.startswith('#'):
                heading_level = len(paragraph.split()[0])
                text = paragraph[heading_level:].strip()
                process_line(text)
                continue
                
            # 检查是否为数字标题
            is_title = any([
                paragraph.startswith(str(i) + '.') for i in range(1, 10)
            ]) or any([
                paragraph.startswith(f'({i})') for i in range(1, 10)
            ])
            
            if is_title:
                process_line(paragraph)
            else:
                process_line(paragraph, True)  # 非标题添加缩进
        
        return lines

    def draw_text(c, text_object, line, font_size, is_centered=False):
        """处理文本渲染"""
        text_object.setFont("SimKai", font_size)
        if is_centered:  # 只有主标题居中
            text_width = c.stringWidth(line, "SimKai", font_size)
            text_x = (letter[0] - text_width) / 2 - margin_left
            text_object.moveCursor(text_x, 0)
            text_object.textLine(line)
            text_object.moveCursor(-text_x, 0)
        else:
            text_object.textLine(line)

    # 创建文本对象
    text_object = c.beginText(margin_left, letter[1] - page_top_margin)
    text_object.setFont("SimKai", FONT_SIZE_SIHAO)
    text_object.setLeading(line_height)  # 设置行间距

    # 绘制标题
    draw_text(c, text_object, title, FONT_SIZE_XIAOER, True)

    # 处理内容
    text_lines = split_text_to_lines(content, max_width)
    current_line = 0
    page_number = 1

    for line in text_lines:
        if current_line >= max_lines_per_page:
            c.drawText(text_object)
            c.setFont("SimKai", FONT_SIZE_XIAOWU)
            c.drawString(letter[0] / 2, 20, str(page_number))
            c.showPage()
            page_number += 1
            text_object = c.beginText(margin_left, 750)
            text_object.setFont("SimKai", FONT_SIZE_SIHAO)
            text_object.setLeading(line_height)
            current_line = 0

        # 检查标题级别
        if line.startswith('#'):
            heading_level = len(line.split()[0])  # 计算#的数量
            text = line[heading_level:].strip()
            if heading_level == 1:  # 一级标题，三号
                draw_text(c, text_object, text, FONT_SIZE_SANHAO, False)
                text_object.setLeading(line_height * 1.5)  # 标题增加行间距
            elif heading_level == 2:  # 二级标题，小三
                draw_text(c, text_object, text, FONT_SIZE_XIAOSAN, False)
                text_object.setLeading(line_height * 1.2)
            elif heading_level == 3:  # 三级标题，四号
                draw_text(c, text_object, text, FONT_SIZE_SIHAO, False)
            text_object.setLeading(line_height)  # 恢复正常行间距
        else:
            # 正文使用四号字
            text_object.setFont("SimKai", FONT_SIZE_SIHAO)  # 确保设置字体
            draw_text(c, text_object, line, FONT_SIZE_SIHAO, False)

        current_line += 1

    # 处理最后一页
    c.drawText(text_object)
    c.setFont("SimKai", FONT_SIZE_XIAOWU)
    c.drawString(letter[0] / 2, 20, str(page_number))
    c.save()


def content_to_pdf(contents, titles, filenames):
    pdf_urls = []
    for content, title, filename in zip(contents, titles, filenames):
        # 调用 save_to_pdf 函数生成 PDF
        save_to_pdf(content, title, filename)

        filepath = os.path.join(os.path.dirname(__file__), '../output/teaching_designs/pdf', filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail=f"PDF generation failed for {filename}")

        pdf_urls.append(f"/download/{filename}")

    return pdf_urls
