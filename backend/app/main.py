from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.products import router as products_router
from app.api.routes.search import router as search_router
from app.api.routes.visual_search import router as visual_search_router
from app.api.routes.recreate_look import router as recreate_router
from app.api.routes.styling import router as styling_router
from app.core.config import settings
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(products_router)
app.include_router(search_router)
app.include_router(visual_search_router)
app.include_router(recreate_router)
app.include_router(styling_router)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "MESTA"}


STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(STATIC_DIR / "index.html")
