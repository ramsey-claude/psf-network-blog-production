# Framer içerik girişi — sorun günlüğü + tekrar yaşamamak için prompt

Bu dosya, blog içeriklerini Framer CMS'e aktarırken yaşadığımız sorunları ve
bir daha yaşamamak için izlenecek yöntemi kaydeder. Yeni içerik partisinde
en alttaki "Yeniden kullanılabilir prompt"u kullan.

## Ortam (sabit gerçekler)
- Framer CMS koleksiyonu: **Articles**
- Gövde alanı: **Content** (rich-text). **Body** alanı KULLANILMIYOR (boş bırak).
- Alan eşlemesi:
  | İçerik parçası | Framer alanı |
  |---|---|
  | SEO/başlık | Title |
  | URL | Slug |
  | Dek / kısa özet | Excerpt |
  | "Quick Answer" özeti | TL;DR |
  | Asıl gövde | **Content** |
  | Meta description | Meta Description |
  | Anahtar kelimeler | Keywords |
  | Hero görseli | Hero Image (CSV'de değil, elle) |
  | Yazar / kategori | Author / Blog Categories (reference, elle) |

## Yaşadığımız sorunlar ve kökleri

1. **Yanlış CSV seçildi.** İlk denemede Framer'ın CMS Export çıktısı seçildi
   (1 satır, Author/Body kolonlu). Kök neden: dosya adı ayırt edici değildi ve
   doğrulama yapılmadı.
   → Çözüm: import ekranında HER ZAMAN **"X Items"** sayısı (12 olmalı) ve
   kolon listesinde **TL;DR** var mı diye bak.

2. **Kopya kaydı riski.** Mevcut Live yazılarla (best-fractional, reg-a) slug
   çakıştı.
   → Çözüm: import'ta **Slug Field = Slug** seç; çakışmada **Skip** (Update
   değil), "All items" işaretle. Mevcut Live içerik korunur.

3. **EN BÜYÜK SORUN — markdown düz metin olarak yapıştı.** Content alanına bir
   metin editöründen kopyalanan markdown, `##` ve `**` işaretleriyle harfi
   harfine girdi; biçimlenmedi. Kök neden: pano **text/plain** taşıyordu ve
   Framer rich-text editörü ham markdown'ı parse ETMİYOR.
   → Çözüm: gövdeyi **HTML olarak** ver. Markdown → HTML render et, dosyayı
   **tarayıcıda** aç, Ctrl/Cmd+A → C, Content'e yapıştır. Pano **text/html**
   taşıdığı için başlık/liste/kalın/link korunur.

4. **Gövdeyi CSV'ye koymak işe yaramaz.** CSV import gövdeyi düz metin yapar
   (format kaybolur). Bu yüzden CSV = sadece kısa alanlar; gövde = HTML paste.

5. **Tablolar.** Framer CMS rich-text tabloyu tam desteklemez. Tablolu
   yazılarda (REIT vs, Crowdfunding vs, Best Platforms) tablo paste sonrası
   bozulabilir → görsel veya Framer komponenti olarak ayrıca ekle.

## Doğru iş akışı (özet)
1. `workflow/build_framer_import.py` → `framer-articles-import.csv` (kısa
   alanlar) + `bodies/<slug>.md` (temiz gövde).
2. `workflow/render_bodies_html.py` → `html/<slug>.html` (paste için).
3. Framer: CSV Import → Slug Field=Slug → 12 Items + TL;DR doğrula → çakışmada
   Skip All → Import.
4. Her yazı: HTML'i tarayıcıda aç → tümünü kopyala → **Content**'e yapıştır.
5. Elle: Hero Image, Author, Blog Categories, Featured, Status=Live.
6. Tabloları ve stat-card/CTA bloklarını gözden geçir.

## Kontrol listesi (her partide)
- [ ] CSV import ekranında **Items = beklenen sayı** ve **TL;DR** kolonu var
- [ ] Slug Field = Slug seçili
- [ ] Mevcut Live yazılarda çakışma → **Skip** (Update değil)
- [ ] Gövde **HTML'den** yapıştırıldı, markdown'dan değil
- [ ] Body alanı boş, Content dolu
- [ ] Hero/Author/Category elle eklendi
- [ ] Tablolar kontrol edildi

---

## Yeniden kullanılabilir prompt (yeni içerik partisi için)

> psfnetwork blog içeriklerini Framer CMS "Articles" koleksiyonuna aktaracağım.
> Kurallar:
> - Gövde alanı **Content** (rich-text), Body kullanılmıyor.
> - Alanlar: Title, Slug, Excerpt(=dek), TL;DR(=quick answer), Meta
>   Description, Keywords; Hero/Author/Category elle.
> - Bana iki çıktı üret: (1) Framer alan adlarıyla birebir eşleşen tek
>   **CSV** (Title, Slug, Date, Featured, Excerpt, TL;DR, Meta Description,
>   Keywords — gövde YOK), (2) her yazı için **HTML** dosyası (markdown'dan
>   render, çünkü Framer ham markdown'ı parse etmez; HTML paste format korur).
> - Üretim işaretlerini temizle: H1'i ayır, `**Dek:**`, `[VISUAL-*]`,
>   `**Stat cards:**`.
> - Bana adım adım, kısa yönlendirmelerle ilerlet; her Framer adımında ekran
>   görüntüsü isteyerek doğrula. CSV import'ta Items sayısını ve TL;DR kolonunu
>   doğrulat; slug çakışmasında Skip dedirt.
> - Tabloları işaretle: Framer rich-text tabloyu tam desteklemez.
