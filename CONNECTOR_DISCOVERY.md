# Hotjar Connector — Connector Discovery

**Vendor API Baseline:** https://hotjar.com

## Архитектура API
- **Базовый адрес:** `https://api.hotjar.io/v1`
- **Протокол:** REST / HTTPS (JSON)
- **Аутентификация:** OAuth 2.0 Client Credentials Grant (Bearer Token)
- **Ключевые эндпоинты:**
  - сайты (/sites)
  - тепловые карты (/heatmaps)
  - записи сессий (/recordings)
  - формы опросов (/surveys)
- **Тестовая точка проверки подключения:** `GET /v1/sites`.
