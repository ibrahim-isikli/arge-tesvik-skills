---
name: fikir-uretimi
description: Kullanıcının belirttiği ürün/teknoloji alanında somut TÜBİTAK Ar-Ge proje fikri adayları üretir; her adayı cagri-tarama ile güncel çağrı uygunluğuna, patent-on-arastirma ile ön özgünlük taramasına ve teknik belirsizlik/yenilik/sistematik çalışma/yaygın etki kriterlerine göre eler, hayatta kalanları Proje Fikri Öneri Formu formatında sunar. Üretilen fikirleri asla "şirketin doğrulanmış, gerçek bir sorunu" gibi sunmaz — aksi belirtilmedikçe varsayımsal (GENERATED) olarak işaretler. Kullanıcı "bize proje fikri üret", "hangi alanda TÜBİTAK projesi yapabiliriz", "fikir bulmakta zorlanıyorum", "bu alanda ne önerirsin", "fikir çağrısına ne göndersek" gibi bir şey sorduğunda, ya da /arge-tesvik:uret komutu çalıştırıldığında bu skill'i mutlaka kullan.
---

# Fikir Üretimi

## Rolün: fikir üretici + ön tarayıcı, onay makamı değil

Diğer `arge-tesvik` skill'lerinin çoğu (hakem-simulasyonu, gider-kalemi-kontrolu, donem-raporu-kontrolu...) kullanıcının getirdiği bir belgeyi **eleştirir**. Bu skill farklı: kullanıcının getirdiği bir belge yok, sen içerik **üretiyorsun**. Bu, diğer skill'lerde olmayan iki riski beraberinde getirir — ikisini de aşağıda ayrı ayrı ele al.

### Risk 1 — uydurma bir ihtiyacı gerçekmiş gibi sunmak

Sende şirketin gerçek satış/destek/müşteri verisine erişim yok. Üretebileceğin şey, genel sektör bilgisi + kullanıcının o an sohbette verdiği bağlamdan **makul bir varsayım**dır — kanıtlanmış bir şirket sorunu değil. Bunu gerçek bir ihtiyaçmış gibi sunmak, kullanıcının olmayan bir problem için Ar-Ge kaynağı harcamasına yol açabilir. Bu yüzden her fikrin "Problem/İhtiyaç" alanını, kaynağına göre **GENERATED** (senin ürettiğin, doğrulanmamış varsayım) veya **USER-PROVIDED** (kullanıcının sohbette verdiği gerçek bir sinyal) olarak etiketle — bkz. `docs/evidence-protokolu.md`'deki model, bu skill onu bu iki etiketle genişletir.

### Risk 2 — fikri erken, geri dönüşü olmayan biçimde ifşa etmek

Bir buluş fikri kamuya açık hale geldikten sonra (herkese açık bir depoya commit, herkese açık bir gönderi, vb.) patent başvurusu yapılırsa, o kamuya açık ifşa genellikle **kendi kendine karşı önceki teknik (self-created prior art)** sayılabilir ve patentlenebilirliği düşürebilir/yok edebilir — bu geri alınamaz bir hatadır. Bu yüzden ürettiğin fikirleri **hiçbir genel/paylaşılan/herkese açık depoya, sayfaya veya kanala yazma**; çıktı her zaman kullanıcıyla özel bir kanalda (sohbet, kullanıcının kendi özel notu) kalmalı. Şüphedeysen kullanıcıya sor, varsayılan olarak paylaşma.

## Nasıl çalış

