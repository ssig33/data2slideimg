from PIL import Image, ImageDraw, ImageFont
from typing import Optional
from src.models import TableData
import os


class LayoutEngine:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.margin = 80
        self.current_y = self.margin
        
        # Try to load Japanese font
        self.font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "C:\\Windows\\Fonts\\msgothic.ttc"
        ]
        
        self.title_font = self._load_font(72)
        self.text_font = self._load_font(36)
        self.table_font = self._load_font(24)
        
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Load font with fallback"""
        for font_path in self.font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        # Fallback to default
        return ImageFont.load_default()
    
    def draw_title(self, img: Image.Image, title: str):
        """Draw title at the top"""
        draw = ImageDraw.Draw(img)
        
        # Calculate text size
        bbox = draw.textbbox((0, 0), title, font=self.title_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center horizontally
        x = (self.width - text_width) // 2
        y = self.margin
        
        # Draw text with shadow
        draw.text((x + 3, y + 3), title, fill=(0, 0, 0, 128), font=self.title_font)
        draw.text((x, y), title, fill=(255, 255, 255), font=self.title_font)
        
        self.current_y = y + text_height + self.margin
    
    def draw_text_block(self, img: Image.Image, text: str):
        """Draw text block"""
        draw = ImageDraw.Draw(img)
        
        # Word wrap
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=self.text_font)
            if bbox[2] - bbox[0] > self.width - 2 * self.margin:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        for line in lines:
            draw.text((self.margin, self.current_y), line, fill=(255, 255, 255), font=self.text_font)
            self.current_y += 50
        
        self.current_y += 30
    
    def draw_graph(self, img: Image.Image, graph_img: Image.Image):
        """Draw graph image"""
        # Calculate position
        graph_width = min(graph_img.width, self.width - 2 * self.margin)
        graph_height = min(graph_img.height, self.height - self.current_y - self.margin)
        
        # Resize if needed
        if graph_img.width != graph_width or graph_img.height != graph_height:
            graph_img = graph_img.resize((graph_width, graph_height), Image.Resampling.LANCZOS)
        
        # Center horizontally
        x = (self.width - graph_width) // 2
        
        # Paste with transparency
        img.paste(graph_img, (x, self.current_y), graph_img if graph_img.mode == 'RGBA' else None)
        
        self.current_y += graph_height + self.margin
    
    def draw_table(self, img: Image.Image, table: TableData):
        """Draw table"""
        draw = ImageDraw.Draw(img)
        
        # Calculate cell dimensions
        num_cols = len(table.headers)
        num_rows = len(table.rows) + 1  # +1 for header
        
        table_width = self.width - 2 * self.margin
        cell_width = table_width // num_cols
        cell_height = 60
        
        # Draw header
        y = self.current_y
        for i, header in enumerate(table.headers):
            x = self.margin + i * cell_width
            # Draw cell background
            draw.rectangle([x, y, x + cell_width, y + cell_height], 
                         fill=(255, 255, 255, 30), outline=(255, 255, 255, 128))
            # Draw text
            bbox = draw.textbbox((0, 0), header, font=self.table_font)
            text_width = bbox[2] - bbox[0]
            text_x = x + (cell_width - text_width) // 2
            draw.text((text_x, y + 15), header, fill=(255, 255, 255), font=self.table_font)
        
        y += cell_height
        
        # Draw rows
        for row in table.rows:
            for i, cell in enumerate(row):
                x = self.margin + i * cell_width
                # Draw cell
                draw.rectangle([x, y, x + cell_width, y + cell_height], 
                             outline=(255, 255, 255, 128))
                # Draw text
                bbox = draw.textbbox((0, 0), cell, font=self.table_font)
                text_width = bbox[2] - bbox[0]
                text_x = x + (cell_width - text_width) // 2
                draw.text((text_x, y + 15), cell, fill=(255, 255, 255), font=self.table_font)
            y += cell_height
        
        self.current_y = y + self.margin