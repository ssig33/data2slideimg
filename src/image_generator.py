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
    
    # Random colors
    color1 = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    color2 = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    
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
    
    # Draw text blocks
    if request.textBlocks:
        for text_block in request.textBlocks:
            layout.draw_text_block(img, text_block.text)
    
    # Draw graphs or table
    if request.graphs:
        graph_renderer = GraphRenderer()
        for graph in request.graphs:
            graph_img = graph_renderer.render_graph(graph)
            layout.draw_graph(img, graph_img)
    elif request.table:
        layout.draw_table(img, request.table)
    
    # Convert to bytes
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()