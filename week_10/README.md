# Tuần 10: Demo Service Operation, Security & Monitoring

API demo dùng Python/FastAPI để trình bày deploy production, logging, metrics, rate limiting, circuit breaker, audit logs và cấu hình bằng environment variables.

Production URL:

```text
https://week-10-observability-api.onrender.com
```

Swagger UI:

```text
https://week-10-observability-api.onrender.com/docs
```

## Script hỗ trợ demo

Chạy từ thư mục `week_10`:

```powershell
.\scripts\demo-api.ps1 -Scenario all
```

Script mặc định gọi production URL. Nếu muốn gọi local:

```powershell
.\scripts\demo-api.ps1 -BaseUrl http://127.0.0.1:8000 -Scenario all
```

Các scenario có sẵn:

```text
health      Kiểm tra /health và /ready
items       Tạo item, list item, đồng thời tạo audit log
metrics     Gọi API rồi đọc /metrics
trace       Gọi API, lấy X-Trace-ID rồi xem /admin/traces/{trace_id}
rate-limit  Gửi nhiều POST request để tạo lỗi 429
external    Gọi external dependency để demo circuit breaker
security    Kiểm tra security headers
all         Chạy các phần an toàn, không tự spam rate-limit
```

## Các phần cần demo

### 1. Production API

Mở trên trình duyệt:

```text
https://week-10-observability-api.onrender.com/health
https://week-10-observability-api.onrender.com/docs
```

Hoặc chạy:

```powershell
.\scripts\demo-api.ps1 -Scenario health
```

Cần show:

- API có HTTPS public URL.
- `/health` trả `environment=production`.
- Swagger UI mở được và liệt kê các endpoint.

### 2. Logs và audit logs

Demo có hai nơi xem log:

- Log JSON trên Render Dashboard -> service `week-10-observability-api` -> tab `Logs`.
- Log do API tự lưu trong SQLite, xem qua endpoint `/admin/logs`.

Chạy:

```powershell
.\scripts\demo-api.ps1 -Scenario items
```

Sau đó mở:

```text
https://week-10-observability-api.onrender.com/admin/logs?limit=20
https://week-10-observability-api.onrender.com/admin/logs?event=audit_event
```

Nếu cấu hình `LOG_VIEWER_API_KEY` trên Render, cần gửi thêm header `X-Log-Viewer-Key`.

Cần show trong logs:

- `event=request_completed` cho request log.
- `method`, `path`, `status_code`, `duration_ms`.
- `event=audit_event` khi tạo item.
- `action=item_created` và `resource_id` của item vừa tạo.

Ý chính khi trình bày:

```text
API ghi log có cấu trúc ra stdout cho nền tảng deploy, đồng thời lưu một bản vào SQLite để tự truy vấn request log và audit log.
```

### 3. Metrics Prometheus

Chạy:

```powershell
.\scripts\demo-api.ps1 -Scenario metrics
```

Sau đó mở:

```text
https://week-10-observability-api.onrender.com/metrics
```

Cần show:

- Metrics dạng Prometheus text format.
- Các metric HTTP request/latency/status code.
- Custom metric `items_created_total`.

Ý chính khi trình bày:

```text
/metrics có thể được Prometheus scrape để theo dõi request count, latency và lỗi trên production.
```

### 4. Internal tracing

Chạy:

```powershell
.\scripts\demo-api.ps1 -Scenario trace
```

Script sẽ gọi `/health`, lấy header `X-Trace-ID`, rồi mở:

```text
https://week-10-observability-api.onrender.com/admin/traces/{trace_id}
```

Cần show:

- Response API có `X-Trace-ID` và header chuẩn `traceparent`.
- Trace response có `trace_id`, `service`, `root_span`, `events`.
- Các event cùng trace gồm `request_started` và `request_completed`.
- Với endpoint external hoặc tạo item, cùng `trace_id` sẽ gom thêm `external_call_*` hoặc `audit_event`.

Ý chính khi trình bày:

```text
Vì demo là mono service, app dùng internal tracing bằng trace_id để gom các log/event của một request. Khi hệ thống tách nhiều service, có thể nâng cấp sang OpenTelemetry và collector như Jaeger hoặc Tempo.
```

### 5. Rate limiting

Chạy riêng scenario này vì nó cố ý tạo lỗi:

```powershell
.\scripts\demo-api.ps1 -Scenario rate-limit
```

Cần show:

- Một số request đầu tạo item thành công.
- Khi vượt giới hạn, API trả `429 Too Many Requests`.
- Render Logs có `event=rate_limit_exceeded`.

Giới hạn hiện tại:

```text
POST /api/v1/items = 10/minute
GET /api/v1/external/status = 5/minute
```

Ý chính khi trình bày:

```text
Rate limiting bảo vệ endpoint public khỏi spam request và lạm dụng tài nguyên.
```

### 6. Circuit breaker

Trạng thái bình thường:

```powershell
.\scripts\demo-api.ps1 -Scenario external
```

Khi `EXTERNAL_FAILURE_MODE=false`, endpoint external trả `200`.

Để giả lập lỗi:

1. Mở Render Dashboard -> tab `Environment`.
2. Đổi `EXTERNAL_FAILURE_MODE=true`.
3. Chờ Render redeploy/restart.
4. Chạy lại:

```powershell
.\scripts\demo-api.ps1 -Scenario external
```

Cần show:

- Một vài request đầu trả `503 External service is unavailable`.
- Sau 3 lần fail liên tiếp, circuit breaker mở.
- Các request sau trả `503` nhanh với thông báo circuit open.
- Render Logs có `external_service_failed`, `circuit_state_changed`, `external_circuit_open`.

Sau demo nhớ đổi lại:

```text
EXTERNAL_FAILURE_MODE=false
```

Ý chính khi trình bày:

```text
Circuit breaker giúp API không gọi liên tục vào dependency đang lỗi, giảm latency và giảm tải cho hệ thống.
```

### 7. Security production cơ bản

Chạy:

```powershell
.\scripts\demo-api.ps1 -Scenario security
```

Cần show:

- Header `X-Content-Type-Options: nosniff`.
- Header `X-Frame-Options: DENY`.
- Render Environment chứa config production.
- File `.env` không được commit, chỉ có `.env.example` làm template.

Ý chính khi trình bày:

```text
Demo có các lớp bảo vệ cơ bản ở tầng ứng dụng: environment variables, security headers, validation, rate limiting và audit logs. Nếu có domain riêng có thể đặt thêm Cloudflare Free phía trước để có proxy/WAF cơ bản.
```

## Checklist trước khi demo

- Mở sẵn Render Logs.
- Mở sẵn Swagger UI.
- Chạy thử `.\scripts\demo-api.ps1 -Scenario health`.
- Chạy thử `.\scripts\demo-api.ps1 -Scenario items` để chắc logs hiện ra.
- Chỉ chạy `rate-limit` và `external` khi tới đúng phần demo vì hai phần này cố ý tạo lỗi.
