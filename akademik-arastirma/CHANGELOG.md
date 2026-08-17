# Changelog

Bu dosya `akademik-arastirma` plugin'indeki önemli değişiklikleri listeler. Sürümler [Semantic Versioning](https://semver.org)'ı takip eder.

**Sürümleme kuralı:**
- **MAJOR** — geriye dönük uyumsuz bir değişiklik (skill/komut kaldırma, isim değişikliği, davranış tersine çevrilmesi).
- **MINOR** — yeni bir skill/komut eklenmesi, ya da mevcut bir skill'in davranışını gözle görülür biçimde genişleten bir değişiklik.
- **PATCH** — prompt netleştirmesi, hata düzeltmesi, dokümantasyon/metadata güncellemesi; skill'in kapsamını değiştirmeyen değişiklikler.

## 0.1.0

- İlk sürüm. [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) reposundaki akademik araştırma pipeline'ından (deep-research / academic-paper / academic-paper-reviewer / integrity gates) ilham alınarak, Türkçe akademik araştırma bağlamına (DergiPark, TR Dizin, YÖK Ulusal Tez Merkezi, APA 7 Türkçe kuralları, YÖK Bilimsel Araştırma ve Yayın Etiği Yönergesi) uyarlanmış, odaklı ve bakımı kolay bir eklenti olarak sıfırdan yazıldı — kaynak repodaki 968 dosyalık kapsamlı yapı birebir çevrilmedi, temel fikirler (Sokratik planlama, disiplinli hakem eleştirisi, atıf/kaynak bütünlük kontrolü, "AI kopilot, pilot değil" ilkesi) 4 skill'e damıtıldı.
- `literatur-taramasi` skill'i ve `/akademik-arastirma:tara` komutu eklendi: araştırma sorusu netleştirme, canlı literatür taraması (DergiPark/TR Dizin/Google Scholar/YÖK Tez Merkezi), kaynak değerlendirme.
- `makale-yazim-rehberligi` skill'i ve `/akademik-arastirma:planla` komutu eklendi: Sokratik yapı planlama, iskelet/başlık ağacı üretme, taslak akış/tutarlılık eleştirisi — içerik yazmaz.
- `akademik-hakem-simulasyonu` skill'i ve `/akademik-arastirma:hakem` komutu eklendi: dergi hakemi/tez jürisi gözüyle dört boyutlu eleştiri (araştırma sorusu/katkı, yöntem, bulgu-tartışma tutarlılığı, literatüre yerleşim).
- `atif-butunluk-kontrolu` skill'i ve `/akademik-arastirma:atif` komutu eklendi: metin-içi atıf/kaynakça eşleşmesi, format kontrolü, örneklem bazlı canlı kaynak doğrulama, aşırı iddialı dil taraması, AI beyanı hatırlatması.
- `docs/evidence-protokolu.md` eklendi: FACT/INFERENCE/USER-PROVIDED/UNKNOWN/OUTDATED/CONFLICTING sınıflandırma modeli, kaynak güven hiyerarşisi, zorunlu uyarı bloğunun kanonik metni ve "içerik yazmama" tasarım ilkesi.
