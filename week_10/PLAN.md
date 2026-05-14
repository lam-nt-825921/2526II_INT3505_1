# Week 10 Plan: Service Operation, Security & Monitoring

## 1. Muc tieu demo

Thiet ke va trien khai mot API Python don gian len moi truong production mien phi, co cac thanh phan van hanh co ban:

- Deploy API len public URL.
- Logging co cau truc de theo doi request, loi va hanh vi quan trong.
- Metrics Prometheus de quan sat request count, latency, status code.
- Rate limiting de bao ve endpoint.
- Circuit breaker de tranh goi lien tuc den dependency bi loi.
- Audit logs cho cac hanh dong co tac dong den du lieu.
- Cau hinh production co HTTPS, bien moi truong, secret khong commit vao git.

## 2. Pham vi API

Ten demo: `week_10_observability_api`

Chuc nang API nen giu nho de tap trung vao operation/security:

- `GET /health`: kiem tra service con song.
- `GET /ready`: kiem tra service san sang nhan traffic.
- `GET /api/v1/items`: lay danh sach item trong bo nho.
- `POST /api/v1/items`: tao item moi, co audit log.
- `GET /api/v1/external/status`: gia lap goi den external service, dung circuit breaker.
- `GET /metrics`: expose Prometheus metrics.

Du lieu demo co the luu in-memory de khong phai cau hinh database. Neu can giong production hon, them SQLite sau.

## 3. Cong nghe su dung

Ngon ngu bat buoc: Python.

Framework va thu vien du kien:

- `fastapi`: xay dung REST API.
- `uvicorn[standard]`: ASGI server.
- `pydantic-settings`: quan ly config bang environment variables.
- `python-json-logger`: ghi log dang JSON, thay cho Winston vi demo dung Python.
- `prometheus-fastapi-instrumentator`: tu dong do metrics HTTP cho FastAPI.
- `slowapi`: rate limiting theo IP/client.
- `pybreaker`: circuit breaker cho dependency ben ngoai.
- `httpx`: HTTP client cho external call demo.
- `pytest` va `httpx`: test API co ban.

## 4. Cau truc thu muc du kien

```text
week_10/
  README.md
  PLAN.md
  requirements.txt
  .env.example
  render.yaml
  app/
    __init__.py
    main.py
    config.py
    logging_config.py
    metrics.py
    rate_limit.py
    circuit_breaker.py
    schemas.py
    audit.py
    routes/
      __init__.py
      health.py
      items.py
      external.py
  tests/
    test_health.py
    test_items.py
    test_rate_limit.py
```

## 5. Cac buoc thuc hien

### Buoc 1: Tao moi truong ao va cai dependencies

Lenh tren Windows PowerShell:

```powershell
cd week_10
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" pydantic-settings python-json-logger prometheus-fastapi-instrumentator slowapi pybreaker httpx pytest
pip freeze > requirements.txt
```

### Buoc 2: Tao FastAPI app toi thieu

- Tao `app/main.py`.
- Dang ky router health, items, external.
- Them middleware ghi request log.
- Them exception handler de log loi co cau truc.
- Chay local bang:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Buoc 3: Logging

Can co cac log toi thieu:

- Request log: method, path, status_code, duration_ms, client_ip.
- Error log: exception type, message, path.
- Audit log: hanh dong tao item, thoi gian, client_ip, request_id neu co.

Dung JSON log de de doc tren Render logs, Railway logs hoac New Relic/Datadog neu dung goi GitHub Education.

Vi du truong log:

```json
{
  "timestamp": "2026-05-14T10:00:00Z",
  "level": "INFO",
  "event": "request_completed",
  "method": "POST",
  "path": "/api/v1/items",
  "status_code": 201,
  "duration_ms": 12.4
}
```

### Buoc 4: Metrics voi Prometheus

- Cai `prometheus-fastapi-instrumentator`.
- Expose `/metrics`.
- Xac minh local:

```powershell
curl http://127.0.0.1:8000/metrics
```

Metrics can quan sat:

- Tong so request theo endpoint/status.
- Latency request.
- So request loi 4xx/5xx.
- Custom metric neu can: tong so item da tao.

### Buoc 5: Rate limiting

Dung `slowapi`:

