# Changelog

Bu dosya `arge-tesvik` plugin'indeki önemli değişiklikleri listeler. Sürümler [Semantic Versioning](https://semver.org)'ı takip eder.

## 0.3.0

- `gider-kalemi-kontrolu` skill'i ve `/arge-tesvik:gider` komutu eklendi. TEYDEB bütçe kalemlerini 5 resmi gider kategorisine (personel, seyahat, hizmet alımı, alet/teçhizat/yazılım/yayın alımı, malzeme/sarf) oturtur ve hakem raporlarında sık görülen ret kalıplarına göre işaretler.

## 0.2.0

- `itiraz-hazirlik` skill'i ve `/arge-tesvik:itiraz` komutu eklendi. Ret kararı sonrası itiraz mı yoksa revizyon + yeniden başvuru mu uygun olduğuna karar vermeye yardımcı olur; itiraz yolu için TÜBİMER dilekçe taslağını sadece mevcut proje metnine/hakem raporuna dayanarak hazırlar.

## 0.1.0

- İlk sürüm: `hakem-simulasyonu`, `cagri-tarama`, `patent-on-arastirma` skill'leri; `/arge-tesvik:degerlendir` ve `/arge-tesvik:tara` komutları; `markapatent-mcp` HTTP MCP bağımlılığı.
