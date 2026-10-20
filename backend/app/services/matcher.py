import re

SKILL_ALIASES = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "Pandas": ["pandas"],
    "FastAPI": ["fastapi", "fast api"],
    "LangChain": ["langchain"],
    "RAG": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
    ],
    "LLMs": [
        "llm",
        "llms",
        "large language model",
        "large language models",
    ],
    "Vector Databases": [
        "vector database",
        "vector databases",
        "vector db",
        "vector dbs",
    ],
    "PyTorch": ["pytorch", "py torch"],
    "TensorFlow": ["tensorflow"],
}


def extract_skills(text: str) -> set[str]:
    found_skills = set()

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(pattern, text, flags=re.IGNORECASE):
                found_skills.add(skill)
                break

    return found_skills


def match_resume_to_job(
    resume_text: str,
    job_description: str,
) -> dict:
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    matched_skills = resume_skills & required_skills
    missing_skills = required_skills - resume_skills

    if required_skills:
        score = round(
            len(matched_skills) / len(required_skills) * 100
        )
    else:
        score = 0

    return {
        "match_score": score,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required_skills),
        "scoring_method": "keyword_skill_coverage",
    }
