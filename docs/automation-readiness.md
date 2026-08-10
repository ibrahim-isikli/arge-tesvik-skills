# Otomasyon Hazırlığı — Mevcut Durum Analizi

Bu doküman, repoyu şu hedef otomasyon modeline göre değerlendirir:

```
push → validate → tests → output contract checks → Claude review → PASS/FAIL
```

**Bu bir workflow implementasyonu değildir** — sadece mevcut script/test envanterinin bu modele göre nereye oturduğunu, hangi parçaların CI'da gerçekten çalıştırılabileceğini ve hangilerinin çalıştırılmaması gerektiğini analiz eder.

**Güncelleme:** Bu depoda kısa bir süre `.github/workflows/validate.yml` adında minimal bir CI workflow'u vardı (`scripts/validate.py`'ı push/pull_request'te çalıştırıyordu). Bu workflow kaldırıldı çünkü depo sahibinin GitHub hesabı, reponun içeriğiyle ilgisi olmayan bir billing kilidi nedeniyle Actions job'larını hiç başlatamıyordu ("The job was not started because your account is locked due to a billing issue.") ve depo sahibi GitHub Actions'a bağımlı olmak istemedi. Aşağıdaki analiz, "CI'da çalışıyor" ifadelerini artık **potansiyel/varsayımsal** olarak okuyun — şu an hiçbir şey otomatik çalışmıyor, hepsi elle (`python3 scripts/validate.py`) çalıştırılıyor.

## 1. Envanter: hangi script/test ne gerektiriyor

| Bileşen | Deterministik mi? | Network/MCP gerekli mi? | Claude API/CLI gerekli mi? | CI'da şu an çalışıyor mu? |
|---|---|---|---|---|
| `scripts/validate.py` | **Evet** — stdlib, aynı girdi = aynı çıktı | Hayır | Hayır | **Hayır** — CI workflow'u kaldırıldı (hesap billing kilidi); şu an sadece elle çalıştırılıyor |
| `skills/gider-kalemi-kontrolu/scripts/check_table.py` | **Evet** — stdlib | Hayır | Hayır (ama girdisi genelde bir Claude çıktısıdır) | Hayır |
| `tests/*/eval-scenarios.md` (7 dosya) | Hayır — LLM çıktısı, insan/LLM-grader yorumu gerekir | Evet (bazıları: cagri-tarama, patent-on-arastirma) | **Evet** (`claude -p --plugin-dir .`) | Hayır |
| `tests/golden/` (framework, henüz proje verisi yok) | Kısmen — `expected/*.yaml` deterministik, karşılaştırma adımı değil | Skill'e göre değişir | **Evet** | Hayır |
| Bu audit turlarında yapılan runtime regression testleri | Hayır | Evet | **Evet** | Hayır (manuel, bu oturumlarda elle çalıştırıldı) |

## 2. CI'da çalışması gereken (hedef modelin "validate" ve "output contract checks" adımları)

- **`scripts/validate.py`** — CI'da çalışmıyor (workflow kaldırıldı), ama teknik olarak buna en uygun aday: deterministik, hızlı (<1sn), bağımlılıksız, secret gerektirmiyor. Hedef modelin "validate" adımının tam karşılığı — GitHub Actions dışında bir CI sağlayıcısı (veya hesap billing sorunu çözülürse tekrar GitHub Actions) kullanılırsa yeniden bağlanabilir.
- **`skills/gider-kalemi-kontrolu/scripts/check_table.py`** — CI'da **doğrudan** çalıştırılamaz çünkü girdisi (bir gider tablosu) yoktur; bir Claude oturumunun ürettiği çıktıya ihtiyaç duyar. CI'da anlamlı olması için ya (a) sabit bir örnek tablo dosyası test-fixture olarak commit edilip script buna karşı çalıştırılabilir (bu, script'in kendi doğruluğunu test eder, skill'in davranışını değil), ya da (b) bir "Claude review" adımının çıktısı olarak üretilip ardından bu script'e verilir (aşağıya bakın). Şu an ikisi de kurulu değil.

## 3. CI'da çalıştırılMAMALI (network/LLM bağımlılığı, non-determinism, maliyet)

