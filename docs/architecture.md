# data2slideimg Architecture

## Overview
data2slideimg is a JSON-to-slide-image generator with both CLI and API interfaces.

## Project Structure
```
data2slideimg/
├── src/
│   ├── models.py         # Pydantic data models
│   ├── main.py          # FastAPI application
│   ├── cli.py           # CLI interface
│   ├── image_generator.py # Core image generation logic
│   ├── graph_renderer.py  # Graph rendering with matplotlib
│   └── layout.py        # Layout engine for positioning elements
├── docs/                # Documentation
├── test_input.json      # Sample input file
└── README.md
```

## Core Components

### 1. Data Models (`models.py`)
- `SlideRequest`: Main request model
- `TextBlock`: Text content block
- `GraphData`: Graph configuration (bar/line/pie)
- `TableData`: Table structure with headers and rows

### 2. Image Generation (`image_generator.py`)
- `generate_gradient_background()`: Creates random gradient backgrounds
- `generate_slide_image()`: Main orchestration function

### 3. Layout Engine (`layout.py`)
- `LayoutEngine`: Manages element positioning and sizing
- Font loading with Japanese support fallback
- Automatic text wrapping and element spacing

### 4. Graph Rendering (`graph_renderer.py`)
- `GraphRenderer`: matplotlib-based graph generation
- Supports bar, line, and pie charts
- Transparent background for overlay

### 5. Interfaces
- **CLI** (`cli.py`): Command-line interface using Click
- **API** (`main.py`): FastAPI web service

## Data Flow
1. JSON input → Pydantic validation
2. Background generation (random gradient)
3. Layout calculation and element positioning
4. Text/graph/table rendering
5. Image composition and PNG output

## Key Features
- 1920x1080px output resolution
- Japanese font support with fallbacks
- Random gradient backgrounds
- Automatic layout management
- Both CLI and HTTP API interfaces
- JSON Schema generation for API documentation