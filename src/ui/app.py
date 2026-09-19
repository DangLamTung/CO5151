"""LegalPilot-VN: Autonomous Multi-Agent RAG Web Interface."""

import streamlit as st

st.set_page_config(
    page_title="LegalPilot-VN | Agentic RAG",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ LegalPilot-VN")
st.caption(
    "Autonomous Multi-Agent RAG for Cross-Statutory Synthesis, Temporal Consistency & Verifiable Compliance"
)

# Sidebar: System Status & Profiles
with st.sidebar:
    st.header("🏢 Thông tin Doanh nghiệp")
    company_name = st.text_input("Tên công ty", value="SME Tech Solution LLC")
    entity_type = st.selectbox("Loại hình", ["TNHH (LLC)", "Cổ phần (JSC)", "FDI"])
    capital = st.number_input("Vốn điều lệ (VND)", value=10_000_000_000, step=1_000_000_000)
    headcount = st.number_input("Số lao động tham gia BHXH", value=45, step=5)

    st.divider()
    st.header("⚙️ Cấu hình Agent")
    st.checkbox("Bật Selective Edge Traversal", value=True)
    st.checkbox("Bật Live vbpl.vn Update", value=True)
    st.checkbox("Bật Claim Auditor Reflection", value=True)

# Main query interface
query = st.text_area(
    "Nhập câu hỏi hoặc tình huống pháp lý cần thẩm định:",
    placeholder="Ví dụ: Công ty muốn bảo lãnh giấy phép lao động cho chuyên gia kỹ thuật nước ngoài vào năm 2026 thì cần đáp ứng những điều kiện và giấy tờ gì theo Nghị định 152 và Nghị định 70?",
    height=120,
)

col1, col2 = st.columns([1, 5])
with col1:
    submit_btn = st.button("🚀 Bắt đầu Thẩm định", type="primary", use_container_width=True)

if submit_btn and query:
    st.info("Hệ thống đang điều phối Multi-Agent (Orchestrator $\\rightarrow$ LawGraph $\\rightarrow$ VBPL $\\rightarrow$ Drafter $\\rightarrow$ Claim Auditor)...")
    st.warning("⚠️ Foundation mode: Vui lòng khởi động các backend agent để thực hiện truy vấn hoàn chỉnh.")
