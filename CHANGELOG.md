# Changelog

Bu dosya `arge-tesvik` plugin'indeki önemli değişiklikleri listeler. Sürümler [Semantic Versioning](https://semver.org)'ı takip eder.

**Sürümleme kuralı:**
- **MAJOR** — geriye dönük uyumsuz bir değişiklik (skill/komut kaldırma, isim değişikliği, davranış tersine çevrilmesi).
- **MINOR** — yeni bir skill/komut eklenmesi, ya da mevcut bir skill'in davranışını gözle görülür biçimde genişleten bir değişiklik (yeni kontrol boyutu, yeni çıktı alanı).
- **PATCH** — prompt netleştirmesi, hata düzeltmesi, dokümantasyon/metadata güncellemesi; skill'in kapsamını değiştirmeyen değişiklikler.

## 1.0.0

- **BREAKING (davranış tersine çevrildi):** `patent-on-arastirma`'nın varsayılan/birincil yöntemi artık `markapatent-mcp` (TÜRKPATENT) değil, ücretsiz genel patent veritabanı taraması (`WebSearch`/`WebFetch` ile Google Patents/Espacenet) — hiçbir hesap/API key gerektirmez. `markapatent-mcp` artık yalnızca kullanıcı açıkça TÜRKPATENT'e özel doğrulama veya marka/tasarım araması istediğinde devreye giriyor (marka/tasarım zaten sadece bu yolla taranabiliyordu). Gerekçe: `markapatent-mcp` üçüncü taraf bir servise (Capsolver, ücretli, minimum $10 yükleme) bağımlı ve bu turda gerçek kullanımda bakiyesi tükenmiş durumda bulundu — varsayılan akışı buna bağımlı tutmak, plugin'in temel kullanım senaryosunu (patent ön taraması) parayla/üçüncü tarafla şartlandırıyordu. `Kaynak` kolonu artık `Genel patent veritabanı (Google Patents/Espacenet)` / `TÜRKPATENT (markapatent-mcp)` değerlerini ayırt ediyor.
- `docs/evidence-protokolu.md` kaynak hiyerarşisiyle uyumlu olacak şekilde README, gereksinimler tablosu ve "markapatent-mcp bağlantısı" bölümü (artık "opsiyonel" olarak) güncellendi; kendi Capsolver key'inizle self-host etme seçeneği belgelendi.
- `tests/patent-on-arastirma/eval-scenarios.md` yeni varsayılan davranışı (markapatent-mcp'nin opt-in olması) yansıtacak şekilde güncellendi.

## 0.8.0

- `patent-on-arastirma`: markapatent-mcp (TÜRKPATENT) UNAVAILABLE/DEGRADED olduğunda artık sessizce durmuyor — `WebSearch`/`WebFetch` bağlıysa Google Patents/Espacenet üzerinde ikincil bir tarama deniyor, bulguları `Kaynak: TÜRKPATENT` / `Kaynak: İkincil` diye ayrıştırılmış yeni bir kolonla raporluyor. İkincil kaynağın TÜRKPATENT sonucuymuş gibi sunulmasını yasaklayan yeni bir "Kesinlikle yapma" maddesi eklendi. Bu değişiklik, bu turda gerçek bir runtime testinde markapatent-mcp'nin arkasındaki captcha-çözücü servisin (Capsolver) bakiyesi tükendiğinde tetiklendi — Google Patents/Justia gibi hedef sitelerin patent detay sayfalarının otomatik erişimi (403/503) sıkça engellediği de aynı testte doğrulandı; bu durumda ilgili alan (rüçhan tarihi/IPC-CPC/hukuki durum) tahmin edilmeden "bulunamadı" olarak işaretleniyor.
- `tests/patent-on-arastirma/eval-scenarios.md`: senaryo 5 (MCP hatası) bu yeni ikincil-tarama davranışını ve gerçek runtime'da karşılaşılan 403/503 erişim engelini yansıtacak şekilde güncellendi.

## 0.7.0

- `fikir-uretimi` skill'i ve `/arge-tesvik:uret` komutu eklendi. Belirtilen ürün/teknoloji alanında 3-5 aday TÜBİTAK Ar-Ge proje fikri üretir, her adayı 4 unsura (teknik belirsizlik/yenilik/sistematik çalışma/yaygın etki) göre eler; hayatta kalanlar için `cagri-tarama`'yı güncel çağrı uygunluğu, `patent-on-arastirma`'yı ön özgünlük taraması için çalıştırır ve sonucu Proje Fikri Öneri Formu formatında sunar. Bu, eklentideki diğer skill'lerden farklı olarak kullanıcının getirdiği bir belgeyi eleştirmek yerine içerik üretiyor — bu yüzden iki ek kurala tabi: (a) her fikrin "Problem/İhtiyaç" alanı GENERATED (doğrulanmamış varsayım) veya USER-PROVIDED (kullanıcının verdiği gerçek sinyal) olarak etiketlenir, gerçek bir şirket ihtiyacıymış gibi sunulmaz; (b) üretilen fikir içeriği hiçbir genel/paylaşılan depoya veya üçüncü tarafa otomatik gönderilmez/yayınlanmaz — erken kamu ifşası, olası bir patent başvurusuna karşı kendi kendine önceki teknik (self-created prior art) sayılabileceği için.
- `docs/evidence-protokolu.md`'deki FACT/INFERENCE/USER-PROVIDED/UNKNOWN/OUTDATED/CONFLICTING modeli, `fikir-uretimi` özelinde GENERATED etiketiyle genişletildiği not edildi (skill'e özgü, kanonik modele eklenmedi — bkz. dosyadaki "kasıtlı olarak ortak yapılmayan" ilkesi).

