# Beyin klonu

Bildiğin şeyleri kafandan çıkarıp, sorgulanabilir ve büyüyen bir yapıya koymak
için. Not defteri değil: not defteri ne yazdığını saklar, bu senin ne
bildiğini saklar ve seni ne kadar iyi tahmin ettiğini ölçer.

Klon boş başlar ve senin cevaplarınla dolar. Konusu sensin: bir işe, bir
şirkete ya da bu repoya bağlı değil.

```bash
python3 workflow/mind.py init         # depoyu kur (varsayılan: ~/.mind)
python3 workflow/mind.py interview --n 8
```

`interview` bugünün oturum dosyasını açar ve en verimli soruları içine yazar.
Cevapları **Cevap:** satırının altına yazarsın, ham hali yeterli. Sonra:

```bash
python3 workflow/mind.py distill      # ham cevapları modele çevirmek için paket
```

Aklına bir şey geldiğinde soru beklemene gerek yok:

```bash
python3 workflow/mind.py capture "şunu fark ettim"
python3 workflow/mind.py addq "kendi soruma cevap vermeliyim" --domain kendi
```

Bu depoyu bir iş reposunun kayıtlarıyla tohumlamak istersen
`init --from-repo` bunu yapar: o repodaki kararlardan varsayım çıkarır, hepsini
`onaysız` yazar, kaynağını da ekler. İsteğe bağlı, çünkü bir proje seni değil,
senin bir dilimini gösterir.

## Ne nerede

| Yol | İçerik | Git |
|---|---|---|
| `workflow/mind.py` | Motor, kendi kendine yeter, başka dosyaya bağlı değil | evet |
| `mind/questions/bank.md` | 112 soruluk başlangıç bankası, 18 alan | evet |
| `mind/AGENT.md` | Bir Claude oturumunun uyacağı protokol | evet |
| `~/.mind/model/` | Klonun kendisi: inançlar, kurallar, tercihler, kararlar | **hayır** |
| `~/.mind/inbox/` | Ham yakalama | **hayır** |
| `~/.mind/sessions/` | Röportaj oturumları | **hayır** |
| `~/.mind/deltas/` | Provalar: klon ne dedi, sen ne dedin | **hayır** |
| `~/.mind/questions.md` | Cevaplarından doğan kendi soruların | **hayır** |

Depo varsayılan olarak `~/.mind`, yani bu reponun tamamen dışında. Başka bir
yerde tutmak istersen:

```bash
export MIND_HOME=~/Documents/beyin
python3 workflow/mind.py stats
```

Özel bir repoya taşımak için `python3 workflow/mind.py export --to ~/beyin-repo`.
Motoru ve bankayı da yanında götürür.

## Beş girdi tipi

| Tip | Ne zaman | Örnek |
|---|---|---|
| inanç | Dünya hakkında bir iddia | "Görünmeyen sorun, bilinen sorundan tehlikelidir" |
| kural | Karar kalıbı | "Geri dönülemez bir kararda bir gece bekle" |
| tercih | Ne sevdiğin, neye tahammülün yok | "Kapanmış konuyu tekrar açan toplantıya girmem" |
| karar | Verilmiş, sonucu olan karar | "O ortaklıktan çıktım, sebebi şuydu" |
| soru | Cevabı olmayan ama gereken | "Bu işi üç yıl daha yapmak istiyor muyum" |

Her girdinin durumu var: `onaysız` (klon çıkardı, sen onaylamadın), `onaylı`
(senin sözün), `revize`, `reddedildi`. İkiz sadece `onaylı` girdilerden
konuşur. Reddedilen girdi silinmez, çünkü fikrini değiştirdiğin yer de bilgidir.

## Klonun büyümesi

Dosya biriktirmek büyüme değil. Büyüme, klonun seni doğru tahmin etmeye
başlaması. Ölçüsü prova:

```bash
python3 workflow/mind.py rehearse --question "bu müşteriye şu fiyatı verir miydim"
# klon cevaplar, sen cevaplarsın, fark yeni girdi olur
python3 workflow/mind.py grade X-001 --verdict partial
python3 workflow/mind.py fidelity
```

Sadakat yükselmiyorsa klon yanlış şeyleri biliyordur. O zaman soruları
değiştirmek gerekir, daha çok yazmak değil.

## Ritim

| Ne zaman | Ne |
|---|---|
| Aklına geldikçe | `capture "..."`, `addq "..."` |
| Haftada bir, 20 dakika | `interview --n 8`, sonra `distill` |
| Ayda bir | `rehearse` ile üç prova, `grade`, `fidelity` |
| Üç ayda bir | `gaps` içindeki tazelenmesi gerekenler: hâlâ böyle mi düşünüyorsun |

## Komutlar

```bash
python3 workflow/mind.py init                    # kur (--from-repo ile tohumla)
python3 workflow/mind.py capture "..."           # ham yakalama
python3 workflow/mind.py addq "..." --domain kendi
python3 workflow/mind.py interview --n 8         # sıradaki sorular
python3 workflow/mind.py distill                 # ham kayıtları modele çevir
python3 workflow/mind.py add --kind kural ...    # tek girdi yaz
python3 workflow/mind.py confirm B-003 --durum onaylı
python3 workflow/mind.py ask "fiyatlandırma"     # klon bu konuda ne tutuyor
python3 workflow/mind.py rehearse                # prova aç
python3 workflow/mind.py grade X-001 --verdict right
python3 workflow/mind.py gaps                    # eksikler
python3 workflow/mind.py digest --days 7         # bu hafta ne oldu
python3 workflow/mind.py stats                   # klon ne kadar büyüdü
python3 workflow/mind.py check                   # bütünlük
python3 workflow/mind.py export --to ~/beyin     # taşı
```

## Sınırlar

Klon senin yerine karar vermez, senin ne karar vereceğini tahmin eder. Fark
önemli: tahmin yanlışsa düzeltirsin ve klon öğrenir, karar yanlışsa bedelini
ödersin.

Klona şifre, anahtar, sağlık verisi ya da üçüncü kişilerin mahrem bilgisi
girmez. Bu bir çalışma zihni, arşiv değil.

Bu klasör sana ait ve bu repodan bağımsız: motor tek dosya, depo `~/.mind`
içinde, ikisi de başka bir yere taşınabilir. `brain/` ayrı bir şey, bu reponun
kendi hafızası. Karıştırma: biri sen değişince değişir, diğeri buradaki iş
değişince.
