import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from src.models import GraphData
import os


class GraphRenderer:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Set Japanese font for matplotlib
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "C:\\Windows\\Fonts\\msgothic.ttc"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    plt.rcParams['font.family'] = ['DejaVu Sans']
                    from matplotlib.font_manager import FontProperties
                    self.jp_font = FontProperties(fname=font_path)
                    break
                except:
                    continue
        else:
            self.jp_font = None
        
    def render_graph(self, graph_data: GraphData) -> Image.Image:
        """Render graph based on type"""
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        
        if graph_data.type == "bar":
            ax.bar(graph_data.labels, graph_data.data)
            ax.set_xlabel('Categories', fontproperties=self.jp_font)
            ax.set_ylabel('Values', fontproperties=self.jp_font)
            # Set Japanese font for x-axis labels
            if self.jp_font:
                ax.set_xticklabels(graph_data.labels, fontproperties=self.jp_font)
        elif graph_data.type == "line":
            ax.plot(graph_data.labels, graph_data.data, marker='o')
            ax.set_xlabel('X-axis', fontproperties=self.jp_font)
            ax.set_ylabel('Y-axis', fontproperties=self.jp_font)
            if self.jp_font:
                ax.set_xticklabels(graph_data.labels, fontproperties=self.jp_font)
        elif graph_data.type == "pie":
            ax.pie(graph_data.data, labels=graph_data.labels, autopct='%1.1f%%')
            ax.axis('equal')
            # Set Japanese font for pie chart labels
            if self.jp_font:
                for text in ax.texts:
                    text.set_fontproperties(self.jp_font)
        
        # Save to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
        buf.seek(0)
        
        # Convert to PIL Image
        img = Image.open(buf)
        plt.close(fig)
        
        return img