## 0.6.2

- `.gitignore`, `CODE_OF_CONDUCT.md` ve `CONTRIBUTING.md` eklendi. Bu dosyalar daha önce, hiç merge edilmemiş ve kapatılmış bir PR'da (`claude/arge-tesvik-skills-setup-5shcq1`) taslak olarak vardı; içerikleri gözden geçirilip depo o zamandan bu yana değişmiş güncel yapıya (`tests/` eval çerçevesi, `scripts/validate.py`, CI'sız test akışı) uyacak şekilde güncellenerek eklendi. `evals/*.json` (artık `tests/<skill>/eval-scenarios.md` ile karşılanıyor) ve o dalın eski CI workflow dosyası, güncel yapıda gereksiz oldukları için taşınmadı.

## 0.6.1

- `.github/workflows/validate.yml` (CI) kaldırıldı. Depo sahibinin GitHub hesabı, reponun içeriğiyle ilgisi olmayan bir billing kilidi nedeniyle Actions job'larını hiç başlatamıyordu ("account is locked due to a billing issue") ve GitHub Actions'a bağımlı olunmaması tercih edildi. `scripts/validate.py` hâlâ var ve çalışıyor, sadece artık otomatik değil — commit öncesi elle çalıştırılmalı (`python3 scripts/validate.py`). README ve `docs/automation-readiness.md` bu değişikliği yansıtacak şekilde güncellendi.

## 0.6.0

