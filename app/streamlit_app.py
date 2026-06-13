from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from app.pdf_reader import extract_text_from_pdf
from app.ai_extractor import analyze_tender_text


st.set_page_config(
    page_title="Tender Document Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Tender Document Analyzer")
st.write(
    "AI-powered assistant for extracting key information from public tender documents."
)

uploaded_file = st.file_uploader(
    "Upload a tender PDF",
    type=["pdf"]
)

demo_mode = st.checkbox(
    "Run in demo mode",
    value=False,
    help="Use demo mode if you do not have an OpenAI API key configured."
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    st.success("PDF uploaded successfully.")

    if st.button("Analyze Tender"):
        with st.spinner("Extracting and analyzing tender information..."):
            text = extract_text_from_pdf(Path(temp_file_path))
            analysis = analyze_tender_text(text, demo_mode=demo_mode)

        st.subheader("Tender Analysis Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Contracting Authority",
                analysis.contracting_authority.value or "Not found"
            )
            st.metric(
                "Submission Deadline",
                analysis.submission_deadline.value or "Not found"
            )

        with col2:
            st.metric(
                "Project Title",
                analysis.tender_title.value or "Not found"
            )
            st.metric("Estimated Budget", analysis.estimated_budget.value or "Not found")

        st.subheader("Evidence")

        evidence_items = [
            ("Contracting Authority", analysis.contracting_authority),
            ("Tender Title", analysis.tender_title),
            ("Submission Deadline", analysis.submission_deadline),
            ("Estimated Budget", analysis.estimated_budget),
        ]

        for label, field in evidence_items:
            with st.expander(label):
                st.write(f"**Value:** {field.value or 'Not found'}")
                st.write(f"**Confidence:** {field.confidence}")
                st.write(f"**Page:** {field.page or 'Not available'}")
                st.write(f"**Quote:** {field.quote or 'Not available'}")

        st.divider()

        st.subheader("Summary")
        st.write(analysis.summary)

        st.subheader("Deliverables")
        st.write(analysis.deliverables or "No documents identified.")

        st.subheader("Evaluation Criteria")
        st.write(analysis.evaluation_criteria or "No criteria identified.")

        st.subheader("Technical Requirements")
        st.write(analysis.technical_requirements or "No technical requirements identified.")

        st.subheader("Risks or Missing Information")
        st.write(analysis.risks_or_missing_information or "No risks identified.")

        st.download_button(
            label="Download JSON Result",
            data=analysis.model_dump_json(indent=2),
            file_name="tender_analysis.json",
            mime="application/json"
        )