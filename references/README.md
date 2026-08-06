# references/ klasörü

Bu klasör boş gelir — TÜBİTAK'ın telif hakkı olan resmi belgelerini içermez, çünkü bu belgeler sık güncellenir ve dağıtım hakkı bu depoya ait değildir. Skill'lerin en güncel ve doğru bilgiyle çalışması için aşağıdaki belgeleri **siz** tubitak.gov.tr üzerinden indirip bu klasöre eklemelisiniz.

## Neden elle eklemeniz gerekiyor

- **Güncellik**: Uygulama esasları ve şablonlar TÜBİTAK tarafından önceden haber verilmeden güncellenebilir. Depoya gömülü statik bir kopya, siz fark etmeden eskimiş olabilir.
- **Kaynak güvenilirliği**: Skill'ler ("hakem-simulasyonu", "gider-kalemi-kontrolu", "cagri-tarama", "itiraz-hazirlik") sayısal değerleri (bütçe limiti, gider tavanı, süre, tarih) uydurmamak için gerçek kaynağa ihtiyaç duyar. Sizin indirdiğiniz resmi PDF, en güvenilir kaynaktır.
- **Telif/dağıtım**: TÜBİTAK belgelerini bir üçüncü taraf reposunda yeniden dağıtmak yerine, her kullanıcının kendi güncel kopyasını tutması istendi.

## Eklemeniz önerilen dosyalar

| Dosya | Nereden | Ne işe yarar |
|---|---|---|
| TEYDEB Uygulama Esasları (güncel) | tubitak.gov.tr → TEYDEB → Mevzuat | `hakem-simulasyonu` skill'inin "endüstriyel Ar-Ge" tanımını doğru uygulaması için |
| ARDEB (1001/3001) Uygulama Esasları | tubitak.gov.tr → ARDEB → Mevzuat | Akademik/girişim odaklı çağrılarda değerlendirme kriterleri için |
| AGY101 (Proje Öneri Formu) şablonu | İlgili çağrının başvuru sayfası | Taslakların TÜBİTAK'ın beklediği bölüm yapısına uyup uymadığını kontrol etmek için |
| AGY301 (Gelişme Raporu) şablonu | İlgili çağrının başvuru sayfası | Devam eden projelerde ara rapor değerlendirmesi için |
| Güncel çağrı metinleri (1501, 1505, 1507, 1509, 1511, 1707, 1001, 3001) | tubitak.gov.tr çağrı sayfaları | Son başvuru tarihi, bütçe üst limiti gibi çağrıya özgü koşullar için |
| Gider Formları Hazırlama Kılavuzu / Bütçe Hazırlama Rehberi | tubitak.gov.tr → TEYDEB → Mevzuat | `gider-kalemi-kontrolu` skill'inin gider kategorilerini ve güncel tavan/oranları doğru uygulaması için |
| TÜBİMER İtiraz Usul ve Esasları | tubitak.gov.tr → TÜBİMER | `itiraz-hazirlik` skill'inin itiraz süresi, kabul edilen gerekçe kategorileri ve idari ücret gibi bilgileri hafızadan uydurmadan uygulaması için |
| ÜYZ (üretken yapay zeka) Rehberi (Eylül 2025) | tubitak.gov.tr | Bu eklentinin tüm skill'lerinin uyduğu gizlilik ve beyan kurallarının kaynağı |

## Nasıl kullanılır

Dosyaları indirdiğiniz haliyle (PDF/DOCX) bu klasöre koymanız yeterli — skill'ler bir proje önerisini değerlendirirken veya bir çağrıyı tararken bu klasördeki güncel belgelere referans verebilir. Dosya adlarını değiştirmeniz gerekmiyor, sadece anlamlı isimler kullanmanız (örn. `teydeb-uygulama-esaslari-2025.pdf`) okunabilirliği artırır.

Bu araç TÜBİTAK ile ilişkili değildir. Resmi kaynak: [tubitak.gov.tr](https://www.tubitak.gov.tr)
