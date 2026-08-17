# akademik-arastirma

Türkçe akademik araştırma sürecini destekleyen bir Claude Code eklentisi (`akademik-arastirma`): literatür taraması, makale/tez yapısı planlama, hakem simülasyonu ve atıf/bütünlük kontrolü.

Bu eklenti [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) projesinden ilham alınarak, Türkçe akademik bağlama (DergiPark, TR Dizin, YÖK Ulusal Tez Merkezi, APA 7 Türkçe kuralları, YÖK Bilimsel Araştırma ve Yayın Etiği Yönergesi) uyarlanmış, sıfırdan yazılmış ve kasıtlı olarak küçük tutulmuş bir yapıdır — kaynak projenin 968 dosyalık kapsamlı yapısının birebir çevirisi değildir.

```
Based on ideas from Academic Research Skills by Cheng-I Wu
https://github.com/Imbad0202/academic-research-skills
```

## Temel ilke: içerik yazmaz, planlar/eleştirir/kontrol eder

Dört skill'in ortak tasarım kararı: hiçbiri kullanıcı adına akademik metin (paragraf, cümle, bulgu yorumu) üretmez. Sebep hem akademik yazarlık sorumluluğunun araştırmacıda kalmasını sağlamak hem de YÖK Bilimsel Araştırma ve Yayın Etiği Yönergesi kapsamındaki özgünlük/yazarlık beklentileriyle uyumlu kalmaktır — kaynak projenin "AI kopilotunuzdur, pilotunuz değil" ilkesiyle aynı çizgide.

## Skill'ler

| Skill | Ne yapar |
|---|---|
| `literatur-taramasi` | Bir araştırma sorusu için literatür tarama stratejisi kurar, DergiPark/TR Dizin/Google Scholar/YÖK Ulusal Tez Merkezi'nde canlı arama yapar, bulunan kaynakları alaka/tür/güncellik açısından raporlar. Var olmayan kaynak uydurmaz; bulamadığını "bulunamadı" der. |
| `makale-yazim-rehberligi` | Sokratik sorularla makale/tez yapısı planlar (IMRaD, tez bölümleri, derleme, vaka çalışması, politika notu), iskelet/başlık ağacı üretir, mevcut taslağın akış/argüman tutarlılığını eleştirir. Paragraf veya cümle içeriği yazmaz. |
| `akademik-hakem-simulasyonu` | Bir makale/tez taslağını dergi hakemi/jüri gözüyle eleştirir — araştırma sorusu/katkı, yöntem sağlamlığı, bulgu-tartışma tutarlılığı, literatüre yerleşim boyutlarında. Puan uydurmaz, kabul/ret garantisi vermez. |
| `atif-butunluk-kontrolu` | Metin-içi atıf ↔ kaynakça eşleşmesini, format tutarlılığını (APA 7/Chicago/IEEE/Vancouver/MLA) kontrol eder; şüpheli kaynakları örnekleyerek canlı arama ile doğrulamaya çalışır (DOĞRULANDI/BULUNAMADI/UYUŞMAZLIK); aşırı iddialı dili ve AI beyanı eksikliğini işaretler. İntihal taraması yapmaz. |

Slash komutları ilgili skill'i doğrudan tetikler:

- `/akademik-arastirma:tara` → `literatur-taramasi`
- `/akademik-arastirma:planla` → `makale-yazim-rehberligi`
- `/akademik-arastirma:hakem` → `akademik-hakem-simulasyonu`
- `/akademik-arastirma:atif` → `atif-butunluk-kontrolu`

Claude Code'da plugin komutları `<plugin-adı>:<komut-adı>` şeklinde adlandırılır, bu yüzden tam komut isimleri yukarıdaki gibidir. Başka bir eklentiyle çakışmadığı sürece kısaca `/tara` ya da `/hakem` yazmak da çalışır.

## Kurulum

Bu plugin, `arge-tesvik-skills` reposundaki marketplace'in bir parçasıdır — ek bir marketplace deposuna ihtiyaç yoktur.

```
claude plugin marketplace add ibrahim-isikli/arge-tesvik-skills
claude plugin install akademik-arastirma@arge-tesvik-skills
```

Yerelde geliştirirken/denerken (doğrudan bu klasörden):

```
claude --plugin-dir /path/to/arge-tesvik-skills/akademik-arastirma
```

## Evidence protokolü ve ortak kurallar

`docs/evidence-protokolu.md`, skill'lerin kaynak/atıf/güncellik iddialarında kullandığı ortak sınıflandırma modelini (FACT/DOĞRULANDI, INFERENCE, USER-PROVIDED, UNKNOWN/BULUNAMADI, OUTDATED, CONFLICTING/UYUŞMAZLIK), kaynak güven hiyerarşisini ve her skill'in sonunda tekrarlanan zorunlu uyarı bloğunun kanonik metnini tek yerde toplar.

## Sınırlamalar

- Skill'ler birer LLM talimat kümesidir, deterministik doğrulayıcı değildir — çıktıları her zaman bir başlangıç noktasıdır, resmi hakem/jüri kararı, intihal taraması veya kesin kaynak doğrulaması yerine geçmez.
- `literatur-taramasi` ve `atif-butunluk-kontrolu` canlı web erişimine bağımlıdır; abonelik gerektiren veritabanlarına (Scopus, Web of Science) doğrudan erişim yoktur — kullanıcının bu kaynaklardan paylaştığı veri değerlendirilebilir ama skill kendi adına oraları taradığını iddia etmez.
- `atif-butunluk-kontrolu`'nun "BULUNAMADI" etiketi "uydurma kaynak" ile eş anlamlı değildir; her zaman elle teyit gerektirir.
- Hiçbir skill akademik metin (paragraf/cümle) üretmez; bu kasıtlı bir tasarım sınırıdır, eksiklik değildir.

## Sorun giderme

- **Slash komutu görünmüyor**: Eklentinin yüklendiğini kontrol edin (`claude plugin list`) ve gerekirse `/reload-plugins` çalıştırın.
- **Skill tetiklenmiyor ama slash komutu çalışıyor**: Skill'in `description` alanı tetikleme kuralıdır; isteğinizde skill'in kapsadığı anahtar kelimelerden biri geçmiyorsa ilgili slash komutunu doğrudan kullanmanız daha güvenilirdir.

## Zorunlu kurallar (tüm skill'lerde geçerli)

- **Gizlilik**: Yayınlanmamış/hassas araştırma verisi (IRB onayı bekleyen katılımcı bilgisi vb.) bu tür araçlara girilirken kurumun veri politikası göz önünde bulundurulmalıdır.
- **Yapay zeka kullanım beyanı**: Hazırlıkta bir üretken yapay zeka aracından önemli ölçüde faydalanıldıysa, hedef dergi/kurumun politikasına göre bunun beyan edilmesi gerekebileceği her skill çıktısının sonunda hatırlatılır.
- **Nihai sorumluluk**: İçeriğin doğruluğu, özgünlüğü ve akademik bütünlüğünden nihai olarak araştırmacı/yazar sorumludur; hiçbir skill bu sorumluluğu üstlenmez.

## Sürüm geçmişi

Değişiklikler için [CHANGELOG.md](./CHANGELOG.md)'ye bakın.
