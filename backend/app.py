import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ats_engine import ATSEngine

app = FastAPI(title="Resume ATS Score Checker", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = Path(__file__).parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

engine = None


def get_engine() -> ATSEngine:
    global engine
    if engine is None:
        engine = ATSEngine()
    return engine


@app.get("/")
def root():
    return {"message": "Resume ATS Score Checker API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_id = str(uuid.uuid4())
    save_path = UPLOADS_DIR / f"{file_id}.pdf"

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = get_engine().analyze_resume(str(save_path))
        return {"success": True, "data": result}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        msg = str(exc)
        if "429" in msg or "quota" in msg.lower():
            raise HTTPException(
                status_code=429,
                detail=(
                    "Gemini API quota exceeded. Wait 1–2 minutes and try again. "
                    "If this keeps happening, check usage at https://ai.dev/rate-limit"
                ),
            ) from exc
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc
    finally:
        if save_path.exists():
            save_path.unlink()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
