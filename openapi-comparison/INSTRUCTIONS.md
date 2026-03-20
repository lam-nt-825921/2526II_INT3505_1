# Khung Phân tích và Phương pháp Đánh giá

Tài liệu này xác định chi tiết mục tiêu, giới hạn bài tập và các tiêu chí được sử dụng để đánh giá các định dạng mô tả API.

## Mục tiêu bài tập
Mục tiêu chính là so sánh các công cụ tài liệu hóa API (**OpenAPI, API Blueprint, RAML, TypeSpec**) nhằm làm rõ ưu nhược điểm của từng định dạng. 
Từ đó đưa ra những đề xuất: chọn định dạng nào là phù hợp với từng dự án cụ thể.

## Hệ tiêu chí Đánh giá

Bài đánh giá sẽ được thực hiện dựa trên 5 tiêu chí sau:

1. **Format & Syntax (Định dạng & Cú pháp)**
   - Khả năng có thể hiểu được của tài liệu đối với con người và máy móc.
   - *Phương pháp đánh giá:* Xem xét sự cân bằng giữa mức độ thân thiện, trực quan với người dùng (human-readable) so với mức độ tối ưu, chuẩn xác cho các hệ thống phần mềm (machine-readable/parsable).

2. **Reusability & Modularity (Khả năng Tái sử dụng & Tính Module)**
   - Khả năng duy trì ranh giới tách biệt mã nguồn hợp lý khi quy mô của dự án lớn lên.
   - *Phương pháp đánh giá:* Nền tảng đó hỗ trợ chia nhỏ các file (file splitting), tái cấu trúc dữ liệu cơ sở (model inheritance), và mức độ tuân thủ nguyên lý chống lặp lại code (DRY - Don't Repeat Yourself) ra sao.

3. **Ecosystem & Tooling (Hệ sinh thái & Công cụ hỗ trợ)**
   - Khả năng phổ cập, mức độ dễ dàng tìm kiếm sự giúp đỡ của cộng đồng và các công cụ hỗ trợ.
   - *Phương pháp đánh giá:* Đánh giá độ phủ trong cộng đồng, sự đa dạng của các phần mềm hỗ trợ từ bên thứ 3 (IDE plugins, UI renderers dạng Swagger/Redoc, API Gateway integrations).

4. **Code & Test Generation (Khả năng Sinh mã & Kiểm thử tự động)**
   - Tầm ảnh hưởng đối với giai đoạn Tự động hóa (Automation layer) trong SDLC (Vòng đời phát triển phần mềm).
   - *Đánh giá chi tiết:* Kiểm thử xem mã nguồn định dạng có khả năng dịch tự động ra Client SDKs, Server Stubs hay thậm chí tự động tạo ra những bộ API Mock Servers cho môi trường Unit / End-to-end Testing hay không.

5. **Learning Curve (Gia tốc & Đường cong học tập)**
   - Hao phí về tài nguyên đào tạo và độ thích ứng khi triển khai công nghệ.
   - *Đánh giá chi tiết:* Mức độ dễ dàng tiếp cận công cụ đối với các lập trình viên mới, đặc biệt là đo lường được rào cản kỹ thuật nếu nhóm người dùng thiên về nghiệp vụ (như Technical Writer, Product Manager/Owner).

### Tiến trình thực hiện phương pháp luận
1. Tiến hành khảo sát độc lập hệ thống của từng mô hình qua lăng kính 5 tiêu chí trên. 
2. Rút ra các kết luận nền tảng (Micro-conclusions/Tiểu kết) cho từng tiêu chuẩn độc lập. 
3. Liên kết các tiểu kết để đưa ra đánh giá, nhận định bao quát lớn nhất (Macro-conclusion).

## Trình bày Kết quả
Toàn bộ hệ thống đánh giá kỹ thuật và luận điểm cuối cùng sẽ được tập hợp chuyển ngữ sang dàn ý báo cáo/slide tại [SLIDE_CONTENT.md](./SLIDE_CONTENT.md).
