# Beyin klonu

Bildiğin şeyleri kafandan çıkarıp, sorgulanabilir ve büyüyen bir yapıya koymak
için. Not defteri değil: not defteri ne yazdığını saklar, bu senin ne
bildiğini saklar ve seni ne kadar iyi tahmin ettiğini ölçer.

## Beş dakikada başlangıç

```bash
python3 workflow/mind.py init         # depoyu kur, tohum varsayımları yaz
python3 workflow/mind.py gaps         # klon neyi bilmiyor
python3 workflow/mind.py interview --n 8
```

`init`, bu reponun kanıtlarından çıkarılmış 19 varsayımı senin adına yazar.
Hepsi `onaysız`. İlk iş bunları gözden geçirmek, çünkü onaylamak saniye sürer
ve sıfırdan soru cevaplamaktan hızlıdır:

```bash
python3 workflow/mind.py confirm B-001 --durum onaylı
python3 workflow/mind.py confirm B-002 --durum reddedildi --note "tam tersi"
```

Sonra röportaj. `interview` bugünün oturum dosyasını açar, en verimli soruları
içine yazar. Cevapları dosyaya yaz, sonra:

```bash
python3 workflow/mind.py distill      # ham cevapları modele çevirmek için paket
```

## Ne nerede

| Yol | İçerik | Git |
|---|---|---|
| `workflow/mind.py` | Motor | evet |
| `mind/questions/bank.md` | 120 soruluk banka, 20 alan | evet |
| `mind/AGENT.md` | Bir Claude oturumunun uyacağı protokol | evet |
| `mind/private/model/` | Klonun kendisi: inançlar, kurallar, tercihler, kararlar | **hayır** |
| `mind/private/inbox/` | Ham yakalama | **hayır** |
| `mind/private/sessions/` | Röportaj oturumları | **hayır** |
| `mind/private/deltas/` | Provalar: klon ne dedi, sen ne dedin | **hayır** |

Bu repo herkese açık, bu yüzden klon deposu git dışında. Başka bir yerde
tutmak istersen `MIND_HOME` değişkenini kullan:

```bash
export MIND_HOME=~/Documents/beyin
python3 workflow/mind.py stats
```

Özel bir repoya taşımak için `python3 workflow/mind.py export --to ~/beyin-repo`.
Motoru ve bankayı da yanında götürür.

## Beş girdi tipi

| Tip | Ne zaman | Örnek |
|---|---|---|
| inanç | Dünya hakkında bir iddia | "Görünmeyen borç, bilinen borçtan tehlikelidir" |
| kural | Karar kalıbı | "Rekabet duruşu zayıfken o karşılaştırmayı yazma" |
| tercih | Ne sevdiğin, neye tahammülün yok | "Kapanmış konu denetimde yeniden açılmaz" |
| karar | Verilmiş, sonucu olan karar | "Voice sample beklemeyi bıraktık" |
| soru | Cevabı olmayan ama gereken | "Batch 2 kapakları neden geri alındı" |

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
| Aklına geldikçe | `capture "..."` |
| Haftada bir, 20 dakika | `interview --n 8`, sonra `distill` |
| Ayda bir | `rehearse` ile üç prova, `grade`, `fidelity` |
| Üç ayda bir | `gaps` içindeki tazelenmesi gerekenler: hâlâ böyle mi düşünüyorsun |

## Komutlar

```bash
python3 workflow/mind.py init                    # kur ve tohumla
python3 workflow/mind.py capture "..."           # ham yakalama
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

Bu klasör kişisel. `brain/` ise operasyonun hafızası: kurallar, olaylar,
makaleler. İkisi ayrı çünkü biri sen değişince değişir, diğeri operasyon
değişince.
