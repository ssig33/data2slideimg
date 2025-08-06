from PIL import Image, ImageDraw, ImageFont
from typing import Optional
from src.models import TableData
from pilmoji import Pilmoji
import os


class LayoutEngine:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.margin = 80
        self.current_y = self.margin
        self.content_start_y = self.margin  # Start of content area after title
        
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
        
        # Use Pilmoji for emoji support
        with Pilmoji(img) as pilmoji:
            # Calculate text size
            bbox = draw.textbbox((0, 0), title, font=self.title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center horizontally
            x = (self.width - text_width) // 2
            y = self.margin
            
            # Draw text with shadow
            pilmoji.text((x + 3, y + 3), title, fill=(0, 0, 0, 128), font=self.title_font)
            pilmoji.text((x, y), title, fill=(255, 255, 255), font=self.title_font)
        
        self.current_y = y + text_height + self.margin
        self.content_start_y = self.current_y
    
    def draw_text_blocks_right(self, img: Image.Image, text_blocks: list, x_start: int):
        """Draw text blocks in right column"""
        draw = ImageDraw.Draw(img)
        current_y = self.content_start_y
        right_width = self.width - x_start - self.margin
        
        with Pilmoji(img) as pilmoji:
            for text_block in text_blocks:
                # Character-based wrap for Japanese text
                lines = []
                current_line = ""
                
                for char in text_block:
                    test_line = current_line + char
                    bbox = draw.textbbox((0, 0), test_line, font=self.text_font)
                    if bbox[2] - bbox[0] > right_width:
                        if current_line:
                            lines.append(current_line)
                            current_line = char
                        else:
                            lines.append(char)
                    else:
                        current_line = test_line
                
                if current_line:
                    lines.append(current_line)
                
                # Draw lines
                for line in lines:
                    pilmoji.text((x_start, current_y), line, fill=(255, 255, 255), font=self.text_font)
                    current_y += 50
                
                current_y += 30
        
        return current_y
    
    def draw_graph_left(self, img: Image.Image, graph_img: Image.Image):
        """Draw graph image in left column"""
        # Left column dimensions
        left_width = (self.width - 3 * self.margin) // 2
        available_height = self.height - self.content_start_y - self.margin
        
        # Calculate graph size to fit left column
        graph_width = min(graph_img.width, left_width)
        graph_height = min(graph_img.height, available_height)
        
        # Maintain aspect ratio
        aspect_ratio = graph_img.width / graph_img.height
        if graph_width / graph_height > aspect_ratio:
            graph_width = int(graph_height * aspect_ratio)
        else:
            graph_height = int(graph_width / aspect_ratio)
        
        # Resize graph
        graph_img = graph_img.resize((graph_width, graph_height), Image.Resampling.LANCZOS)
        
        # Position in left column
        x = self.margin
        y = self.content_start_y
        
        # Draw gray background for graph
        draw = ImageDraw.Draw(img)
        padding = 20
        bg_x1 = x - padding
        bg_y1 = y - padding
        bg_x2 = x + graph_width + padding
        bg_y2 = y + graph_height + padding
        draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(240, 240, 240))
        
        # Paste graph
        img.paste(graph_img, (x, y), graph_img if graph_img.mode == 'RGBA' else None)
        
        # Return right column start position
        return self.margin + left_width + self.margin
    
    def draw_image_left(self, img: Image.Image, source_img: Image.Image):
        """Draw image in left column"""
        # Left column dimensions
        left_width = (self.width - 3 * self.margin) // 2
        available_height = self.height - self.content_start_y - self.margin
        
        # Calculate image size to fit left column
        img_width = min(source_img.width, left_width)
        img_height = min(source_img.height, available_height)
        
        # Maintain aspect ratio
        aspect_ratio = source_img.width / source_img.height
        if img_width / img_height > aspect_ratio:
            img_width = int(img_height * aspect_ratio)
        else:
            img_height = int(img_width / aspect_ratio)
        
        # Resize image
        source_img = source_img.resize((img_width, img_height), Image.Resampling.LANCZOS)
        
        # Position in left column
        x = self.margin
        y = self.content_start_y
        
        # Draw gray background for image
        draw = ImageDraw.Draw(img)
        padding = 20
        bg_x1 = x - padding
        bg_y1 = y - padding
        bg_x2 = x + img_width + padding
        bg_y2 = y + img_height + padding
        draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(240, 240, 240))
        
        # Paste image
        img.paste(source_img, (x, y))
        
        # Return right column start position
        return self.margin + left_width + self.margin
    
    def draw_table_right(self, img: Image.Image, table: TableData, x_start: int, y_start: int):
        """Draw table in right column"""
        draw = ImageDraw.Draw(img)
        
        # Calculate cell dimensions for right column
        num_cols = len(table.headers)
        right_width = self.width - x_start - self.margin
        cell_width = right_width // num_cols
        cell_height = 50
        
        y = y_start + 30  # Add some space before table
        
        # Draw header
        for i, header in enumerate(table.headers):
            x = x_start + i * cell_width
            # Draw cell background
            draw.rectangle([x, y, x + cell_width, y + cell_height], 
                         fill=(50, 50, 50, 200), outline=(255, 255, 255, 128))
            # Draw text
            bbox = draw.textbbox((0, 0), header, font=self.table_font)
            text_width = bbox[2] - bbox[0]
            text_x = x + (cell_width - text_width) // 2
            draw.text((text_x, y + 12), header, fill=(255, 255, 255), font=self.table_font)
        
        y += cell_height
        
        # Draw rows
        for row in table.rows:
            for i, cell in enumerate(row):
                x = x_start + i * cell_width
                # Draw cell
                draw.rectangle([x, y, x + cell_width, y + cell_height], 
                             outline=(255, 255, 255, 128))
                # Draw text
                bbox = draw.textbbox((0, 0), cell, font=self.table_font)
                text_width = bbox[2] - bbox[0]
                text_x = x + (cell_width - text_width) // 2
                draw.text((text_x, y + 12), cell, fill=(255, 255, 255), font=self.table_font)
            y += cell_height


