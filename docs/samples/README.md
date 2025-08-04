# Sample Slides

This directory contains sample JSON files and their generated slide images demonstrating different chart types and table functionality.

## Chart Types

### Bar Chart
- **Input**: [bar_chart.json](bar_chart.json)
- **Horizontal**: ![Bar Chart](bar_chart.png)
- **Vertical**: ![Bar Chart Vertical](bar_chart_vertical.png)

### Line Chart
- **Input**: [line_chart.json](line_chart.json)
- **Horizontal**: ![Line Chart](line_chart.png)
- **Vertical**: ![Line Chart Vertical](line_chart_vertical.png)

### Pie Chart
- **Input**: [pie_chart.json](pie_chart.json)
- **Horizontal**: ![Pie Chart](pie_chart.png)
- **Vertical**: ![Pie Chart Vertical](pie_chart_vertical.png)

## Table Sample
- **Input**: [table_sample.json](table_sample.json)
- **Horizontal**: ![Table Sample](table_sample.png)
- **Vertical**: ![Table Sample Vertical](table_sample_vertical.png)

## Japanese Sample
- **Input**: [japanese_sample.json](japanese_sample.json)
- **Horizontal**: ![Japanese Sample](japanese_sample.png)
- **Vertical**: ![Japanese Sample Vertical](japanese_sample_vertical.png)

## Image Sample
- **Input**: [image_sample.json](image_sample.json)
- **Horizontal**: ![Image Sample](image_sample.png)
- **Vertical**: ![Image Sample Vertical](image_sample_vertical.png)

## Map Sample
- **Input**: [map_sample.json](map_sample.json) / [map_sample_vertical.json](map_sample_vertical.json)
- **Horizontal**: ![Map Sample](map_sample.png)
- **Vertical**: ![Map Sample Vertical](map_sample_vertical.png)
- **Features**: OpenStreetMap tiles with red marker at center point

## Vertical Format (Stories)
- **Input**: [vertical_sns_analysis.json](vertical_sns_analysis.json)
- **Output**: ![Vertical SNS Analysis](vertical_sns_analysis.png)
- **Format**: 1080x1920 (9:16 aspect ratio)
- **Features**: Glassmorphism cards, vibrant gradients, mobile-optimized text sizes

## Usage

To generate these samples yourself:

```bash
uv run python -m src.cli -i docs/samples/bar_chart.json -o output.png
```