# data2slideimg

Convert JSON data to slide images.

## Usage

CLI:
```bash
uv run python -m src.cli -i input.json -o output.png
```

API:
```bash
uv run python -m src.main
```

## API Endpoints

- `POST /generate` - Generate slide image
- `GET /.well-known/schemas/slide-generator.json` - JSON Schema

## License

WTFPL