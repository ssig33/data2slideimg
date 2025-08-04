from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
import random
import requests
import os
from src.models import SlideRequest, MapData
from src.layout import LayoutEngine, VerticalLayoutEngine
from src.graph_renderer import GraphRenderer


def download_image(url: str) -> Image.Image:
    """Download image from URL"""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def generate_map_with_marker(map_data: MapData) -> Image.Image:
    """Generate map image with red marker at center"""
    # Use Stamen Terrain tiles (free, no API key required)
    # Alternative: a.tile.openstreetmap.org
    
    # Convert lat/lon to tile coordinates
    import math
    
    n = 2.0 ** map_data.zoom
    xtile = int((map_data.lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(math.radians(map_data.lat))) / math.pi) / 2.0 * n)
    
    # Calculate how many tiles we need
    tiles_x = (map_data.width + 255) // 256
    tiles_y = (map_data.height + 255) // 256
    
    # Create base image
    map_img = Image.new('RGB', (map_data.width, map_data.height))
    
    # Download and paste tiles
    for dx in range(tiles_x):
        for dy in range(tiles_y):
            try:
                # Using OSM tile server
                tile_url = f"https://a.tile.openstreetmap.org/{map_data.zoom}/{xtile + dx - tiles_x//2}/{ytile + dy - tiles_y//2}.png"
                response = requests.get(tile_url, headers={'User-Agent': 'data2slideimg/1.0'})
                tile = Image.open(BytesIO(response.content))
                
                # Paste tile
                x = dx * 256
                y = dy * 256
                map_img.paste(tile, (x, y))
            except:
                pass  # Skip failed tiles
    
    # Crop to exact size
    map_img = map_img.crop((0, 0, map_data.width, map_data.height))
    
    # Draw red marker at center
    draw = ImageDraw.Draw(map_img)
    center_x = map_data.width // 2
    center_y = map_data.height // 2
    
    # Draw pin shape
    # Pin body (circle)
    pin_radius = 15
    draw.ellipse(
        [center_x - pin_radius, center_y - pin_radius * 2,
         center_x + pin_radius, center_y],
        fill='red',
        outline='darkred',
        width=2
    )
    
    # Pin tip (triangle)
    draw.polygon(
        [(center_x, center_y),
         (center_x - pin_radius//2, center_y - pin_radius),
         (center_x + pin_radius//2, center_y - pin_radius)],
        fill='red'
    )
    
    # Inner circle for highlight
    draw.ellipse(
        [center_x - pin_radius//2, center_y - pin_radius * 2 + 5,
         center_x + pin_radius//2, center_y - pin_radius],
        fill='white'
    )
    
    return map_img


def generate_gradient_background(width: int, height: int, vibrant: bool = False) -> Image.Image:
    """Generate random gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    if vibrant:
        # Vibrant colors for vertical format - darker for better contrast
        palettes = [
            # Darker neon gradients
            [(180, 0, 100), (0, 100, 180)],
            [(100, 0, 180), (0, 180, 100)],
            [(180, 70, 0), (180, 0, 150)],
            # Darker pastel gradients
            [(180, 140, 160), (140, 160, 180)],
            [(180, 160, 140), (140, 180, 160)],
            [(160, 140, 180), (180, 160, 140)],
        ]
        colors = random.choice(palettes)
        color1, color2 = colors
    else:
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
    
    # New layout: image/graph left, text and table right
    right_column_start = None
    
    # Priority: image > map > graph
    if request.image:
        # Download and draw image in left column
        source_img = download_image(request.image.url)
        right_column_start = layout.draw_image_left(img, source_img)
    elif request.map:
        # Generate and draw map in left column
        source_img = generate_map_with_marker(request.map)
        right_column_start = layout.draw_image_left(img, source_img)
    elif request.graph:
        # Draw graph in left column if no image
        graph_renderer = GraphRenderer()
        graph_img = graph_renderer.render_graph(request.graph)
        right_column_start = layout.draw_graph_left(img, graph_img)
    else:
        # If no image or graph, use full width for text
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


def generate_vertical_slide_image(request: SlideRequest) -> bytes:
    """Generate vertical slide image (stories format) from request data"""
    width, height = 1080, 1920  # 9:16 aspect ratio
    
    # Create base image with vibrant gradient
    img = generate_gradient_background(width, height, vibrant=True)
    
    # Use image or map as clean background if provided
    has_image_background = False
    if request.image:
        try:
            bg_img = download_image(request.image.url)
            # Maintain aspect ratio - scale to fit width and center vertically
            original_width, original_height = bg_img.size
            aspect_ratio = original_width / original_height
            
            # Scale to fit width
            new_width = width
            new_height = int(width / aspect_ratio)
            
            # If scaled image is too short, scale to fit height instead
            if new_height < height:
                new_height = height
                new_width = int(height * aspect_ratio)
            
            bg_img = bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create base image and paste centered
            img = generate_gradient_background(width, height, vibrant=True)
            paste_x = (width - new_width) // 2
            paste_y = (height - new_height) // 2
            img.paste(bg_img, (paste_x, paste_y))
            
            has_image_background = True
        except:
            pass  # Use gradient only if image fails
    elif request.map:
        try:
            # Generate map with marker as background
            bg_img = generate_map_with_marker(request.map)
            # Maintain aspect ratio - scale to fit width and center vertically
            original_width, original_height = bg_img.size
            aspect_ratio = original_width / original_height
            
            # Scale to fit width
            new_width = width
            new_height = int(width / aspect_ratio)
            
            # If scaled image is too short, scale to fit height instead
            if new_height < height:
                new_height = height
                new_width = int(height * aspect_ratio)
            
            bg_img = bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create base image and paste centered
            img = generate_gradient_background(width, height, vibrant=True)
            paste_x = (width - new_width) // 2
            paste_y = (height - new_height) // 2
            img.paste(bg_img, (paste_x, paste_y))
            
            has_image_background = True
        except:
            pass  # Use gradient only if map fails
    
    # Initialize vertical layout engine
    layout = VerticalLayoutEngine(width, height)
    
    # Draw title with glassmorphism effect
    if request.title:
        layout.draw_title_overlay(img, request.title, has_image_background)
    
    # Draw graph/data card if exists
    if request.graph:
        graph_renderer = GraphRenderer()
        graph_img = graph_renderer.render_graph(request.graph, vertical_format=True)
        layout.draw_graph_card(img, graph_img, has_image_background)
    
    # Draw text blocks as cards
    if request.textBlocks:
        text_blocks_text = [block.text for block in request.textBlocks]
        layout.draw_text_cards(img, text_blocks_text, has_image_background)
    
    # Draw table as card
    if request.table:
        layout.draw_table_card(img, request.table, has_image_background)
    
    # Convert to bytes
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()