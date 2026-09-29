# Project Jarvis: Kullanım Kılavuzu (Guide)

Bu belge, **Project Jarvis** otonom ajan sürüsünün (swarm) nasıl kullanılacağını, yönetileceğini ve genel mimarisini açıklar.

## 1. Sistemin Çalışma Mantığı

Jarvis, bilgisayarınızda yerel olarak çalışan ve **Gemini 3.1 Pro** modeliyle güçlendirilmiş bağımsız yapay zeka ajanlarından oluşur.
* **WSL2 (Ubuntu):** Tüm sistemin kalbidir. Python, Git ve Tmux burada çalışır. Ajanlar izole Linux ortamında kod yazar.
* **Docker Desktop:** Ajanların birbirleriyle bağlamı (context) ve hafızayı paylaşabilmesi için arka planda bir PostgreSQL veritabanı barındırır.
* **Tmux (Sürü Orkestrasyonu):** Ajanların (Master, Core, Tests) her biri `tmux` adı verilen Linux sanal terminal ekranlarında 7/24 uyanık bekler.
* **Rider / AHK (Kokpit):** Windows tarafında JetBrains Rider yerleşik terminali ile WSL'e bağlanıp, AutoHotkey kısayollarıyla komutları ajanlara iletirsiniz.

---

## 2. Terminal ve Kısayol İşlemleri

Sistemi başlatmak ve kontrol etmek için Ubuntu terminalinizi açmanız yeterlidir.

### Hızlı Giriş (Sihirli Komut)
Ubuntu terminalini açtığınızda doğrudan sanal ortamı aktif etmek ve proje dizinine gitmek için şu komutu yazın:
```bash
jarvis
```

### Sürüyü (Swarm) Başlatmak
Ajanları ayağa kaldırmak için proje dizininde şu komutu çalıştırın:
```bash
./scripts/start_swarm.sh
```
*Bu betik `agent-master`, `agent-core` ve `agent-tests` adında üç ayrı oturum başlatır ve içlerinde Aider'ı aktif eder.*

---

## 3. Ajanları Yönetmek (Tmux Kullanımı)

Ajanlar arka planda çalışırken onlara komut vermek veya neler yaptıklarını izlemek için Tmux komutlarını kullanırız.

| İşlem | Komut / Tuş Kombinasyonu |
| :--- | :--- |
| **Aktif ajanları listeleme** | `tmux ls` |
| **Master Ajan'ın ekranına bağlanma** | `tmux attach -t agent-master` |
| **Core Ajan'ın ekranına bağlanma** | `tmux attach -t agent-core` |
| **Bağlı ekrandan çıkma (Arka plana atma)** | Klavyede **`Ctrl + B`** yapıp elinizi çekin, ardından **`D`** tuşuna basın. |
| **Bir ajanı tamamen kapatma/kapatmak** | Ajanın ekranındayken `exit` veya `/exit` (Aider için) yazıp çıkın. Veya dışarıdan: `tmux kill-session -t agent-master` |

---

## 4. JetBrains Rider IDE Entegrasyonu

Ajanlar WSL içinde çalışırken, kodu düzenlediğiniz yer Windows üzerindeki JetBrains Rider'dır.
Terminal ile kod editörünü aynı pencerede birleştirmek için:
1. Rider'ı açın.
2. `Settings (Ayarlar) > Tools > Terminal` menüsüne gidin.
3. **Shell path** kısmındaki PowerShell yolunu silin ve yerine `wsl.exe` yazıp kaydedin.
4. Artık Rider'ın alt penceresindeki Terminal sekmesini açtığınızda doğrudan Ubuntu terminaline düşersiniz. Buraya `jarvis` yazarak anında ajanlarınızı yönetebilirsiniz.

---

## 5. AutoHotkey (AHK) Otomasyonu

Windows üzerinde hızlı aksiyon almak için oluşturulan `automation/shortcuts.ahk` betiğine (Windows üzerinden) çift tıklayarak çalışır durumda tutun.

**Tanımlı Kısayollar:**
* `Win + Alt + S`: Hızlıca `./scripts/start_swarm.sh` komutunu yazar ve enterlar. (Aktif terminaldeyken kullanılır).
* `::/worker` (yazıp boşluk bırakın): Hızlıca görev atama şablonunu terminale enjekte eder.
* `::/master` (yazıp boşluk bırakın): Master ajana analiz görevi şablonunu enjekte eder.

---

## 6. Veritabanı ve Hafıza (MCP)

Sistemdeki ajanların durum hafızasını tutan PostgreSQL veritabanı, mevcut projelerinizle çakışmaması (ör: `trimdb`) için özel olarak **5433** portunda çalışır. Veritabanını kapatıp açmak için Ubuntu terminalinde:
* Durdurmak için: `docker compose down`
* Başlatmak için: `docker compose up -d`

*Not: MCP sunucusunu bağımsız bir terminalde veya ajanları başlatmadan önce `python src/mcp_server/server.py` komutuyla başlatabilirsiniz.*
