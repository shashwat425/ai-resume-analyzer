
# from griffe import logger

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.pdf_parser import extract_text_from_pdf
from app.services.matcher import match_resume_to_job
from app.services.llm_service import analyze_with_llm

# from griffe import logger

router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@router.post("/analyze-resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    groq_api_key: str = Form(...),
):
    # 1. Validate the uploaded file
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume"
        )

    # 2. Validate the job description
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty"
        )

    if not groq_api_key.strip():
        raise HTTPException(
            status_code=400,
            detail="Groq API key cannot be empty.",
        )

    # 3. Read the pdf file and check its size
    pdf_bytes = await resume.read(MAX_FILE_SIZE + 1)
    
    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the 5MB limit"
        )

    # 4. Check that the uploaded content looks like a PDF
    if not pdf_bytes.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="The Uploaded file does not appear to be a valid PDF"
        )

    # 5. Extract resume text
    try:
        resume_text = extract_text_from_pdf(pdf_bytes)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    # 6. Match resume skills against job requirements
    results = match_resume_to_job(
        resume_text,
        job_description,
    )
    
    # try:
    #     ai_feedback = analyze_with_llm(
    #         resume_text,
    #         job_description,
    #     )
    # except Exception:
    #     raise HTTPException(
    #         status_code=502,
    #         detail=(
    #             "AI analysis failed. Check the model availability, "
    #             "API key, network connection, and API usage limits."
    #         ),
    #     )
    try:
        ai_feedback = analyze_with_llm(
            resume_text,
            job_description,
            groq_api_key.strip(),
        )
    except Exception as exc:
        print(f"Groq analysis error:{type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="AI analysis failed. Check the backend terminal for details.",
        ) from exc

    # 7. Return a JSON response
    return {
        "filename": resume.filename,
        "resume_text": resume_text,
        "job_description": job_description,
        "analysis": results,
        "ai_feedback": ai_feedback,
    }
