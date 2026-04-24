# FastAPI DDD Demo

## Project structure

```text
app/
├── application/      # Use cases and DTOs
├── domain/           # Entities and repository contracts
├── infrastructure/   # Repository implementations and external adapters
├── interfaces/       # HTTP controllers and dependency wiring
└── bootstrap.py      # App factory
main.py               # Application entrypoint
```

## DDD responsibilities

- `domain`: pure business objects and abstract repository interfaces
- `application`: orchestrates use cases and returns DTOs
- `infrastructure`: concrete implementations such as database or in-memory repositories
- `interfaces`: FastAPI routers, request handling, and dependency injection

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Sample endpoints

- `GET /api/health`
- `GET /api/hello/{name}`
- `POST /api/line-scan/generate`

## Line scan image generation

This project now includes a minimal line-scan image generator based on the logic in the reference code:

- decode `.raw` bytes using `width` and `channels`
- reshape the raw stream into an image
- trim rows that are fully zero
- save the generated image as a regular image file

Example request:

```json
{
  "input_path": "D:/tmp_dir1/sample.raw",
  "output_path": "output/generated/sample.bmp",
  "width": 16384,
  "channels": 1,
  "output_format": "bmp",
  "trim_zero_rows": true
}
```
