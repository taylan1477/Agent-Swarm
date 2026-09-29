# AGENT SWARM - PROJE DÖKÜMANTASYONU & BAĞLAM (CONTEXT) 🤖📦

Bu döküman, **Agent Swarm** projesinin geçmişini, mimarisini, dosya yapısını ve bir sonraki yapay zeka oturumunda (Antigravity Conversation) kaldığı yerden devam edebilmesi için gerekli tüm bilgileri içerir.

---

## 🎯 Projenin Amacı ve Vizyonu
Agent Swarm, tek bir güçlü bilgisayar (HP Victus 16 - i5-13500H, RTX 4060, 32GB RAM) üzerinde çalışan, harici bir bulut VPS sunucusuna ihtiyaç duymadan paralel kodlama, refactor ve test yürüten **otonom çoklu ajan (multi-agent dev swarm)** geliştirme ortamıdır.

Ana kokpit olarak Windows üzerindeki **JetBrains Rider** kullanılırken, arka planda **WSL2 (Ubuntu 24.04)** üzerinde izole `tmux` oturumları ve `aider-chat` ajanları çalışır.

---

## 🏛️ Mimari Bileşenler

```
[Windows 11 Host]
   └── JetBrains Rider (IDE Cockpit & Terminal)
   └── AutoHotkey v2 (Hızlı Terminal Makroları ve Enjeksiyon)
         │ (WSL2 Köprüsü)
[WSL2 - Ubuntu 24.04]
   ├── Master Orchestrator (Gemini 3.1 Pro / Flash API)
   ├── Worker Agents (İzole tmux oturumlarında çalışan aider CLI ajanları)
   └── Shared State & Memory (Docker PostgreSQL + Python FastMCP Server)
```

1. **Cockpit (Rider IDE):** Geliştiricinin kodu incelediği, terminalden ajanları izlediği ana merkez.
2. **Master Orchestrator:** Yüksek seviyeli sistem mimarisi, görev dağıtımı ve kod analizini yöneten LLM beyni.
3. **Worker Agents:** Belirli klasörlere (backend, frontend, test) atanmış `aider` ajanları.
4. **Local Context / Memory (MCP):** Docker üzerinde koşan PostgreSQL veritabanı ve `src/mcp_server/server.py` aracılığıyla ajanların durum kaydetmesini sağlayan Model Context Protocol sunucusu.
5. **Automation:** Windows tarafında terminale hızlı prompt veya ajan komutları basan `automation/shortcuts.ahk`.

---

## 📂 Dosya ve Dizin Yapısı

- `README.md` - Proje mimarisi ve genel tanıtım.
- `GUIDE.md` - Rider + WSL2 + Aider adım adım kurulum rehberi.
- `docker-compose.yml` - Yerel PostgreSQL veritabanı konteyneri tanımı.
- `src/mcp_server/`
  - `server.py` - FastMCP tabanlı Python Model Context Protocol sunucusu.
  - `requirements.txt` - MCP sunucusu Python bağımlılıkları (`mcp`, `asyncpg`, `pydantic`).
- `scripts/start_swarm.sh` - WSL2 üzerinde izole `tmux` pencerelerini ve aider worker oturumlarını başlatan script.
- `automation/shortcuts.ahk` - Windows AutoHotkey v2 kısayolları (`::/worker`, Rider odaklama).
- `.aider.chat.history.md` & `.aider.input.history` - Önceki aider oturum kayıtları.

---

## 📌 Mevcut Durum ve Alınan Kararlar
1. **Neden Ara Verildi?:** Geliştirici, ilk fazda ücretsiz Gemini Flash / Pro kotaları ve aider ile testler yaptıktan sonra, mobil antrenör uygulaması (**Fit-Connect**) ve tamamen internetsiz yerel asistan (**Voice OS**) geliştirmeye odaklandı.
2. **Hedef:** Bu proje bağımsız bir repoya alındı (`taylan1477/Agent-Swarm`). Yeni oturumda bu mimari modern LLM API'leri (Gemini 2.5/3 Pro, Claude 3.7 Sonnet vb.) ile canlandırılmaya ve üretime hazır bir otonom kodlama ekibine dönüştürülmeye hazırdır.

---

## 🚀 Yeni Conversation İçin Yol Haritası (Next Steps)
1. **Docker PostgreSQL Kontrolü:** `docker-compose up -d` ile local context DB'nin ayağa kaldırılması.
2. **MCP Sunucu Testi:** `src/mcp_server/server.py` dosyasının çalıştırılıp veritabanı tablolarının doğrulanması.
3. **start_swarm.sh Güncellemesi:** Modern aider bayrakları ve Gemini model parametreleri ile `start_swarm.sh` scriptinin optimize edilmesi.
4. **Rider Terminal Entegrasyonu:** Rider içerisinden tek tuşla worker ajanlarına görev atayan akışın test edilmesi.
