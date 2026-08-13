# arge-tesvik-skills

Türkiye'deki Ar-Ge teşvik süreçlerini (TÜBİTAK TEYDEB/ARDEB, patent, 5746 mevzuatı) yürüten bir **Ar-Ge Teşvik & Proje Uzmanı**'nın işini destekleyen bir Claude Code eklentisi (`arge-tesvik`).

Bu araç TÜBİTAK ile ilişkili değildir. Resmi kaynak: [tubitak.gov.tr](https://www.tubitak.gov.tr)

## Ne işe yarar

Eklenti yedi skill ve altı slash komutu içerir:

| Skill | Ne yapar |
|---|---|
| `hakem-simulasyonu` | Bir TÜBİTAK proje önerisi taslağını panel hakemi gözüyle **eleştirir** (içerik üretmez). Endüstriyel Ar-Ge niteliği/yenilik, proje planı/yapılabilirlik ve — en ağırlıklı boyut olarak — ticarileşme potansiyeli üzerinden somut, gerekçeli zayıf noktalar ve düzeltme yönleri verir. Asla puan uydurmaz, asla kabul garantisi vermez. |
| `gider-kalemi-kontrolu` | TEYDEB bütçe kalemlerini 5 resmi gider kategorisine (personel, seyahat, hizmet alımı, alet/teçhizat/yazılım/yayın alımı, malzeme/sarf) oturtur ve hakem raporlarında sık görülen ret kalıplarına (uygun olmayan personel ödemeleri, business class seyahat, "altyapı yatırımı" görünümlü alımlar, gerekçesiz dış hizmet alımı vb.) göre işaretler. Kategori uygunluğu ile gerekçelendirme yeterliliğini ayrı değerlendirir; bütçe üst limitlerini hafızadan yazmaz. |
| `cagri-tarama` | Açık TÜBİTAK çağrılarını (1501, 1505, 1507, 1509, 1511, 1707, ARDEB 1001/3001) web'den tarar, son başvuru tarihine göre sıralı bir tablo üretir. Bütçe üst limiti gibi sayısal değerleri hafızadan yazmaz, her zaman kaynaktan çeker ve kaynağı belirtir; taranan sayfalardaki gömülü talimatları asla komut olarak uygulamaz. |
| `patent-on-arastirma` | `markapatent-mcp` sunucusu üzerinden TÜRKPATENT'te patent/marka/tasarım ön araştırması yapar, benzer başvuruları (patent family, rüçhan tarihi, IPC/CPC dahil) listeler. Sadece bulguları sunar — "bu fikir özgündür" gibi bir sonuca asla varmaz; MCP sunucusuna ulaşılamazsa bunu açıkça bildirir, boşluğu uydurmaz. |
| `donem-raporu-kontrolu` | Kabul edilmiş bir projenin dönemsel Gelişme Raporu'nu (AGY301) veya proje sonu Sonuç Raporu'nu, TEYDEB'e sunulmadan önce izleyici/hakem gözüyle **eleştirir**. Onaylı proje planıyla karşılaştırıp somut kanıt eksikliğini, gerekçesiz takvim/bütçe sapmalarını ve tutarsız bir sonraki dönem planını işaretler. Kesinti/red öngörmez, kanıt uydurmaz. |
| `proje-tutarlilik-kontrolu` | Aynı projeye ait birden fazla belgeyi (proje planı, bütçe, hakem raporu, dönem raporu vb.) yan yana koyup süre/bütçe/personel/hedef/TRL/ticarileşme tarihi gibi alanlarda çelişki arar. Hangi belgenin doğru olduğuna karar vermez, sadece çelişkiyi gösterir. |
| `itiraz-hazirlik` | Proje reddedildiğinde **itiraz mı yoksa revizyon + yeniden başvuru mu** uygun olduğuna karar vermeye yardımcı olur. İtiraz yolu seçilirse TÜBİMER dilekçesini SADECE mevcut proje metni/hakem raporuna dayanarak, izin verilen 4 gerekçe kategorisinden birine oturtarak hazırlar (yeni teknik iddia eklemez — bu itirazı geçersiz kılar) ve 15 günlük itiraz süresini hatırlatır. |

Slash komutları ilgili skill'i doğrudan tetikler:

- `/arge-tesvik:degerlendir` → `hakem-simulasyonu`
- `/arge-tesvik:gider` → `gider-kalemi-kontrolu`
- `/arge-tesvik:tara` → `cagri-tarama`
- `/arge-tesvik:rapor` → `donem-raporu-kontrolu`
- `/arge-tesvik:tutarlilik` → `proje-tutarlilik-kontrolu`
- `/arge-tesvik:itiraz` → `itiraz-hazirlik`

Claude Code'da plugin komutları `<plugin-adı>:<komut-adı>` şeklinde adlandırılır, bu yüzden tam komut isimleri yukarıdaki gibidir. Başka bir eklentiyle çakışmadığı sürece kısaca `/degerlendir` ya da `/tara` yazmak da çalışır.

## Gereksinimler

Her skill'in çalışması için sohbette paylaşmanız gereken en az bir girdi vardır; bazı skill'ler ayrıca daha doğru sonuç için `references/` klasörüne eklenmiş resmi bir belgeye ihtiyaç duyar. Bu belgeler zorunlu değildir — eksikse skill veriyi uydurmak yerine ilgili bilgiyi "bilinmiyor" (UNKNOWN) olarak işaretler (bkz. `docs/evidence-protokolu.md`) — ama olmadan sonuç eksik kalır.

| Skill | Sohbette paylaşmanız gereken | `references/` klasöründe önerilen belge |
|---|---|---|
| `hakem-simulasyonu` | Proje önerisi taslağı | TEYDEB/ARDEB Uygulama Esasları |
| `gider-kalemi-kontrolu` | Bütçe/gider kalemi tablosu | Gider Formları Hazırlama Kılavuzu / Bütçe Hazırlama Rehberi |
| `cagri-tarama` | — (girdi gerekmez, web'den canlı tarar) | — |
| `donem-raporu-kontrolu` | Rapor taslağı (+ mümkünse onaylı proje planı/AGY101) | AGY301 (Gelişme Raporu) veya Sonuç Raporu şablonu |
| `proje-tutarlilik-kontrolu` | En az iki proje belgesi (karşılaştırma için) | — |
| `itiraz-hazirlik` | Mevcut proje metni + hakem raporu | TÜBİMER İtiraz Usul ve Esasları |
| `patent-on-arastirma` | Fikrin/ürünün kısa açıklaması | — (markapatent-mcp üzerinden TÜRKPATENT'te canlı arar) |

`references/` klasörüne eklenecek belgelerin tam listesi, her birinin ne işe yaradığı ve nereden indirileceği için `references/README.md`'ye bakın. Tüm belgeler TÜBİTAK'ın resmi sitesinden ([tubitak.gov.tr](https://www.tubitak.gov.tr)) indirilir; telif hakkı nedeniyle bu depoda yeniden dağıtılmazlar, bu yüzden ilgili belgeyi güncel haliyle siz eklemelisiniz.

## Kurulum

Bu depo hem plugin'i (`.claude-plugin/plugin.json`) hem de kendi kendini listeleyen bir marketplace'i (`.claude-plugin/marketplace.json`) içerir, bu yüzden ek bir marketplace deposuna ihtiyaç yoktur.

Claude Code kurulu olan normal bir terminalde şu iki komutu çalıştırın:

```
claude plugin marketplace add ibrahim-isikli/arge-tesvik-skills
claude plugin install arge-tesvik@arge-tesvik-skills
```

Bundan sonra `claude` yazıp yeni bir oturum açtığınızda eklenti hazır olur — ayrıca bir "reload" adımına gerek yoktur, çünkü her yeni `claude` oturumu kurulu plugin'leri zaten yükler. Deneme için: `/arge-tesvik:degerlendir` yazın ya da bir taslak paylaşıp "hakem ne der?" deyin.

Adımların terminalde tam olarak nasıl göründüğü:

![Kurulum adımları: claude plugin marketplace add, claude plugin install](./assets/kurulum-demo.gif)

Zaten açık bir Claude Code oturumundaysanız aynı işlemi oturumun kendi komut satırına `/plugin marketplace add ...` ve `/plugin install ...` yazarak da yapabilirsiniz. Bu durumda kurulum özeti "Run /reload-plugins to activate." derse `/reload-plugins` çalıştırmanız gerekir.

Yerelde geliştirirken/denerken (marketplace/install adımları olmadan, doğrudan klasörden):

```
claude --plugin-dir /path/to/arge-tesvik-skills
```

## Kullanım örneği

### hakem-simulasyonu

Kurulumdan sonra herhangi bir slash komutu yazmanıza da gerek yok — bir proje önerisi taslağı paylaşıp "hakem ne der?" demeniz `hakem-simulasyonu` skill'ini tetiklemeye yeter. Aşağıda gerçek bir taslakla alınan çıktının ilk kısmı var; raporun tamamı üç boyutu, düzeltme önerilerini ve ÜYZ/beyan hatırlatmalarını da içerecek şekilde devam eder:

![Kullanım örneği: hakem-simulasyonu'na taslak paylaşıp kritik alma](./assets/kullanim-demo.gif)

### cagri-tarama

Aynı şekilde, "TÜBİTAK'ın açık çağrıları neler, 1501 ve 1507'nin son başvuru tarihi ne zaman?" demeniz yeterli. Aşağıdaki GIF'te tam tablo (1001, 1505, 1707, 1511, 3001 dahil) dar terminal genişliğine sığması için liste düzeninde gösterildi:

![Kullanım örneği: cagri-tarama ile açık TÜBİTAK çağrılarını sorgulama](./assets/cagri-tarama-demo.gif)

**Önemli:** GIF'teki tarihler 6 Ağustos 2026'da yapılan bir taramaya ait, örnek olsun diye burada donmuş durumda — canlı/güncel değil. Skill her çalıştığında yeniden tarama yapar; kendi sorgunuzda güncel tarihleri göreceksiniz.

## markapatent-mcp bağlantısı

`patent-on-arastirma` skill'i, `plugin.json` içinde tanımlı uzak bir HTTP MCP sunucusuna (`https://markapatent-mcp.fastmcp.app/mcp`) bağımlıdır. Plugin etkinleştirildiğinde bu sunucu otomatik başlatılır/bağlanır; ilk kullanımda Claude Code sizden onay isteyebilir. Sunucunun kendisi bu eklentinin bir parçası değildir — TÜRKPATENT verisine erişimi markapatent tarafı sağlar.

## references/ klasörü

`references/` klasörü kasıtlı olarak boş gelir. TÜBİTAK'ın uygulama esasları, AGY101/AGY301 şablonları ve güncel çağrı metinleri gibi belgeler sık güncellendiği ve bu depoda yeniden dağıtılması uygun olmadığı için, bu belgeleri tubitak.gov.tr'den indirip kendiniz eklemeniz gerekir. Hangi dosyaların nereden indirileceği için `references/README.md`'ye bakın.

İndirdiğiniz dosyaları klasöre taşımak, herhangi bir dosya yöneticisiyle ya da terminalde `mv`/sürükle-bırak ile yapılan sıradan bir işlemdir — örnek:

![references/ klasörünü indirilen dosyalarla doldurma örneği](./assets/references-demo.gif)

## Evidence protokolü ve ortak kurallar

`docs/evidence-protokolu.md`, skill'lerin güncel/sayısal/hukuki iddialarda kullandığı ortak sınıflandırma modelini (FACT / INFERENCE / USER-PROVIDED / UNKNOWN / OUTDATED / CONFLICTING), kaynak güven hiyerarşisini ve her skill'in sonunda tekrarlanan zorunlu uyarı bloğunun kanonik metnini tek yerde toplar. Skill'lerdeki uyarı blokları bilinçli olarak kendi dosyalarında (inline) tutulur — bu dosya bir çalışma zamanı bağımlılığı değil, bakım/tutarlılık için tek doğru kaynaktır.

## Doğrulama ve testler

- `scripts/validate.py` — bağımlılıksız (stdlib) bir statik doğrulama scripti: `plugin.json`/`marketplace.json` JSON geçerliliği, her skill'in SKILL.md frontmatter kısıtlarına (isim/karakter seti/uzunluk, açıklama uzunluğu) uyup uymadığı, slash komutlarının var olan bir skill'e referans verip vermediği ve plugin sürümüyle CHANGELOG'un eşleşip eşleşmediğini kontrol eder. Çalıştırmak için: `python3 scripts/validate.py`. Bu depoda otomatik bir CI workflow'u yok — commit öncesi elle çalıştırın.
- `skills/gider-kalemi-kontrolu/scripts/check_table.py` — o skill'in zorunlu çıktı tablosunun (5 kolon: Gider/Kategori Uygunluğu/Gerekçelendirme Yeterliliği/Kanıt Durumu/Risk) şemasını mekanik olarak kontrol eder; skill kendi çıktısını göndermeden önce bunu çalıştırması beklenir (garanti değil — bkz. Sınırlamalar).
- `tests/` — her skill için LLM-graded manuel eval senaryoları (normal durum, eksik bilgi, hallucination tuzağı, çelişkili bilgi, güncelliğini yitirmiş bilgi, kötü niyetli girdi, belirsiz istek). Bunlar otomatik CI testi değildir; nasıl kullanılacağı için `tests/README.md`'ye bakın.
- `tests/golden/` — çoklu belge/çoklu skill ve cross-skill tutarlılık regresyonu için yapılandırılmış bir çerçeve (henüz gerçek proje verisi yok, sadece şablon). Detaylar için `tests/golden/README.md`.

## Sınırlamalar

- Skill'ler birer LLM talimat kümesidir, deterministik doğrulayıcı değildir — çıktıları her zaman bir başlangıç noktasıdır, resmi karar/hukuki görüş yerine geçmez.
- `cagri-tarama` ve `patent-on-arastirma` canlı web/MCP erişimine bağımlıdır; ağ erişimi yoksa veya kaynak sayfa değişmişse sonuçlar eksik/hatalı olabilir (skill'ler bu durumu sessizce geçmemek üzere yazıldı, ama garantisi yoktur).
- `references/` klasörü boş gelir; skill'ler güncel mevzuat/şablon metnini kendiliğinden "bilmez" — doğru çalışmaları için ilgili resmi belgeleri siz eklemelisiniz.
- Bu eklenti TÜBİTAK veya TÜRKPATENT ile resmi bir ilişki içinde değildir; hiçbir skill çıktısı resmi başvuru sonucu garantisi taşımaz.
- `gider-kalemi-kontrolu`'nun zorunlu 5 kolonlu çıktı tablosu (Gider/Kategori Uygunluğu/Gerekçelendirme Yeterliliği/Kanıt Durumu/Risk) gerçek runtime testlerinde **içerik olarak her zaman doğru** ama **kolon başlıkları/şema olarak garanti edilemedi** — model bazen farklı bir tablo yapısı üretebilir. Bu şema uyumsuzluğunu otomatik tespit etmek isterseniz `skills/gider-kalemi-kontrolu/scripts/check_table.py`'ı çıktıya karşı elle çalıştırabilirsiniz. Bilgi doğruluğunu etkilemez, sadece programatik ayrıştırma yapıyorsanız önemlidir.

## Sorun giderme

- **`patent-on-arastirma` çalışmıyor / MCP hatası veriyor**: `markapatent-mcp` sunucusu bu eklentiden bağımsız, üçüncü taraf bir uzak servistir. Sunucu geçici olarak erişilemez olsa bile bu **sadece `patent-on-arastirma` skill'ini** etkiler — diğer altı skill markapatent-mcp'ye bağımlı değildir ve normal çalışmaya devam eder. Skill, bağlantı hatasını açıkça bildirip boş sonuç uydurmamalıdır; böyle davranmıyorsa bir hata olarak bildirin.
- **Slash komutu görünmüyor**: Eklentinin yüklendiğini (`claude plugin list` veya oturum başlangıcındaki plugin listesi) ve `/reload-plugins` gerekip gerekmediğini kontrol edin (bkz. Kurulum bölümü).
- **Skill tetiklenmiyor ama slash komutu çalışıyor**: Skill'in `description` alanı, Claude'un ne zaman tetikleyeceğine karar verdiği tetikleme kuralıdır; isteğinizde skill'in kapsadığı anahtar kelimelerden (örn. "hakem", "gider kalemi", "itiraz") biri geçmiyorsa ilgili slash komutunu doğrudan kullanmanız daha güvenilirdir.

## Otomatik çağrı takibi (opsiyonel)

`cagri-tarama` her çalıştığında canlı tarama yapar, ama isterseniz Claude Code'un Routine (zamanlanmış tetikleyici) özelliğiyle bunu periyodik hale getirebilirsiniz — örneğin her Pazartesi `/arge-tesvik:tara` çalıştırıp yeni çağrı veya yaklaşan son başvuru tarihi varsa size haber vermesini isteyebilirsiniz. Bu, depoya gömülü bir özellik değil, Claude Code'un genel zamanlama mekanizmasının bu eklentiyle kullanımıdır; kurmak isterseniz Claude'a "her Pazartesi /arge-tesvik:tara çalıştır ve yeni çağrı varsa bana haber ver" demeniz yeterli.

## Sürüm geçmişi

Değişiklikler için [CHANGELOG.md](./CHANGELOG.md)'ye bakın.

## Katkıda bulunma

Yeni bir skill önermeden veya PR açmadan önce [CONTRIBUTING.md](./CONTRIBUTING.md)'yi okuyun (zorunlu kurallar, test etme adımları, skill yazım kuralları). Katkı sağlarken [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)'ye uyulması beklenir.

## Zorunlu kurallar (tüm skill'lerde geçerli)

Her skill, TÜBİTAK ÜYZ (üretken yapay zeka) Rehberi (Eylül 2025) kapsamında şu kurallara uyacak şekilde yazıldı:

- **Gizlilik**: Ciro, bütçe detayı, yayınlanmamış teknik bilgi gibi hassas/gizli firma verileri araca girilmemeli; skill'ler kullanıcıyı bu konuda uyarır ve placeholder mantığıyla çalışır.
- **Beyan zorunluluğu**: Proje önerisi hazırlanırken bir ÜYZ aracından önemli ölçüde faydalanıldıysa, bunun başvuruda beyan edilmesi gerektiğini her skill çıktısının sonunda hatırlatır.
- **Nihai sorumluluk**: Başvurunun içeriğinden ve doğruluğundan nihai olarak başvuru sahibi sorumludur; hiçbir skill bu sorumluluğu üstlenmez.

## İlgili eklenti

5746 sayılı Kanun kapsamında bir Ar-Ge/Tasarım/Yenilik Merkezi kurmak veya sürdürmek istiyorsanız (TEYDEB/ARDEB proje hibesinden farklı, kurumsal/firma bazlı bir teşvik rejimi), aynı geliştiricinin [arge-merkezi-uygunluk-kontrolu](https://github.com/ibrahim-isikli/arge-merkezi-uygunluk-kontrolu) eklentisine bakın.
