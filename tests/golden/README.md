# tests/golden/ — Golden Test Dataset Mimarisi

## Bu ne, `tests/*/eval-scenarios.md`'den farkı ne

`tests/<skill>/eval-scenarios.md` dosyaları tek seferlik, izole senaryolardır (bir skill'e tek bir girdi verip tek bir beklenen davranışı kontrol etme). **Golden dataset** ise bunun bir üst katmanı: **aynı (kurgusal) projeye ait birden fazla belgeyi**, birden fazla skill üzerinden, **makine tarafından kısmen kontrol edilebilir** beklenen sonuçlarla saklar — özellikle cross-skill regression (bkz. audit turlarındaki "AkışSense" test verisi) ve proje-tutarlilik-kontrolu gibi çoklu-belge skill'leri için tekrarlanabilir bir referans sağlamak içindir.

**Bu turda bu dizine gerçek veya sahte-gerçekçi bir proje eklenmedi** — sadece `_template/` altında boş bir şablon var. Gerçek bir golden proje eklerken (`project-001/` gibi) bu şablonu kopyalayıp doldurun.

## Neden manuel `tests/*/eval-scenarios.md`'den ayrı bir yapı gerekiyor

1. **Çoklu belge / çoklu skill:** Bir eval-scenario dosyası tek bir skill'i tek bir girdiyle test eder. Golden bir proje ise aynı belgeler kümesinin `hakem-simulasyonu`, `gider-kalemi-kontrolu`, `donem-raporu-kontrolu`, `proje-tutarlilik-kontrolu` üzerinden ayrı ayrı çalıştırılmasını ve sonuçların **birbiriyle de tutarlı olup olmadığının** kontrolünü gerektirir (cross-skill regression).
2. **Makine tarafından kısmen doğrulanabilirlik:** Serbest metin "Beklenen davranış" cümleleri yerine, golden projedeki `expected/*.yaml` dosyaları yapılandırılmıştır — bir değerlendirici (insan ya da ayrı bir LLM-grader oturumu) gerçek çıktıyı bu yapılandırılmış listeyle karşılaştırıp madde madde işaretleyebilir.
3. **Regresyon tekrarlanabilirliği:** Aynı golden proje, SKILL.md değişikliklerinden sonra tekrar tekrar çalıştırılıp "önceden yakalanan bulgular hâlâ yakalanıyor mu" diye kontrol edilebilir — audit turlarında elle yapılan bu işin (bkz. "AkışSense" test verisi) kalıcı/tekrar kullanılabilir hale gelmiş biçimi.

## Dizin yapısı

```
tests/golden/
├── README.md              (bu dosya)
├── SCHEMA.md               (her project-NNN'in iç yapısının tam şeması)
├── _template/               (boş şablon — kopyalanacak, gerçek veri YOK)
│   ├── manifest.yaml
│   ├── documents/
│   │   └── README.md        (buraya hangi belgelerin konacağını açıklar)
│   └── expected/
│       ├── findings.yaml
│       ├── conflicts.yaml
│       └── evidence-states.yaml
├── project-001/              (henüz yok — ileride eklenecek gerçek/gerçekçi ilk golden proje)
└── project-002/              (henüz yok)
```

## Nasıl kullanılır (ileride, bir proje eklendiğinde)

1. `_template/`'i `project-NNN/` olarak kopyalayın, `manifest.yaml`'ı doldurun (proje adı, hangi belgeler hangi skill'e girdi olacak).
2. `documents/` altına kaynak belgeleri koyun (kurgusal/anonimleştirilmiş — asla gerçek bir başvuru sahibinin verisi değil, bkz. gizlilik uyarısı).
3. `expected/findings.yaml`, `expected/conflicts.yaml`, `expected/evidence-states.yaml`'ı proje belgelerini siz (insan) inceleyerek doldurun — bunlar "doğru cevap anahtarı"dır, bir skill çalıştırılıp oradan kopyalanmamalıdır (aksi halde skill kendi hatasını da "doğru" olarak onaylar).
4. İlgili skill'leri `claude -p --plugin-dir .` ile `documents/` içeriğiyle çalıştırın, çıktıyı kaydedin.
5. Çıktıyı `expected/*.yaml` ile karşılaştırın (manuel veya bir LLM-grader promptuyla) — her beklenen bulgu/çelişki/evidence-state için: yakalandı mı, yanlış pozitif üretildi mi, kanıt etiketi doğru mu.

## Kapsam dışı (bilinçli olarak)

- Bu, gerçek zamanlı web/MCP çağrılarını (cagri-tarama, patent-on-arastirma) golden test kapsamına almaz — o ikisinin sonucu günden güne değişir, "golden" (sabit beklenen sonuç) kavramıyla uyumsuzdur. Onlar için `tests/cagri-tarama/eval-scenarios.md` ve `tests/patent-on-arastirma/eval-scenarios.md` zaten uygun çerçevedir.
- Otomatik bir grader script'i bu turda yazılmadı — `expected/*.yaml` şeması, ileride böyle bir script (ya da bir LLM-grader promptu) yazılabilecek şekilde yapılandırılmıştır, ama şu an değerlendirme manueldir.
