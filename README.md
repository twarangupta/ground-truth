# GroundTruth

A retrieval-augmented question-answering assistant over public Indian financial documents (RBI, SEBI, mutual fund material), built around a real evaluation harness. It answers only from the documents, cites document and page, declines when the answer is not there, and routes risky questions to a human reviewer.

**Status: Phase 0 of 8 (repository setup).** No AI functionality exists yet. This README only describes what is built.

Everything runs on free tiers; no paid services are used.

## Requirements

- Docker Desktop
- [uv](https://docs.astral.sh/uv/) (installs Python 3.12 for the project automatically)
- GNU make (Windows: `winget install ezwinports.make`)

## Run it

```bash
make setup      # create .env from .env.example, install Python dependencies
make dev        # start Postgres + pgvector, then the API on http://127.0.0.1:8000
```

Check `http://127.0.0.1:8000/health` and the interactive API docs at `http://127.0.0.1:8000/docs`.

Other targets: `make help`.

## Checks

```bash
make check              # lint, strict type check, unit tests (same as CI)
make test-integration   # tests against the real Postgres container
```

## Repository layout

| Folder | Contents |
|---|---|
| `api/` | Python backend (FastAPI) |
| `infra/` | Docker Compose for local services |
| `data/` | Document manifest (Phase 1); downloaded PDFs are never committed |
| `eval/` | Evaluation harness (Phase 2 and 5) |
| `web/` | React frontend (Phase 7) |

## Results

NOT MEASURED. Evaluation starts in Phase 2.

## License

Code is released under the [MIT License](LICENSE). Source documents (RBI, SEBI, fund publications) are not part of this repository; they are downloaded at setup time and remain subject to their publishers' terms.
