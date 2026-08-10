# Katkıda Bulunma

Bu, Türkiye'deki Ar-Ge teşvik süreçleri için bir Claude Code eklentisi (`arge-tesvik`). Katkılar — yeni bir skill fikri, mevcut bir skill'de iyileştirme, hata düzeltmesi — memnuniyetle karşılanır. Katkıda bulunurken [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)'deki kurallara uyulması beklenir.

## Yeni bir skill önermeden/eklemeden önce

Bu eklentideki her skill, gerçek bir kullanıcı sorununa (forum tartışması, TÜBİTAK dokümantasyonu, pratisyen deneyimi) dayanıyor — varsayımla değil. Yeni bir skill önerirken:

1. **Somut kaynak gösterin.** "Bu işe yarar sanırım" değil, "şu forumda/dokümanda şu sorun tekrar ediyor" diyebilmelisiniz.
2. **Hangi mevcut skill'le çakışıyor/tamamlıyor olduğunu belirtin.** Örneğin `gider-kalemi-kontrolu`, `hakem-simulasyonu`'nun bütçe kısmını derinleştiriyor, onun yerine geçmiyor — bu ayrımı netleştirin.
3. **Zorunlu kuralları uygulayın** (aşağıya bakın) — bu eklentideki her skill aynı disiplini paylaşıyor, yeni bir skill bunun dışında kalamaz.

## Zorunlu kurallar (her skill için geçerli)

- **Asla sayısal değer (bütçe limiti, süre, tarih) hafızadan yazma.** Güncel kaynaktan çekilmeli veya kullanıcıya doğrulatılmalı.
- **Asla sonuç/kabul garantisi verme.** "Bu kabul edilir" gibi ifadeler yasak — skill'ler değerlendirme/ön kontrol sağlar, karar mekanizması değildir.
- **ÜYZ gizlilik uyarısı, beyan zorunluluğu hatırlatması ve nihai sorumluluk notu** her skill çıktısının sonunda yer almalı (mevcut skill'lerdeki "Zorunlu uyarı bloğu" bölümlerine bakın, aynı formatı kullanın).
- **Rolünüzü aşmayın.** Örneğin `hakem-simulasyonu` içerik üretmez, sadece eleştirir — bir skill'in tanımlanan rolü neyse (eleştirmen, tarayıcı, kontrolcü) onun dışına çıkmamalı.

## Skill yazarken

`/mnt/skills/examples/skill-creator/SKILL.md` (Claude Code'un skill-creator skill'i) skill yazım kurallarının ve description tetikleme mantığının kaynağıdır — yeni bir skill eklerken veya mevcut birini düzenlerken önce onu okuyun. Özellikle:

- `description` alanı **tetikleyici** olmalı: skill'in ne yaptığını ve hangi kullanıcı ifadelerinde devreye girmesi gerektiğini somut örneklerle anlatın.
- SKILL.md'de imperative (emir kipi) yazın, "neden" açıklayın — sert "ASLA/HER ZAMAN" listesi yerine gerekçeyi anlatan bir üslup tercih edin (istisna: bu eklentideki güvenlik kritik kurallar — puan uydurmama, kabul garantisi vermeme gibi — kasıtlı olarak sert tutuldu, çünkü esneklik burada gerçek zarar riski taşıyor).

## Test etme

PR açmadan önce:

```bash
claude plugin validate . --strict
```

Yeni bir skill'in gerçekten doğru tetiklendiğini görmek için (bu repodaki tüm skill'ler bu şekilde test edildi — bkz. `evals/`):

```bash
claude --plugin-dir . -p "gerçekçi bir kullanıcı cümlesi" --output-format stream-json --verbose
```

çıktısında `Skill` tool-call'ının doğru skill'i çağırdığını doğrulayın. `evals/<skill-adı>.json` dosyasına birkaç gerçekçi test promptu eklemeniz önerilir (format için mevcut dosyalara bakın).

## GIF/görsel eklerken

Bu repodaki `assets/*.gif` dosyalarının hepsi **gerçekten çalıştırılmış komutların gerçek çıktısından** üretildi — uydurma terminal çıktısı yok. Yeni bir görsel eklerken aynı standardı koruyun: komutu gerçekten çalıştırın, gerçek çıktıyı kullanın. Emin değilseniz PR açıklamasında hangi komutu ne zaman çalıştırdığınızı belirtin.

## Kapsam dışı

Bu araç TÜBİTAK ile resmi bir ilişki içinde değil ve olamaz — TÜBİTAK'a ait logo, resmi form adları dışında marka unsuru, veya "TÜBİTAK onaylı" izlenimi verecek hiçbir içerik eklenmemeli.