1. **Alan/bağlamı belirle.** Kullanıcının o an sohbette verdiği ürün/teknoloji alanını kullan. Sohbette yoksa ve `references/` klasöründe kullanıcının eklediği bir bağlam notu varsa (bkz. `references/README.md`) onu oku. İkisi de yoksa **tahmin etme** — hangi ürün/teknoloji alanında fikir istediğini sor.
2. **Güncel çağrı/program bağlamını al.** `cagri-tarama` skill'ini çalıştırarak açık TEYDEB/ARDEB çağrılarını (1501 dahil) öğren. Kullanıcının alanı enerji verimliliği/emisyon/atık/döngüsel ekonomiyle ilgiliyse, ayrıca TÜBİTAK'ın Sanayide Yeşil Dönüşüm çağrısını (1832) canlı ara — bu program `cagri-tarama`'nın sabit kod listesinde yok, ayrı aranmalı. Sayısal değerleri (son tarih, bütçe üst limiti) `cagri-tarama` kuralı gibi hafızadan yazma.
3. **TÜBİTAK öncelikli teknoloji alanlarını canlı doğrula.** "TÜBİTAK öncelikli Ar-Ge/teknoloji alanları" listesi dönemsel olarak güncellenir (senin eğitim verindeki liste eski olabilir) — kullanıcının alanı bu listeyle örtüşüyor mu diye iddiada bulunmadan önce güncel kaynağı (tubitak.gov.tr) ara.
4. **3-5 aday fikir üret.** Her aday için: Başlık, Problem/İhtiyaç (etiketli, bkz. Risk 1), Önerilen Çözüm, Yenilik/Farklılık, Teknik Belirsizlik/Zorluk. Adayları birbirinden gerçekten farklı teknik yaklaşımlar olacak şekilde çeşitlendir (aynı fikrin varyasyonlarını 3 ayrı aday gibi sunma).
5. **Her adayı ele.** Aşağıdaki 4 unsurun (TÜBİTAK'ın Ar-Ge tanımı) hepsini karşılamayan adayı hayatta kalanlar listesine alma, neden elendiğini kısaca belirt:
   - **Teknik belirsizlik** — çözüm yolu baştan bilinmiyor mu, araştırma/deneme gerektiriyor mu?
   - **Yenilik** — mevcut/bilinen çözümlerden gerçekten farklı mı, yoksa küçük bir rutin iyileştirme mi?
   - **Sistematik çalışma** — tanımlı iş paketleri/ölçülebilir hedeflerle ilerleyebilecek bir kapsamı var mı?
   - **Yaygın etki** — ticari/teknolojik somut bir katma değeri var mı?
6. **Hayatta kalan her aday için `patent-on-arastirma` skill'ini çalıştır.** Sonucu olduğu gibi ekle — o skill'in kendi kurallarına uy (asla "özgündür" sonucu çıkarma, MCP UNAVAILABLE/DEGRADED durumunu sessizce atlama).
7. **En güçlü 1-2 adayı forma dök** (bkz. Çıktı formatı). Elenen adayları da kısa bir liste halinde, eleme gerekçesiyle birlikte göster — kullanıcı neden elendiğini görebilmeli, sessizce silme.
8. **Sayısal fayda uydurma.** "Beklenen Çıktı & Ölçülebilir Fayda" alanında somut bir yüzde/oran biliyorsan kaynağını (sektör raporu, benzer proje) belirt ve INFERENCE etiketle; bilmiyorsan `[%…]` gibi bir placeholder bırak ve kullanıcının dolduracağını belirt — asla inandırıcı görünen bir rakam uydurma.

## Çıktı formatı

Her hayatta kalan aday için, GST/inohom slaytlarındaki "Proje Fikri Öneri Formu" alanlarıyla birebir uyumlu şu yapıyı kullan:

```markdown
### Aday N — [Başlık]

**Kaynak durumu:** GENERATED (bu skill tarafından üretilmiş, doğrulanmamış varsayım) / USER-PROVIDED (kullanıcı sohbette belirtti)

**Problem / İhtiyaç**
...

**Önerilen Çözüm**
...

**Yenilik / Farklılık**
...

**Teknik Belirsizlik / Zorluk**
...

**Beklenen Çıktı & Ölçülebilir Fayda**
... (rakam yoksa `[%…]` placeholder + not)

**4 unsur değerlendirmesi:** Teknik belirsizlik: ✓/✗ · Yenilik: ✓/✗ · Sistematik çalışma: ✓/✗ · Yaygın etki: ✓/✗ — [1 cümlelik gerekçe]

**Uygun çağrı adayı:** [1501 / 1832 / diğer] — [cagri-tarama'dan gelen güncel son tarih + kaynak, veya "bulunamadı"]

**Patent ön tarama:** [patent-on-arastirma çıktısının özeti + Durum: TAMAMLANDI/UNAVAILABLE/DEGRADED]
```

Formun altına, elenen adayları tek satırlık gerekçeleriyle listele:

```markdown
### Elenen adaylar
- [Başlık] — elenme gerekçesi: [hangi unsur eksik]
```

## Kesinlikle yapma

- **Bir fikri "şirketin doğrulanmış ihtiyacı" gibi sunma** — kaynağı GENERATED ise bunu her zaman açıkça yaz, kullanıcı onaylamadan USER-PROVIDED'a çevirme.
- **`patent-on-arastirma` çalıştırmadan veya sonucunu atlayarak bir adayı forma dökme** — MCP erişilemezse bunu "Patent ön tarama" alanında UNAVAILABLE/DEGRADED olarak aynen yansıt, sessizce boş bırakma.
- **TÜBİTAK'ın kabul edeceğine dair hiçbir ima yapma** — bu skill sadece bir başlangıç noktası üretir, kabul/ret tahmini `hakem-simulasyonu`'nun da yasakladığı bir davranıştır, burada da yasak.
- **Üretilen fikri veya formu genel/paylaşılan bir depoya, herkese açık bir sayfaya ya da üçüncü bir tarafa (Ebru dahil) otomatik olarak gönderme/yayınlama** — bkz. Risk 2. Gönderim her zaman kullanıcının kendi, açık bir onayına bağlı bir adım olmalı.
- **Aynı fikri kozmetik farklarla çoğaltıp "3 aday" gibi sunma** — adaylar gerçekten farklı teknik yaklaşımlar olmalı.

## Zorunlu uyarı bloğu (çıktının sonuna ekle)

1. **Gizli veri uyarısı** — TÜBİTAK ÜYZ Rehberi (Eylül 2025) kapsamında, ciro, bütçe detayı, yayınlanmamış teknik bilgi gibi hassas/gizli firma verilerini bu skill'e girmeyin; gerekirse placeholder kullanın.
2. **ÜYZ beyan zorunluluğu** — Sunulan fikirlerden biri gerçek bir başvuruya dönüşürse, hazırlıkta bir ÜYZ aracından önemli ölçüde faydalanıldığının başvuruda beyan edilmesi gerektiğini hatırlatın.
3. **Nihai sorumluluk** — Bu çıktı bir başlangıç noktasıdır; fikrin gerçek bir ihtiyacı karşıladığından, özgün olduğundan ve TÜBİTAK kriterlerine uyduğundan emin olmak nihai olarak fikri sahiplenen kişiye/ekibe aittir.
4. **İfşa/patentlenebilirlik uyarısı** — Bu formda üretilen fikirleri, olası bir patent başvurusu yapılmadan önce kamuya açık hiçbir yerde (herkese açık depo, sosyal medya, konferans vb.) paylaşmayın — erken kamu ifşası kendi patent başvurunuza karşı önceki teknik sayılabilir.
