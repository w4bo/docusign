# PDF Digital Signer

Automatically appends a digital signature block (text + image) to the last page of every PDF found in the `tosign/` folder. Signed copies are written to `signed/`.

## Quick start

```bash
# 1. Edit config.yaml with your name (signature.png is already set up)
# 2. Drop your PDFs into tosign/
# 3. Run:
docker compose up
# 4. Collect results from signed/
```

## Configuration (`config.yaml`)

| Key | Description |
|---|---|
| `name` | Full name printed in the signature block |
| `signature_path` | Path to the PNG signature image (relative to the container `/app` working dir) |

## Project structure

```
docusign/
├── tosign/          ← put PDFs here before running
├── signed/          ← signed PDFs appear here
├── signature.png    ← your handwritten signature image
├── config.yaml      ← signer name & signature image path
├── main.py          ← processing logic
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml   ← lint → Docker build → integration smoke-test
```

## GitHub Actions CI

On every push / PR the pipeline:
1. **Lint** with `ruff`
2. **Build** the Docker image (with layer caching)
3. **Integration test**: spins up the full `docker compose` stack with a generated test PDF and verifies the signed output is produced
# docusign
# docusign
