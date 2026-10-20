from fastapi import FastAPI
from app.routes.analysis import router as analysis_router


app = FastAPI(
      title = "AI Resume Analyzer API",
      description = "Analyzes Resume against job description",
      version = "0.1.0",
      )

@app.get("/")
def home():
  return {
      "message" : "AI Resume Analyzer API is running"
      }
      
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }      

app.include_router(
    analysis_router,
    tags=["Resume Analysis"],
)