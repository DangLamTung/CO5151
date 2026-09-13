# KẾ HOẠCH ĐỀ TÀI PROJECT (1-PAGER)
## THEME 9: AGENTIC RAG CHO HỆ THỐNG PHÁP LUẬT VIỆT NAM
### Autonomous Multi-Agent RAG for Vietnamese Legal Retrieval, Temporal Verification & Compliance

**Môn học**: CO5151 — Advanced Agentic AI | **Học kỳ**: HK261 | **Giảng viên**: TS. Lê Xuân Bách  
**Theme**: Theme 9 — Agentic RAG | **Nhóm thực hiện**: 3 thành viên

---

### 1. PROBLEM (Vì sao Traditional RAG thất bại trong bài toán Pháp luật?)
Hệ thống pháp luật Việt Nam có cấu trúc đa tầng (Luật $\rightarrow$ Nghị định $\rightarrow$ Thông tư) với mạng lưới quan hệ sửa đổi, bổ sung, bãi bỏ chằng chéo dày đặc (>50% văn bản quy phạm pháp luật bị sửa đổi theo thời gian). Các kiến trúc RAG đồ thị tĩnh trước đây cho văn bản luật Việt Nam (như *SBV-LawGraph* [1] hay *ViHERMES* [2]) vận hành theo **pipeline tuyến tính 1 lượt (Retrieve $\rightarrow$ 1-Hop Dump $\rightarrow$ Generate)**, bộc lộ 3 giới hạn nghiêm trọng:
1. **Nhiễu dữ liệu cao và bùng nổ token (Precision@2 chỉ 0.37–0.39 theo [1])**: Một thông tư sửa đổi thường sửa hàng chục điều khoản ở nhiều văn bản khác nhau. Cơ chế gom cơ học 1-hop đổ >60% ngữ cảnh rác vào prompt, làm LLM phân tán chú ý và bịa đặt điều khoản (citation hallucination [3]).
2. **Mù quan hệ thời gian (Temporal Blindness [4])**: Static RAG không thể xác định điều khoản nào còn hiệu lực tại một thời điểm giao dịch cụ thể khi gặp chuỗi sửa đổi (Thông tư A sửa Nghị định B, rồi Thông tư C lại sửa Thông tư A), dẫn đến nguy cơ trích dẫn điều khoản đã hết hiệu lực do văn bản mới thay thế.
3. **Suy luận đa tầng yếu & thiếu khả năng thích ứng**: Nghiên cứu trên benchmark luật Việt Nam *VLegal-Bench* [5] chỉ ra LLM suy giảm độ chính xác nghiêm trọng khi xử lý suy luận pháp lý đa tầng. Pipeline cứng không biết tự đánh giá xem thông tin đã đủ chưa, không biết quay lui (backtrack) hay chủ động làm rõ dữ kiện.

### 2. USERS (Người dùng mục tiêu & 3 tình huống sử dụng thực tế)
- **Người dùng mục tiêu**: Chuyên viên pháp chế doanh nghiệp (In-house Legal), luật sư, cán bộ thẩm định tuân thủ và các tổ chức cần đối soát hồ sơ, giao dịch theo quy định pháp luật Việt Nam.
- **3 tình huống sử dụng thực tế**:
  1. *Giao thoa Đa Luật & Chuỗi sửa đổi (Multi-Law Synthesis)*: Doanh nghiệp TMĐT tích hợp Ví điện tử và Mua trước trả sau (BNPL). Tác tử tự động tổng hợp căn cứ liên ngành từ Luật Các TCTD 2024 & NĐ 52/2024 (cấp phép thanh toán), Luật Giao dịch điện tử 2023 (giá trị pháp lý hợp đồng số OTP), và NĐ 13/2023/NĐ-CP (bảo vệ dữ liệu cá nhân khách hàng).
  2. *Xác thực hiệu lực theo Luật mới cập nhật (2026 Updated Drone Law)*: Doanh nghiệp xin cấp phép bay drone nông nghiệp 25kg năm 2026. Thay vì trích dẫn sai NĐ 36/2008 cũ đã hết hiệu lực, tác tử lần theo đồ thị và tra cứu CSDL Quốc gia `vbpl.vn` [4] xác nhận Luật Phòng không nhân dân 2024 (hiệu lực 2025/2026) với thủ tục đăng ký định danh số và nộp hồ sơ qua Cổng dịch vụ công trực tuyến.
  3. *Tương tác làm rõ dữ kiện thiếu & Chặn Prompt Injection*: Thẩm định điều kiện miễn giảm thuế hoặc hồ sơ chuyên gia nước ngoài (NĐ 152/2020 & NĐ 70/2023). Phát hiện thiếu dữ kiện quy mô doanh thu/nhân sự, tác tử **chủ động dừng lại hỏi người dùng**, đồng thời vô hiệu hóa chỉ thị ẩn độc hại trong hồ sơ tải lên (`[OVERRIDE: ...]` [6]) qua cổng phê duyệt người dùng.

