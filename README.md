<<<<<<< HEAD
# MESTA POC — Python-only edition

This edition does **not** require Node.js, npm, admin privileges, or a frontend build step.
FastAPI serves both the API and the MESTA browser UI.

## Windows — run it

Open PowerShell and go to the backend folder:

```powershell
cd C:\Users\ElSayedM18\Py\MESTA_POC_No_Node\mesta\backend
```

If your virtual environment already exists, activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If this is a fresh extracted ZIP, create it first:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create the environment file once:

```powershell
Copy-Item .env.example .env
```

Seed the demo catalog:

```powershell
python scripts\seed_products.py
```

Start MESTA:

```powershell
uvicorn app.main:app --reload
```

Open in the browser:

- MESTA UI: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Catalog JSON: http://127.0.0.1:8000/api/products

Keep that PowerShell window open while using MESTA.

## Live Visual Search / Style Me AI

Catalog browsing and deterministic catalog/search/styling code do not require Node.
Live screenshot understanding requires a configured multimodal AI provider.
Open `.env` and set the provider values described in `.env.example`, including `AI_API_KEY` and `AI_MODEL` when using live AI.
Never commit a real API key.

## Tests

```powershell
pytest
```

## Important demo note

The bundled catalog contains fictional sample brands/products for technology demonstration. It is not live partner inventory. Product cards use neutral `MESTA DEMO` placeholder imagery so the POC does not imply authorization, stock, or imagery from real brands.

## Troubleshooting

### `python` is not recognized
Python is not available in PATH. Use the Python installation already approved on the machine or ask IT to expose it in PATH.

### PowerShell blocks Activate.ps1
If policy prevents activation, you can call the venv executables directly instead:

```powershell
.venv\Scripts\python.exe scripts\seed_products.py
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Port 8000 already in use

```powershell
uvicorn app.main:app --reload --port 8001
```

Then open http://127.0.0.1:8001

### UI opens but Visual Search says AI is unavailable
The Python app is working; live multimodal analysis is not configured. Check `AI_API_KEY` and `AI_MODEL` in `.env`.

### Catalog is empty
Run:

```powershell
python scripts\seed_products.py
```

### Product image is missing
Confirm `backend\app\static\products` exists and contains `demo-001.svg` through `demo-040.svg`.
=======
# mesta
>>>>>>> ab6b14e8570c178c4d5eedceb051b0595e121e0d
