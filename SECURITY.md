# Chính sách Bảo mật & Threat Model v0 — LegalPilot-VN

## 1. Phạm vi Bảo mật (Security Scope)

Hệ thống **LegalPilot-VN** được thiết kế nhằm phục vụ thẩm định tuân thủ pháp lý doanh nghiệp. Do tính chất nhạy cảm của các văn bản hành chính và dữ liệu doanh nghiệp, hệ thống áp dụng mô hình an toàn **Threat Model v0** (Yêu cầu R6 trong Đề cương D1).

### 10 Vector Tấn công Được Kiểm soát:
1. **Zero-width / Hidden Font Injection**: Bóc tách triệt để các ký tự tàng hình và BOM (`[\u200B-\u200D\uFEFF]`) bằng `InputSanitizer`.
2. **Loophole & Tax Evasion Solicitations**: Tự động từ chối và đính kèm cảnh báo pháp lý từ chối trách nhiệm.
3. **False Statute Assertions**: Phát hiện khẳng định sai lệch của người dùng để kích hoạt tra cứu thời gian thực bắt buộc trên `vbpl.vn`.
4. **System Prompt & Secret Extraction**: Ngăn chặn trích xuất system prompt, private keys và API credentials.
5. **SQL Injection**: Áp dụng 100% Parameterized Queries trên SQLite và phát hiện chuỗi SQL độc hại.
6. **Fictitious Statutes**: Phát hiện và gắn cờ các điều luật bịa đặt / không tồn tại.
7. **Courtroom Litigation Defense**: Từ chối đại diện tranh tụng tại tòa án.
8. **Unauthorized Administrative Filing Execution**: Rào chắn con người (**Human Confirmation Token Gate**) bắt buộc xác thực mã token một lần trước khi nộp hồ sơ.
9. **Denial of Service (Token Bloat & Infinite Traversal)**: Giới hạn độ dài input ($\le 8,000$ ký tự), độ sâu duyệt đồ thị ($\le 2$ hops) và số lượng văn bản tối đa ($\le 5$).
10. **Path Traversal**: Chặn các ký tự `../`, tuyệt đối hạn chế phạm vi ghi file trong thư mục `./workspace/dossiers/`.

---

## 2. Quy trình Báo cáo Lỗ hổng (Reporting a Vulnerability)

Nếu bạn phát hiện lỗ hổng bảo mật hoặc vector tấn công vượt qua được tầng Guardrails hiện tại:
1. **Không mở issue công khai** trên GitHub.
2. Gửi thông tin chi tiết (payload kiểm thử, hành vi hệ thống, log) cho nhóm phát triển hoặc tạo bản draft Security Advisory trên GitHub repository.
3. Nhóm phát triển sẽ xác minh, bổ sung quy tắc vào `configs/threat_model_rules.yaml` và phát hành bản vá trong vòng 48 giờ.
