# Changelog

Bu dosya `arge-tesvik` plugin'indeki önemli değişiklikleri listeler. Sürümler [Semantic Versioning](https://semver.org)'ı takip eder.

**Sürümleme kuralı:**
- **MAJOR** — geriye dönük uyumsuz bir değişiklik (skill/komut kaldırma, isim değişikliği, davranış tersine çevrilmesi).
- **MINOR** — yeni bir skill/komut eklenmesi, ya da mevcut bir skill'in davranışını gözle görülür biçimde genişleten bir değişiklik (yeni kontrol boyutu, yeni çıktı alanı).
- **PATCH** — prompt netleştirmesi, hata düzeltmesi, dokümantasyon/metadata güncellemesi; skill'in kapsamını değiştirmeyen değişiklikler.

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
