# docusign

Automatically appends a digital signature block (text + handwritten image) to the bottom-right corner of the last page of every PDF found in the `tosign/` folder. Signed copies are written to `signed/`.

The block layout is:

```
Digitally signed
[signature image]
by: Matteo Francia
on: 11 settembre 2026
```

## Quick start

```bash
# 1. Copy the example config and fill in your details
cp config.example.yaml config.yaml

# 2. Drop your PDFs into tosign/
# 3. Run — signed copies appear in signed/
docker compose up
```

No rebuild needed when you edit `main.py`, `config.yaml`, or `signature.png`; the project directory is mounted directly into the container.

## Configuration (`config.yaml`)

| Key | Description |
|---|---|
| `name` | Full name printed in the signature block |
| `signature_path` | Path to the PNG signature image (relative to `/app` inside the container) |

`config.example.yaml` is the committed template; `config.yaml` is gitignored so personal details stay local.

## Project structure

```
docusign/
├── .devcontainer/
│   └── devcontainer.json   ← VS Code / Codespaces dev container
├── .github/
│   └── workflows/
│       └── ci.yml          ← lint → Docker build → integration smoke-test
├── tosign/                 ← put PDFs here before running
├── signed/                 ← signed PDFs appear here (gitignored)
├── signature.png           ← handwritten signature image
├── config.example.yaml     ← template — copy to config.yaml and edit
├── config.yaml             ← your config (gitignored)
├── main.py                 ← processing logic
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Development

Open the project in VS Code and choose **Reopen in Container** — the dev container uses the same `Dockerfile` and mounts the project live at `/app`, with Python, Pylance, and Ruff pre-installed.

## CI (GitHub Actions)

On every push / PR the pipeline runs three jobs in sequence:

1. **Lint** — `ruff check main.py`
2. **Docker Build** — builds the image with GHA layer caching
3. **Integration** — generates a test PDF, runs `docker compose up`, and verifies the signed output is produced