class VerticalLayoutEngine:
    """Layout engine for vertical (9:16) format with modern styling"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.margin = 60
        self.card_margin = 40
        self.current_y = 100  # Start with safe area for notch
        
        # Try to load Japanese font
        self.font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "C:\\Windows\\Fonts\\msgothic.ttc"
        ]
        
        self.title_font = self._load_font(140)  # Enhanced size for better readability
        self.text_font = self._load_font(50)    # Increased size for mobile readability
        self.table_font = self._load_font(36)
        
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Load font with fallback"""
        for font_path in self.font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        return ImageFont.load_default()
    
    def draw_glassmorphism_rect(self, draw: ImageDraw.Draw, x1: int, y1: int, x2: int, y2: int, has_image_bg: bool = False):
        """Draw enhanced glassmorphism effect rectangle with better readability"""
        if has_image_bg:
            # Much more opaque background for image backgrounds - enhanced readability
            draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 240))
            # Stronger border
            draw.rectangle([x1, y1, x2, y2], outline=(255, 255, 255, 255), width=3)
        else:
            # Dark background for gradient backgrounds - maximum contrast with white text
            draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 200))
            # Stronger border
            draw.rectangle([x1, y1, x2, y2], outline=(255, 255, 255, 255), width=3)
    
    def draw_title_overlay(self, img: Image.Image, title: str, has_image_bg: bool = False):
        """Draw title with overlay effect"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Wrap title if too long
        max_width = self.width - 120  # Leave margin for padding
        lines = []
        
        # Check if title contains Japanese characters
        import re
        has_japanese = bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', title))
        
        if has_japanese:
            # Character-based wrapping for Japanese
            current_line = ""
            for char in title:
                test_line = current_line + char
                bbox = draw.textbbox((0, 0), test_line, font=self.title_font)
                if bbox[2] - bbox[0] > max_width:
                    if current_line:
                        lines.append(current_line)
                        current_line = char
                    else:
                        lines.append(char)
                else:
                    current_line = test_line
            
            if current_line:
                lines.append(current_line)
        else:
            # Word-based wrapping for English
            words = title.split(' ')
            current_line = ""
            
            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                bbox = draw.textbbox((0, 0), test_line, font=self.title_font)
                if bbox[2] - bbox[0] > max_width:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        lines.append(word)
                else:
                    current_line = test_line
            
            if current_line:
                lines.append(current_line)
        
        # Calculate total height with improved spacing
        line_height = 160
        total_height = len(lines) * line_height - 20  # Enhanced line spacing for readability
        
        # Center position
        y = self.current_y
        padding = 40
        
        # Draw glassmorphism background
        self.draw_glassmorphism_rect(
            draw,
            60 - padding,
            y - padding,
            self.width - 60 + padding,
            y + total_height + padding,
            has_image_bg
        )
        
        # Draw text with shadow and outline using Pilmoji
        with Pilmoji(img) as pilmoji:
            text_y = y
            for line in lines:
                # Calculate line width for centering
                bbox = draw.textbbox((0, 0), line, font=self.title_font)
                line_width = bbox[2] - bbox[0]
                x = (self.width - line_width) // 2
                
                # Black outline
                for dx, dy in [(-2,-2), (-2,2), (2,-2), (2,2), (-2,0), (2,0), (0,-2), (0,2)]:
                    pilmoji.text((x + dx, text_y + dy), line, fill=(0, 0, 0, 255), font=self.title_font)
                # Shadow
                pilmoji.text((x + 4, text_y + 4), line, fill=(0, 0, 0, 180), font=self.title_font)
                # Main text
                pilmoji.text((x, text_y), line, fill=(255, 255, 255), font=self.title_font)
                text_y += line_height
        
        self.current_y = y + total_height + padding * 2 + 40
    
    def draw_graph_card(self, img: Image.Image, graph_img: Image.Image, has_image_bg: bool = False):
        """Draw graph in a card with glassmorphism"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Card dimensions
        card_width = self.width - 2 * self.card_margin
        card_height = 400
        
        # Draw chart-specific background (light for readability)
        card_x = self.card_margin
        card_y = self.current_y
        # Light background for charts regardless of image background
        draw.rectangle([card_x, card_y, card_x + card_width, card_y + card_height], 
                      fill=(255, 255, 255, 240))
        # Border
        draw.rectangle([card_x, card_y, card_x + card_width, card_y + card_height], 
                      outline=(255, 255, 255, 255), width=3)
        
        # Resize graph to fit card
        graph_width = card_width - 40
        graph_height = card_height - 40
        aspect_ratio = graph_img.width / graph_img.height
        
        if graph_width / graph_height > aspect_ratio:
            graph_width = int(graph_height * aspect_ratio)
        else:
            graph_height = int(graph_width / aspect_ratio)
        
        graph_img = graph_img.resize((graph_width, graph_height), Image.Resampling.LANCZOS)
        
        # Center graph in card
        graph_x = card_x + (card_width - graph_width) // 2
        graph_y = card_y + (card_height - graph_height) // 2
        
        # Paste graph
        img.paste(graph_img, (graph_x, graph_y), graph_img if graph_img.mode == 'RGBA' else None)
        
        self.current_y = card_y + card_height + 40
    
    def draw_text_cards(self, img: Image.Image, text_blocks: list, has_image_bg: bool = False):
        """Draw text blocks as individual cards"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        for text_block in text_blocks:
            # Wrap text
            lines = []
            current_line = ""
            card_width = self.width - 2 * self.card_margin
            text_width = card_width - 60
            
            for char in text_block:
                test_line = current_line + char
                bbox = draw.textbbox((0, 0), test_line, font=self.text_font)
                if bbox[2] - bbox[0] > text_width:
                    if current_line:
                        lines.append(current_line)
                        current_line = char
                    else:
                        lines.append(char)
                else:
                    current_line = test_line
            
            if current_line:
                lines.append(current_line)
            
            # Calculate card height
            line_height = 60
            card_height = len(lines) * line_height + 60
            
            # Draw card
            card_x = self.card_margin
            card_y = self.current_y
            self.draw_glassmorphism_rect(
                draw,
                card_x,
                card_y,
                card_x + card_width,
                card_y + card_height,
                has_image_bg
            )
            
            # Draw text with Pilmoji and outline
            with Pilmoji(img) as pilmoji:
                text_y = card_y + 30
                for line in lines:
                    # Black outline
                    for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                        pilmoji.text((card_x + 30 + dx, text_y + dy), line, fill=(0, 0, 0, 255), font=self.text_font)
                    # Main text
                    pilmoji.text((card_x + 30, text_y), line, fill=(255, 255, 255), font=self.text_font)
                    text_y += line_height
            
            self.current_y = card_y + card_height + 30
    
    def draw_table_card(self, img: Image.Image, table: TableData, has_image_bg: bool = False):
        """Draw table in a card"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Calculate table dimensions
        num_cols = len(table.headers)
        num_rows = len(table.rows) + 1  # +1 for header
        card_width = self.width - 2 * self.card_margin
        cell_height = 60
        card_height = num_rows * cell_height + 60
        
        # Draw card
        card_x = self.card_margin
        card_y = self.current_y
        self.draw_glassmorphism_rect(
            draw,
            card_x,
            card_y,
            card_x + card_width,
            card_y + card_height,
            has_image_bg
        )
        
        # Table position within card
        table_x = card_x + 30
        table_y = card_y + 30
        table_width = card_width - 60
        cell_width = table_width // num_cols
        
        # Draw header
        for i, header in enumerate(table.headers):
            x = table_x + i * cell_width
            # Header background
            draw.rectangle(
                [x, table_y, x + cell_width, table_y + cell_height],
                fill=(255, 255, 255, 40),
                outline=(255, 255, 255, 100)
            )
            # Header text
            bbox = draw.textbbox((0, 0), header, font=self.table_font)
            text_width = bbox[2] - bbox[0]
            text_x = x + (cell_width - text_width) // 2
            draw.text((text_x, table_y + 15), header, fill=(255, 255, 255), font=self.table_font)
        
        table_y += cell_height
        
        # Draw rows
        for row in table.rows:
            for i, cell in enumerate(row):
                x = table_x + i * cell_width
                # Cell border
                draw.rectangle(
                    [x, table_y, x + cell_width, table_y + cell_height],
                    outline=(255, 255, 255, 60)
                )
                # Cell text
                bbox = draw.textbbox((0, 0), cell, font=self.table_font)
                text_width = bbox[2] - bbox[0]
                text_x = x + (cell_width - text_width) // 2
                draw.text((text_x, table_y + 15), cell, fill=(255, 255, 255), font=self.table_font)
            table_y += cell_height