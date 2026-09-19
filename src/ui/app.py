"""LegalPilot-VN: Autonomous Multi-Agent RAG Web Interface."""

import streamlit as st

st.set_page_config(
    page_title="LegalPilot-VN | Agentic RAG",
    layout="wide",
)

st.title("LegalPilot-VN")
st.caption(
    "Autonomous Multi-Agent RAG for Cross-Statutory Synthesis, Temporal Consistency & Verifiable Compliance"
)

# Sidebar: System Status & Profiles
with st.sidebar:
    st.header("Enterprise Profile")
    company_name = st.text_input("Company Name", value="SME Tech Solution LLC")
    entity_type = st.selectbox("Entity Type", ["LLC (TNHH)", "JSC (Co phan)", "FDI Enterprise"])
    capital = st.number_input("Charter Capital (VND)", value=10_000_000_000, step=1_000_000_000)
    headcount = st.number_input("Insured Headcount", value=45, step=5)

    st.divider()
    st.header("Agent Configuration")
    st.checkbox("Enable Selective Edge Traversal", value=True)
    st.checkbox("Enable Live VBPL Update", value=True)
    st.checkbox("Enable Claim Auditor Reflection", value=True)

# Main query interface
query = st.text_area(
    "Enter legal compliance query or corporate scenario:",
    placeholder="Example: What are the document and experience requirements to sponsor an internal transfer work permit for a foreign technical specialist in 2026 under Decree 152 and Decree 70?",
    height=120,
)

col1, col2 = st.columns([1, 5])
with col1:
    submit_btn = st.button("Run Compliance Audit", type="primary", use_container_width=True)

if submit_btn and query:
    st.info(
        "Orchestrating multi-agent pipeline (Orchestrator -> LawGraph -> VBPL -> Drafter -> Claim Auditor)..."
    )
    st.warning(
        "Foundation mode: Backend agent modules are being initialized. Full workflow will be available once agents are wired."
    )