- `gider-kalemi-kontrolu`: çıktı sözleşmesi yeniden tasarlandı — zorunlu 5 kolonlu ana tablo (Gider | Kategori Uygunluğu | Gerekçelendirme Yeterliliği | Kanıt Durumu | Risk) artık tablo dışı serbest açıklamadan ayrıştırıldı; şemayı mekanik olarak kontrol eden `scripts/check_table.py` eklendi. Gerçek runtime testlerinde (3 farklı gider seti) içerik kalitesi her koşuda doğruydu, ama kolon başlıklarının birebir korunması garanti edilemedi — bu bilinen bir sınırlama olarak belgelendi (bkz. audit raporu).
- `patent-on-arastirma`: MCP durumunu artık açık `UNAVAILABLE`/`DEGRADED` etiketleriyle raporluyor; var olmayan alternatif patent arama araçlarından bahsetmeyi yasaklayan kural eklendi (gerçek runtime testinde doğrulanan bir P3 bulgusunun düzeltilmesi).
- `docs/evidence-protokolu.md`: 5 bulgu-üreten skill arasında Status/Finding/Evidence/Risk/Recommendation/Source kavramlarının hangilerinin gerçekten ortak olduğuna dair bir analiz eklendi (Finding/Evidence ortak; Risk/Status kasıtlı olarak evrensel yapılmadı çünkü bazı skill'ler kurumsal sonuç tahmininden kaçınıyor).
- `.github/workflows/validate.yml` eklendi: push/pull_request'te `scripts/validate.py` çalıştıran minimal CI.
- `tests/golden/` eklendi: çoklu belge/çoklu skill/cross-skill regression için yapılandırılmış bir golden-dataset çerçevesi (`_template/` + `SCHEMA.md`). Henüz gerçek bir proje verisi içermiyor.
- 13 runtime regresyon senaryosu (prompt injection, MCP failure, missing/outdated/conflicting bilgi) bu turun değişikliklerinden sonra yeniden doğrulandı; regresyon bulunmadı.

## 0.5.0

- `proje-tutarlilik-kontrolu` skill'i ve `/arge-tesvik:tutarlilik` komutu eklendi. Aynı projeye ait birden fazla belge arasında süre/bütçe/personel/hedef/TRL/ticarileşme tarihi gibi alanlarda çelişki arar; hangi belgenin doğru olduğuna karar vermez.
- `docs/evidence-protokolu.md` eklendi: FACT/INFERENCE/USER-PROVIDED/UNKNOWN/OUTDATED/CONFLICTING sınıflandırma modeli, kaynak güven hiyerarşisi ve zorunlu uyarı bloğunun kanonik metni. `cagri-tarama`, `gider-kalemi-kontrolu`, `donem-raporu-kontrolu` ve `itiraz-hazirlik` bu modele kısa pointer'larla bağlandı (mevcut inline uyarı blokları korunarak).
- `patent-on-arastirma`: MCP bağlantı hatası/timeout, boş/kısmi sonuç, çok fazla sonuç ve patent family (rüçhan tarihi bazlı birleştirme) için açık talimatlar eklendi; MCP çıktısının veri olarak ele alınıp talimat olarak yorumlanmayacağı netleştirildi.
- `cagri-tarama`: taranan web sayfalarındaki gömülü talimatların (prompt injection) asla komut olarak uygulanmayacağı kuralı eklendi.
- `gider-kalemi-kontrolu`: "kategori uygunluğu" ile "gerekçelendirme yeterliliği" ayrı değerlendirme boyutları haline getirildi (önceden tek bir "bulgu" sütununda karışıyordu).
- `commands/rapor.md`: sadece rapor dosyası verildiğinde onaylı proje planını isteme adımının atlanabildiği bir tutarsızlık düzeltildi.
- `scripts/validate.py` eklendi: plugin/marketplace JSON geçerliliği, skill frontmatter kısıtları, command→skill eşlemesi ve sürüm/CHANGELOG tutarlılığı için bağımlılıksız statik doğrulayıcı.
- `tests/` eklendi: her skill için normal/eksik bilgi/hallucination/çelişki/güncel-olmayan-bilgi/kötü niyetli girdi/belirsiz istek senaryolarını kapsayan LLM-graded manuel eval çerçevesi.
- README'ye Evidence Protokolü, Doğrulama ve Testler, Sınırlamalar ve Sorun Giderme bölümleri eklendi; `plugin.json`'a `repository` alanı eklendi.

## 0.4.0

- `donem-raporu-kontrolu` skill'i ve `/arge-tesvik:rapor` komutu eklendi. Kabul edilmiş bir TEYDEB projesinin dönemsel Gelişme Raporu'nu (AGY301) veya proje sonu Sonuç Raporu'nu, onaylı proje planıyla karşılaştırarak izleyici/hakem gözüyle eleştirir; somut kanıt eksikliğini, gerekçesiz takvim/bütçe sapmalarını ve tutarsız bir sonraki dönem planını işaretler.

## 0.3.0

- `gider-kalemi-kontrolu` skill'i ve `/arge-tesvik:gider` komutu eklendi. TEYDEB bütçe kalemlerini 5 resmi gider kategorisine (personel, seyahat, hizmet alımı, alet/teçhizat/yazılım/yayın alımı, malzeme/sarf) oturtur ve hakem raporlarında sık görülen ret kalıplarına göre işaretler.

## 0.2.0

- `itiraz-hazirlik` skill'i ve `/arge-tesvik:itiraz` komutu eklendi. Ret kararı sonrası itiraz mı yoksa revizyon + yeniden başvuru mu uygun olduğuna karar vermeye yardımcı olur; itiraz yolu için TÜBİMER dilekçe taslağını sadece mevcut proje metnine/hakem raporuna dayanarak hazırlar.

## 0.1.0

- İlk sürüm: `hakem-simulasyonu`, `cagri-tarama`, `patent-on-arastirma` skill'leri; `/arge-tesvik:degerlendir` ve `/arge-tesvik:tara` komutları; `markapatent-mcp` HTTP MCP bağımlılığı.
