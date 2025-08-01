from PIL import Image, ImageDraw
from io import BytesIO
import random
from src.models import SlideRequest
from src.layout import LayoutEngine
from src.graph_renderer import GraphRenderer


def generate_gradient_background(width: int, height: int) -> Image.Image:
    """Generate random gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Random colors - darker for better contrast with white text
    color1 = (random.randint(40, 120), random.randint(40, 120), random.randint(40, 120))
    color2 = (random.randint(20, 80), random.randint(20, 80), random.randint(20, 80))
    
    # Create gradient
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def generate_slide_image(request: SlideRequest) -> bytes:
    """Generate slide image from request data"""
    width, height = 1920, 1080
    
    # Create base image with gradient
    img = generate_gradient_background(width, height)
    
    # Initialize layout engine
    layout = LayoutEngine(width, height)
    
    # Draw title if exists
    if request.title:
        layout.draw_title(img, request.title)
    
    # New layout: graph left, text and table right
    right_column_start = None
    
    # Draw graph in left column if exists
    if request.graph:
        graph_renderer = GraphRenderer()
        graph_img = graph_renderer.render_graph(request.graph)
        right_column_start = layout.draw_graph_left(img, graph_img)
    else:
        # If no graph, use full width for text
        right_column_start = layout.margin
    
    # Draw text blocks in right column
    text_end_y = layout.content_start_y
    if request.textBlocks:
        text_blocks_text = [block.text for block in request.textBlocks]
        text_end_y = layout.draw_text_blocks_right(img, text_blocks_text, right_column_start)
    
    # Draw table below text in right column
    if request.table:
        layout.draw_table_right(img, request.table, right_column_start, text_end_y)
    
    # Convert to bytes
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()