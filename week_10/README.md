# Week 10 Live Demo Guide: Observability API

Huong dan nay dung de thuc hien demo truc tiep tren lop cho API Python trong thu muc `week_10`. Production URL se duoc cap nhat sau khi deploy len Render hoac nen tang tuong duong.

## 1. Muc tieu khi demo

Can show truc tiep cac y sau:

- API Python da deploy len production va co public HTTPS URL.
- Co the mo Swagger UI tren trinh duyet va goi endpoint that.
- Logs hien thi request, loi va audit event.
- Metrics Prometheus hien thi tren endpoint `/metrics`.
- Rate limiting chan request khi goi qua nhieu.
- Circuit breaker tra ve loi nhanh khi external dependency bi fail lien tiep.
- Cau hinh production khong hard-code secret, dung environment variables.

## 2. Cac cua so can mo truoc khi demo

Nen chuan bi san cac tab/cua so sau:

1. VS Code hoac editor tai thu muc `week_10`.
2. Terminal local da activate virtual environment.
3. Trinh duyet mo Swagger UI local: `http://127.0.0.1:8000/docs`.
4. Trinh duyet mo Swagger UI production: `https://<production-url>/docs`.
5. Dashboard deploy, du kien Render Web Service.
6. Tab Logs trong dashboard deploy.
7. Tab Environment trong dashboard deploy.
8. Endpoint metrics production: `https://<production-url>/metrics`.

Gia tri can cap nhat sau khi deploy:

```text
Production URL: TODO
Deploy platform: TODO
Service name: TODO
```

## 3. Chuan bi local

Chay trong PowerShell:

