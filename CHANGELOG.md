# Changelog

Bu dosya `arge-tesvik` plugin'indeki önemli değişiklikleri listeler. Sürümler [Semantic Versioning](https://semver.org)'ı takip eder.

## 0.5.0

- Çok yıldızlı bir topluluk skill reposu (`alirezarezvani/claude-skills`, 24k+ yıldız) analiz edildi. Reponun çoğu (çoklu-araç dönüştürme, persona sistemi, kendi güvenlik denetleyicisi) bizim tek-domain, 5 skill'lik ölçeğimize uymadığı için kopyalanmadı; ölçeğe uygun iki gerçek eksik eklendi:
  - `CODE_OF_CONDUCT.md`
  - README'ye "Sık sorulan sorular" bölümü (resmi ilişki, veri gizliliği, içerik üretip üretmediği, güncelleme, çoklu proje kullanımı, hukuki/mali tavsiye olup olmadığı)

## 0.4.0

- Popüler Claude Code plugin/skill repoları (`anthropics/skills`, `anthropics/claude-code/plugins`) araştırılarak eksik olan standart repo bileşenleri eklendi:
  - `.github/workflows/validate.yml` — her push/PR'da `claude plugin validate --strict` ve JSON/SKILL.md bütünlük kontrolü çalıştıran CI
  - `CONTRIBUTING.md` — yeni skill eklerken uyulması gereken zorunlu kurallar ve test adımları
  - `evals/*.json` — her skill için skill-creator formatında gerçekçi test promptları
  - `.gitignore`
  - README'ye "Sorun giderme" ve "Katkıda bulunma" bölümleri, CI/lisans rozetleri

## 0.3.0

- `gider-kalemi-kontrolu` skill'i ve `/arge-tesvik:gider` komutu eklendi. TEYDEB bütçe kalemlerini 5 resmi gider kategorisine (personel, seyahat, hizmet alımı, alet/teçhizat/yazılım/yayın alımı, malzeme/sarf) oturtur ve hakem raporlarında sık görülen ret kalıplarına göre işaretler.

## 0.2.0

- `itiraz-hazirlik` skill'i ve `/arge-tesvik:itiraz` komutu eklendi. Ret kararı sonrası itiraz mı yoksa revizyon + yeniden başvuru mu uygun olduğuna karar vermeye yardımcı olur; itiraz yolu için TÜBİMER dilekçe taslağını sadece mevcut proje metnine/hakem raporuna dayanarak hazırlar.

## 0.1.0

- İlk sürüm: `hakem-simulasyonu`, `cagri-tarama`, `patent-on-arastirma` skill'leri; `/arge-tesvik:degerlendir` ve `/arge-tesvik:tara` komutları; `markapatent-mcp` HTTP MCP bağımlılığı.