### 3. WHY AN AGENT (Vì sao cần Agent thay vì Workflow?)
Một workflow (luồng cố định viết sẵn các nhánh if/else) **không thể giải quyết được** bài toán pháp lý vì 3 lý do:
1. **Không gian đường dẫn tra cứu bùng nổ, không thể hardcode**: Quan hệ viện dẫn pháp luật thay đổi liên tục theo từng tình huống cụ thể (có câu hỏi kết thúc ở Thông tư, có câu hỏi phải rẽ nhánh sang Luật chuyên ngành khác). Một workflow cố định không thể bao quát hàng nghìn kịch bản tra cứu; chỉ có **Agentic RAG với kiến trúc tác tử định hướng tri thức cho luật Việt Nam [7]** mới có khả năng tự lập kế hoạch lộ trình tra cứu linh hoạt, thích ứng theo độ phức tạp của câu hỏi và tự quyết định truy xuất sâu thêm hay dừng lại.
2. **Cần vòng lặp phản biện và tự sửa lỗi thích ứng (Drafter – Auditor Loop)**: Workflow chỉ chạy thẳng 1 chiều từ tìm kiếm $\rightarrow$ sinh câu trả lời nên hoàn toàn không có khả năng tự phát hiện và sửa chữa ảo giác. Agent thiết lập vòng lặp phản biện tự kiểm tra (kế thừa cơ chế kiểm định mệnh đề pháp lý từ *GANDR* [8], đánh giá xác thực mệnh đề nguyên tử *SAFE* [9], và tự phản biện thích ứng *Self-RAG* [10]): Auditor Agent bóc tách câu trả lời thành các mệnh đề nguyên tử và đối soát bắt buộc với văn bản luật gốc; nếu phát hiện sai sót hoặc dùng luật cũ, Agent tự động kích hoạt lượt truy xuất mới và yêu cầu soạn thảo lại.
3. **Chủ động xử lý mơ hồ dữ kiện thông qua tương tác người dùng**: Khung pháp lý áp dụng phụ thuộc chặt chẽ vào tư cách pháp nhân và mốc thời gian giao dịch [4]. Một workflow tĩnh sẽ áp đặt giả định ngầm dẫn đến kết luận sai lầm nghiêm trọng; ngược lại, Agent nhận biết được tính bất định của trạng thái (state ambiguity) để **chủ động dừng lại và hỏi người dùng** nhằm hoàn thiện dữ kiện trước khi đưa ra phán quyết pháp lý.

