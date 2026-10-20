
import requests
import streamlit as st

# API_URL = "http://127.0.0.1:8000/analyze-resume"
API_URL = "https://ai-resume-analyzer-q37q.onrender.com/analyze-resume"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Resume Analyzer")
st.markdown(
    "Upload your resume, compare it with a job description, "
    "and get AI-powered feedback to improve your application."
)

st.info(
    "Your resume will be analyzed for relevant skills, "
    "missing skills, and improvement opportunities."
)

st.subheader("Groq API key")
st.caption(
    "Enter your key for this session. It is sent to your local backend for "
    "analysis and is not saved in the project files."
)
groq_api_key = st.text_input(
    "Groq API key",
    type="password",
    key="groq_api_key",
    help="Create or manage your key in the Groq Console.",
)

# Resume upload
resume = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"],
)

# Job description
job_description = st.text_area(
    "Paste the job description",
    height=220,
    placeholder=(
        "Paste the complete job description here, "
        "including responsibilities and required skills..."
    ),
)

if st.button("Analyze My Resume", type="primary"):
    if resume is None:
        st.error("Please upload your resume as a PDF.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    elif not groq_api_key.strip():
        st.error("Please enter your Groq API key.")
    else:
        try:
            with st.spinner(
                "Analyzing your resume... This may take a little while."
            ):
                response = requests.post(
                    API_URL,
                    files={
                        "resume": (
                            resume.name,
                            resume.getvalue(),
                            "application/pdf",
                        )
                    },
                    data={
                        "job_description": job_description,
                        "groq_api_key": groq_api_key.strip(),
                    },
                    timeout=120,
                )

            if response.status_code != 200:
                try:
                    error_detail = response.json().get(
                        "detail", "Unknown API error"
                    )
                except ValueError:
                    error_detail = response.text[:500]

                st.error(
                    f"Analysis failed ({response.status_code}): "
                    f"{error_detail}"
                )

            else:
                result = response.json()
                analysis = result["analysis"]
                feedback = result["ai_feedback"]

                st.success("Resume analysis completed!")

                # Match score
                st.subheader("🎯 Resume Match Score")

                score = analysis["match_score"]

                col1, col2, col3 = st.columns(3)

                col1.metric("Match Score", f"{score}%")
                col2.metric(
                    "Matched Skills",
                    len(analysis["matched_skills"]),
                )
                col3.metric(
                    "Missing Skills",
                    len(analysis["missing_skills"]),
                )

                st.progress(score / 100)

                st.caption(
                    "This score measures keyword skill coverage. "
                    "It is not a prediction of hiring success."
                )

                # Skills analysis
                st.subheader("✅ Matched Skills")

                if analysis["matched_skills"]:
                    st.write(", ".join(analysis["matched_skills"]))
                else:
                    st.write("No matching skills detected.")

                st.subheader("📌 Skills Not Found in Resume")

                if analysis["missing_skills"]:
                    st.write(", ".join(analysis["missing_skills"]))
                    st.caption(
                        "These skills were not detected in the resume. "
                        "This does not necessarily mean you lack them."
                    )
                else:
                    st.write("All detected required skills were matched.")

                with st.expander("View all detected resume skills"):
                    st.write(
                        ", ".join(analysis["resume_skills"])
                        or "No skills detected."
                    )

                # AI feedback
                st.divider()
                st.subheader("🤖 AI-Powered Feedback")

                st.markdown("### Overall Assessment")
                st.write(feedback["summary"])

                st.markdown("### 💪 Strengths")
                for item in feedback["strengths"]:
                    st.markdown(f"- {item}")

                st.markdown("### 🛠️ Areas to Improve")
                for item in feedback["areas_to_improve"]:
                    st.markdown(f"- {item}")

                st.markdown("### ✍️ Resume Improvement Suggestions")
                for item in feedback["resume_suggestions"]:
                    st.markdown(f"- {item}")

                st.markdown("### 🎤 Potential Interview Questions")
                for index, question in enumerate(
                    feedback["interview_questions"], start=1
                ):
                    st.markdown(f"{index}. {question}")

                # Downloadable report
                report = f"""
# AI Resume Analysis Report

**Resume:** {result['filename']}

**Match Score:** {score}%

## Overall Assessment
{feedback['summary']}

## Matched Skills
{', '.join(analysis['matched_skills']) or 'None detected'}

## Skills Not Found in Resume
{', '.join(analysis['missing_skills']) or 'None'}

## Strengths
{chr(10).join('- ' + item for item in feedback['strengths'])}

## Areas to Improve
{chr(10).join('- ' + item for item in feedback['areas_to_improve'])}

## Resume Improvement Suggestions
{chr(10).join('- ' + item for item in feedback['resume_suggestions'])}

## Potential Interview Questions
{chr(10).join('- ' + item for item in feedback['interview_questions'])}
"""

                st.download_button(
                    label="⬇️ Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.md",
                    mime="text/markdown",
                )

        except requests.exceptions.Timeout:
            st.error(
                "The analysis took too long. Please try again."
            )
        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the backend. "
                # "Make sure FastAPI is running at "
                # "http://127.0.0.1:8000."
                "Please check whether the deployed FastAPI service is running."
            )
        except (KeyError, ValueError) as exc:
            st.error(
                f"The backend returned an unexpected response: {exc}"
            )
