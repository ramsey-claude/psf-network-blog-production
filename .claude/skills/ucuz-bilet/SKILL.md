---
name: ucuz-bilet
description: >-
  İstanbul - Londra (veya belirtilen başka bir rota) için en ucuz uçak biletini
  web araştırmasıyla bulur. Kullanım: /ucuz-bilet [tarih veya rota].
  Örnek: /ucuz-bilet 15-20 Eylül, /ucuz-bilet tek yön SAW-STN Ekim.
---

# /ucuz-bilet: En Ucuz Uçak Bileti Araması

Bu komut çalıştırıldığında `traveler-agent` alt ajanını (Agent aracıyla,
`subagent_type: traveler-agent`) başlat ve kullanıcının verdiği argümanları
ona aynen aktar.

- Argüman verilmemişse: rota İstanbul -> Londra gidiş-dönüş, önümüzdeki 4-6
  haftada esnek tarih, 1 yetişkin olarak ara.
- Argüman verilmişse: tarih, rota, yön (tek yön / gidiş-dönüş) ve yolcu
  sayısını argümandan çıkar ve ajana ilet.

Ajan raporu döndüğünde sonucu kullanıcıya olduğu gibi, Türkçe ve
karşılaştırma tablosuyla sun. Fiyatların anlık olduğunu ve rezervasyon
sırasında değişebileceğini her raporun sonunda hatırlat.
