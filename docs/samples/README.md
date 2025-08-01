# Sample Slides

This directory contains sample JSON files and their generated slide images demonstrating different chart types and table functionality.

## Chart Types

### Bar Chart
- **Input**: [bar_chart.json](bar_chart.json)
- **Output**: ![Bar Chart](bar_chart.png)

### Line Chart
- **Input**: [line_chart.json](line_chart.json)
- **Output**: ![Line Chart](line_chart.png)

### Pie Chart
- **Input**: [pie_chart.json](pie_chart.json)
- **Output**: ![Pie Chart](pie_chart.png)

## Table Sample
- **Input**: [table_sample.json](table_sample.json)
- **Output**: ![Table Sample](table_sample.png)

## Japanese Sample
- **Input**: [japanese_sample.json](japanese_sample.json)
- **Output**: ![Japanese Sample](japanese_sample.png)

## Image Sample
- **Input**: [image_sample.json](image_sample.json)
- **Output**: ![Image Sample](image_sample.png)

## Usage

To generate these samples yourself:

```bash
uv run python -m src.cli -i docs/samples/bar_chart.json -o output.png
```