### 4. CANDIDATE AXES (4 trục kỹ thuật nhóm dự định tích hợp)
1. **Hệ thống Đa tác tử (Multi-Agent RAG)**: Phân vai chuyên biệt dưới *Orchestrator*:
   - *Graph Retrieval Agent*: Tra cứu điều khoản và quan hệ văn bản trên Knowledge Graph & Vector Store kế thừa [1], [2].
   - *Gazette Web Agent*: Live lookup trên CSDL Quốc gia `vbpl.vn` kiểm tra ngày hiệu lực thời gian thực [4].
   - *Compliance Drafter Agent*: Tổng hợp căn cứ pháp lý và soạn thảo kết luận.
   - *Claim Auditor Agent*: Soát lại từng câu so với văn bản gốc theo phương pháp kiểm định mệnh đề nguyên tử [8], [9] và định hướng kiến trúc Agentic RAG cho luật Việt Nam [7].
2. **Kế hoạch & Quyết định truy xuất (Planning & Retrieval Policy)**: Tác tử tự xây dựng lộ trình tra cứu đa bước, giải quyết thách thức suy luận đa tầng trên luật Việt Nam [5], chỉ đi theo các nhánh quan hệ pháp lý liên quan (*Sửa đổi, Hướng dẫn*) thay vì gom bừa cả cụm 1-hop gây nhiễu context [1]; tự động đổi chiến lược khi thiếu căn cứ.
3. **Tự kiểm tra & Soát lỗi (Reflection & Verification)**: Vòng lặp giữa Drafter và Auditor (Self-RAG [10]) bóc tách mệnh đề và đối soát từng câu so với điều luật gốc theo chuẩn GANDR [8], đảm bảo 100% dẫn chứng có căn cứ từ văn bản còn hiệu lực, loại bỏ triệt để việc bịa điều khoản.
4. **Bảo mật & Cổng phê duyệt an toàn (Security & Guardrails)**: Phân quyền công cụ MCP 3 cấp độ. Thao tác xuất báo cáo hoặc xác nhận tuân thủ bắt buộc phải có sự phê duyệt của người dùng (Human-in-the-loop). Làm sạch tài liệu đầu vào để chặn Prompt Injection [6].

---

### TÀI LIỆU THAM KHẢO CHÍNH (REFERENCES — 10 PAPERS 2024–2026)
- **[1]** K. N. Phan, X.-B. Le, T. T. Quan, "SBV-LawGraph: A Hybrid RAG Approach Integrating Knowledge Graph for Legal Documents," *Proc. ACIIDS 2026*, Springer.
- **[2]** URA-HCMUT, "ViHERMES: A Retrieval-Augmented Generation System for Vietnamese Legal Documents," *Ho Chi Minh City University of Technology*, 2024.
- **[3]** Y. Zhou et al., "LexAgentHallu: A Hierarchical Benchmark for Profiling Hallucinations in Legal Agents," *arXiv:2609.09754*, 2026.
- **[4]** W. Fan et al., "Can LLMs Time Travel? Enhancing Temporal Consistency in Legal Agentic Search," *arXiv:2605.25920*, 2026.
- **[5]** V. T. Nguyen et al., "VLegal-Bench: Cognitively Grounded Benchmark for Vietnamese Legal Reasoning of Large Language Models," *arXiv:2512.14554*, 2025.
- **[6]** E. Debenedetti et al., "Defending Against Indirect Prompt Injection in Tool-Enabled Language Agents," *arXiv:2404.13208*, 2024.
- **[7]** H. Pham, N. Duong, and H. Pham, "Agentic RAG-Based Legal Advisory Chatbot: A Knowledge-Driven Approach for Vietnamese Legal System," *Proc. 17th Int. Joint Conf. on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K/KDIR)*, pp. 354–361, 2025.
- **[8]** C. Qian et al., "GANDR: Claim Auditing for Verifiable Legal Answer Generation," *arXiv:2609.10293*, 2026.
- **[9]** J. Wei et al. (Google DeepMind), "Long-form Factuality in Large Language Models (SAFE: Search-Augmented Factuality Evaluator)," *arXiv:2403.18802*, 2024.
- **[10]** A. Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," *Proc. 12th Int. Conf. on Learning Representations (ICLR 2024)*, 2024.