- **`tests/*/eval-scenarios.md` senaryolarının otomatik koşulması** — her koşu gerçek bir `claude -p` çağrısı, dolayısıyla: (a) para maliyeti var, (b) çıktı LLM'in doğası gereği tam deterministik değil (aynı senaryo iki farklı koşuda farklı ama eşdeğer kalitede metin üretebilir), (c) dış servis bağımlılığı (`cagri-tarama` → tubitak.gov.tr, `patent-on-arastirma` → markapatent-mcp) CI'ı **kırılgan** yapar — bu audit turunda markapatent-mcp'nin gerçekten üretimde bozuk olduğu bulundu (Capsolver bakiye sorunu); bu servis bozukken bir CI job'ı "FAIL" dönerdi ama bu repo kodunun hatası olmazdı. Her push'ta bunları çalıştırmak yanlış negatiflerle CI'ı güvenilmez hale getirir.
- **`tests/golden/` karşılaştırmaları** — henüz otomatik bir grader script'i yok (`tests/golden/README.md`'de bilinçli olarak "şu an değerlendirme manueldir" diye belirtilmiş). Otomatikleştirilmeden CI'a bağlanmamalı.
- Bu audit turlarındaki gibi geniş kapsamlı runtime regresyon koşuları (13+ senaryo) — maliyet ve süre nedeniyle her push'ta değil, en fazla zamanlanmış (ör. haftalık) veya manuel tetiklenen bir job olarak düşünülmeli.

## 4. "Claude review" adımı için gereksinimler (henüz kurulu değil)

Hedef modeldeki "Claude review" adımı (ör. `tests/` senaryolarını veya `tests/golden/`'ı gerçek bir Claude oturumuyla çalıştırıp derecelendirme) kurulursa, aşağıdakiler gerekir:

- **Secret**: `ANTHROPIC_API_KEY` (veya `claude setup-token` ile üretilen uzun ömürlü bir OAuth token) — GitHub repository secrets'a eklenmesi gerekir. Şu an repoda böyle bir secret **yok** (validate.py'nin buna ihtiyacı olmadığı için eklenmedi).
- **Bütçe kontrolü**: bu audit turlarında kullanılan `--max-budget-usd` gibi bir üst sınır olmadan CI'da her PR'da model çağrısı yapmak maliyeti öngörülemez hale getirir.
- **Flakiness kabulü**: MCP/web bağımlı senaryolar için CI'ın "bu dış servis şu an kullanılamıyor" durumunu FAIL değil BLOCKED/SKIP olarak ele alması gerekir — aksi halde markapatent-mcp gibi bir üçüncü taraf servisin arızası, kodda hiçbir hata olmadan CI'ı kırmızıya çevirir (tam olarak bu turda karşılaşılan durum).
- **Grading mekanizması**: LLM çıktısının `tests/*/eval-scenarios.md`'deki "Beklenen davranış" maddeleriyle otomatik karşılaştırılması için ayrı bir tasarım gerekir (ör. ikinci bir Claude çağrısı "grader" olarak, ya da anahtar kelime/regex tabanlı basit kontroller) — bu depoda henüz yok.

## 5. Şu anki gerçekçi otomasyon seviyesi

```
push/PR → scripts/validate.py (CI'da, gerçek, deterministik)  ❌ CI'da değil (elle çalıştırılıyor)
       → skill davranış testleri                               ❌ kurulu değil (manuel)
       → output contract checks (check_table.py)                ❌ kurulu değil (manuel)
       → Claude review                                          ❌ kurulu değil, secret yok
       → PASS/FAIL                                               yok (tamamen manuel)
```

Yani hedef modelin **hiçbir adımı** şu an otomatik/CI'da çalışmıyor — `scripts/validate.py` teknik olarak buna en hazır bileşen olsa da, GitHub Actions'a bağlı bir CI olmadığı için commit öncesi elle çalıştırılması gerekiyor. Geri kalanı (skill davranış testleri, output contract checks, Claude review) zaten bilinçli olarak manuel/insan-tetiklemeli bırakılmıştı çünkü LLM-bağımlı adımların CI'a bağlanması maliyet, non-determinism ve dış servis kırılganlığı riski taşıyor.

## 6. Öneri (uygulanmadı, sadece kayıt)

Eğer ileride bu modele yaklaşılmak istenirse, en düşük riskli sıradaki adım muhtemelen şu olurdu: `tests/golden/`'a gerçek bir proje eklemek + basit bir "expected/findings.yaml'daki `source_quote_contains` alanlarının çıktıda geçip geçmediğini kontrol eden" regex-tabanlı (LLM'siz) bir grader script'i yazmak — bu hem deterministik hem CI'da çalıştırılabilir olurdu, "Claude review" adımının gerektirdiği secret/flakiness sorunlarını taşımadan kısmi bir otomatik kontrol sağlardı. Bu, bu turun kapsamı dışında bırakıldı (yeni capability eklenmeyecek denildi).
