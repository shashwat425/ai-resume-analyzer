Terminal 1 — FastAPI backend

Run this from the backend directory:
uvicorn main:app --reload


Terminal 2 — Streamlit frontend

Navigate to your project root:
cd C:\Users\shash\Desktop\ai-resume-analyzer


If the virtual environment isn't activated in this terminal, activate it:
.\backend\myenv\Scripts\Activate.ps1


Then launch the frontend:
streamlit run frontend/app.py