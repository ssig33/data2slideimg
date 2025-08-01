import click
import json
from pathlib import Path
from src.models import SlideRequest
from src.image_generator import generate_slide_image


@click.command()
@click.option('--input', '-i', type=click.File('r'), required=True, 
              help='Input JSON file')
@click.option('--output', '-o', type=click.Path(), required=True,
              help='Output PNG file path')
def generate(input, output):
    """Generate slide image from JSON input"""
    try:
        # Parse JSON input
        data = json.load(input)
        request = SlideRequest(**data)
        
        # Generate image
        image_bytes = generate_slide_image(request)
        
        # Save to file
        output_path = Path(output)
        output_path.write_bytes(image_bytes)
        
        click.echo(f"Generated slide image: {output}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    generate()