- Gioi han mac dinh: `60/minute`.
- Endpoint tao item: `10/minute`.
- Endpoint external: `5/minute`.
- Tra ve HTTP `429 Too Many Requests` khi vuot gioi han.

Kiem thu bang `curl`, PowerShell loop hoac `hey.exe` co san trong repo.

### Buoc 6: Circuit breaker

Dung `pybreaker` cho endpoint `GET /api/v1/external/status`:

- Gia lap external dependency bang mot ham co ty le loi hoac goi den URL cau hinh qua env.
- Neu loi lien tiep qua nguong, circuit chuyen sang open.
- Khi open, API tra ve `503 Service Unavailable` nhanh, khong tiep tuc goi dependency.
- Ghi log su kien circuit open/half-open/closed.

### Buoc 7: Security production

Cau hinh toi thieu:

- Chi lay config tu environment variables, khong hard-code secret.
- Tao `.env.example`, khong commit `.env`.
- Bat HTTPS thong qua platform deploy.
- Them CORS chi cho phep domain can thiet, khong dung `*` trong production neu co frontend.
- Them rate limiting cho endpoint public.
- Ghi audit log cho hanh dong thay doi du lieu.
- Them header bao mat co ban neu can: `X-Content-Type-Options`, `X-Frame-Options`.

WAF:

- Neu deploy Render/Railway free thi WAF khong day du nhu cloud enterprise.
- Cach mien phi de trinh bay trong demo: dung Cloudflare free plan lam DNS/proxy truoc API neu co domain.
- Neu khong co domain, mo ta WAF la phan nang cao va dung rate limit + validation + audit logs lam lop bao ve trong API.

### Buoc 8: Deploy mien phi

Lua chon uu tien:

1. Render Free Web Service
   - Phu hop demo FastAPI nho.
   - Co public HTTPS URL.
   - Co log tren dashboard.
   - Can `requirements.txt` va start command.

2. Railway qua GitHub Student Developer Pack neu tai khoan co credits
   - Deploy nhanh tu GitHub repo.
   - Phu hop demo API.
   - Can kiem tra credits hien co trong dashboard GitHub Education/Railway.

3. Heroku qua GitHub Student Developer Pack neu offer con kha dung voi tai khoan
   - Deploy Python app bang Procfile.
   - Can kiem tra offer hien tai vi quyen loi Student Pack co the thay doi.

Khuyen nghi cho demo: Render, vi it phu thuoc credits va du de trinh bay production URL.

File deploy du kien:

```yaml
# render.yaml
services:
  - type: web
    name: week-10-observability-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Buoc 9: Kiem thu

Test can co:

- `GET /health` tra ve `200`.
- `POST /api/v1/items` tao item thanh cong va co status `201`.
- Vuot rate limit tra ve `429`.
- Khi external dependency loi lien tiep, circuit breaker tra ve `503`.
- `/metrics` tra ve noi dung Prometheus.

Lenh chay test:

```powershell
pytest
```

### Buoc 10: Noi dung README can viet sau khi code xong

README nen co:

- Mo ta API.
- Cach tao virtual environment.
- Cach chay local.
- Danh sach endpoint.
- Cach xem logs.
- Cach xem metrics.
- Cach test rate limit.
- Cach deploy Render.
- Public URL sau khi deploy.
- Anh chup man hinh dashboard logs/metrics neu can nop bai.

## 6. Tieu chi hoan thanh

- API Python chay local thanh cong.
- Co public production URL tren nen tang mien phi.
- `/health` va `/metrics` truy cap duoc.
- Logs hien thi duoc request va audit event.
- Rate limit tra ve `429` khi bi goi qua nhieu.
- Circuit breaker tra ve `503` khi dependency loi lien tiep.
- Co tai lieu huong dan trong `README.md`.
- Khong commit `.env`, token, secret hoac credential.

## 7. Tai lieu tham khao

- GitHub Education Student Developer Pack: https://education.github.com/pack
- Render Free: https://render.com/docs/free
- Render Python/FastAPI deploy docs: https://render.com/docs/deploy-fastapi
- Prometheus FastAPI Instrumentator: https://github.com/trallnag/prometheus-fastapi-instrumentator
- SlowAPI: https://github.com/laurentS/slowapi
- PyBreaker: https://github.com/danielfm/pybreaker
