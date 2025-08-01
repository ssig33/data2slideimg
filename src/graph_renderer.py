import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from src.models import GraphData


class GraphRenderer:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def render_graph(self, graph_data: GraphData) -> Image.Image:
        """Render graph based on type"""
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        
        if graph_data.type == "bar":
            ax.bar(graph_data.labels, graph_data.data)
            ax.set_xlabel('Categories')
            ax.set_ylabel('Values')
        elif graph_data.type == "line":
            ax.plot(graph_data.labels, graph_data.data, marker='o')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
        elif graph_data.type == "pie":
            ax.pie(graph_data.data, labels=graph_data.labels, autopct='%1.1f%%')
            ax.axis('equal')
        
        # Save to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
        buf.seek(0)
        
        # Convert to PIL Image
        img = Image.open(buf)
        plt.close(fig)
        
        return img