```powershell
cd week_10
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

File `.env` chi dung local va da duoc ignore boi `.gitignore`.

Chay API local:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Khi demo, giu terminal nay mo de show request logs local.

## 4. Luong demo de xuat

### Buoc 1: Gioi thieu code API

Mo nhanh cac file chinh:

- `app/main.py`: noi khoi tao FastAPI, middleware, router, metrics.
- `app/logging_config.py`: cau hinh JSON logging.
- `app/rate_limit.py`: cau hinh rate limit.
- `app/circuit_breaker.py`: cau hinh circuit breaker.
- `app/routes/items.py`: endpoint tao item va audit log.
- `app/routes/external.py`: endpoint gia lap external dependency.
- `.env.example`: cac bien moi truong mau.
- `render.yaml`: cau hinh deploy.
- `tests/`: test health, items, metrics, rate limit va circuit breaker.

Noi ngan gon:

```text
API duoc viet bang Python/FastAPI. Demo tap trung vao operation: logging, metrics, rate limit, circuit breaker va deploy production.
```

### Buoc 2: Show API local

Mo:

```text
http://127.0.0.1:8000/docs
```

Thu cac endpoint:

```text
GET /health
GET /ready
GET /api/v1/items
POST /api/v1/items
```

Trong khi goi endpoint, quay lai terminal local de show log dang duoc ghi truc tiep.

### Buoc 3: Show API production

Mo:

```text
https://<production-url>/docs
```

Thu lai cac endpoint:

```text
GET /health
GET /api/v1/items
POST /api/v1/items
```

Diem can noi:

```text
Day la public HTTPS URL duoc deploy tren nen tang mien phi. API khong chi chay local ma da co the truy cap tu internet.
```

### Buoc 4: Show production logs

Mo dashboard deploy, vao tab Logs.

Sau do goi API production:

```powershell
curl https://<production-url>/health
curl https://<production-url>/api/v1/items
curl -X POST https://<production-url>/api/v1/items -H "Content-Type: application/json" -d "{\"name\":\"live-demo-item\"}"
```

Can show trong log:

- Request log co method, path, status code, duration.
- Audit log khi tao item.
- Error log neu goi endpoint loi co chu dich.

Noi ngan gon:

```text
Logs dang o dang co cau truc nen co the tim kiem, loc theo event, status code hoac endpoint tren moi truong production.
```

### Buoc 5: Show metrics

Mo tren trinh duyet:

```text
https://<production-url>/metrics
```

Hoac dung terminal:

```powershell
curl https://<production-url>/metrics
```

Can chi ra cac nhom metrics:

- Tong so request.
- Latency request.
- Status code 2xx, 4xx, 5xx.
- Endpoint/path neu instrumentation co expose.

Noi ngan gon:

```text
Endpoint /metrics dung dinh dang Prometheus, co the duoc Prometheus scrape de ve dashboard Grafana sau nay.
```

### Buoc 6: Show rate limiting

Dung PowerShell goi nhanh endpoint bi gioi han:

```powershell
1..12 | ForEach-Object {
  curl -X POST https://<production-url>/api/v1/items `
    -H "Content-Type: application/json" `
    -d "{\"name\":\"rate-limit-demo-$_\"}"
}
```

Ket qua can show:

- Mot so request dau thanh cong.
- Sau khi vuot nguong, API tra ve `429 Too Many Requests`.
- Dashboard logs co request bi chan do rate limit.
- Gia tri hien tai: `POST /api/v1/items` bi gioi han `10/minute`.

Neu muon test local thi thay production URL bang:

```text
http://127.0.0.1:8000
```

### Buoc 7: Show circuit breaker

Endpoint demo:

```text
GET /api/v1/external/status
```

Kich ban can show:

1. Dat `EXTERNAL_FAILURE_MODE=true` trong `.env` local hoac trong Environment Variables cua Render.
2. Restart API de config moi co hieu luc.
3. Goi endpoint nhieu lan:

```powershell
1..6 | ForEach-Object {
  curl https://<production-url>/api/v1/external/status
}
```

4. Sau 3 lan fail, circuit breaker open.
5. API tra ve `503 Service Unavailable` nhanh.
6. Logs co event `circuit_state_changed` va `external_circuit_open`.

Response mau khi circuit open:

```json
{
  "detail": "External service circuit is open"
}
```

### Buoc 8: Show environment variables va secret handling

Mo tab Environment tren dashboard deploy.

Chi show cac bien khong nhay cam, vi du:

```text
APP_ENV=production
LOG_LEVEL=INFO
RATE_LIMIT_DEFAULT=60/minute
RATE_LIMIT_WRITE=10/minute
RATE_LIMIT_EXTERNAL=5/minute
EXTERNAL_FAILURE_MODE=false
```

Khong mo hoac doc secret neu co.

Noi ngan gon:

```text
Config production duoc dua qua environment variables. Secret khong commit vao source code va khong nam trong repository.
```

### Buoc 9: Noi ve WAF va bao ve production

Neu co domain rieng va dung Cloudflare:

```text
API co the dat sau Cloudflare Free de co lop proxy/WAF co ban, HTTPS va rule chan traffic xau.
```

Neu chua co domain:

```text
Trong demo mien phi nay, API da co cac lop bao ve trong ung dung: validation, rate limiting, audit logs va structured error handling. WAF se la lop bo sung khi co domain/proxy nhu Cloudflare.
```

## 5. Lenh nhanh dung khi demo

Local:

```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/metrics
curl http://127.0.0.1:8000/api/v1/items
```

Production:

```powershell
curl https://<production-url>/health
curl https://<production-url>/metrics
curl https://<production-url>/api/v1/items
```

Tao item:

```powershell
curl -X POST https://<production-url>/api/v1/items -H "Content-Type: application/json" -d "{\"name\":\"demo-item\"}"
```

Rate limit:

```powershell
1..12 | ForEach-Object {
  curl -X POST https://<production-url>/api/v1/items `
    -H "Content-Type: application/json" `
    -d "{\"name\":\"rate-limit-demo-$_\"}"
}
```

Circuit breaker:

```powershell
1..6 | ForEach-Object {
  curl https://<production-url>/api/v1/external/status
}
```

## 6. Checklist truoc khi len demo

- Local API chay duoc.
- Test local pass voi `.\.venv\Scripts\python.exe -m pytest`.
- Production URL mo duoc.
- `/docs` production mo duoc.
- `/metrics` production mo duoc.
- Logs dashboard dang hien request moi.
- Rate limit co the tao ra `429`.
- Circuit breaker co the tao ra `503`.
- Environment variables da cau hinh tren platform deploy.
- Khong co `.env` hoac secret bi commit.

## 7. Phan se cap nhat sau khi code API xong

- Production URL that.
- Ten service deploy that.
- Neu deploy tren nen tang khac Render, cap nhat build command/start command theo platform do.
