# Çıkış gerilimi tavanı: 28 V

Tarih: 2026-09-22 · Durum: karar (REV_C)

gopo'nun çıkışı en fazla **28 V** verir. USB PD 3.1 EPR spesifikasyonu 36 V ve 48 V sabit PDO'lara da izin verir, ama bu kartın güç zinciri 28 V'a göre boyutlandırılmıştır. Tavan yükseltilecekse aşağıdaki tablodaki her satır yeniden ele alınmalıdır.

## Tavanı belirleyen parça

**U1 AP33772S** (DS46176 Rev.10): "PD3.1 EPR/AVS up to 28V, SPR/PPS up to 21V". Kontrolcü 36/48 V PDO isteyemez; tavan doğrudan buradan gelir. VCC mutlak maksimum 34 V, 28 V PDO'da OVP 31 V.

## Zincirdeki gerilim sınırları (28 V'ta marj)

| Parça | Görev | Sınır | 28 V'ta durum |
|---|---|---|---|
| U1 AP33772S | PD sink | EPR 28 V; VCC abs 34 V, CC abs 34 V | Tavanı koyan parça |
| U3 INA226 | Akım/gerilim ölçümü | VBUS çalışma 36 V, abs 40 V | 36/48 V EPR'de elenir |
| U12 LM74801-Q1 | Çıkış anahtarı + ideal diyot | 65 V | Rahat |
| U12 OV (R55 237k / R56 10k) | Aşırı gerilim kesmesi | 30,4 V (29,5-31,3 V) | 28 V +%5 = 29,4 V'un üstünde |
| Q3, Q5 SQJB60EP | VBUS ve çıkış anahtarları | VDS 60 V | Rahat |
| D3, D7 SMBJ30A | VBUS / OUT_POS TVS | VRWM 30 V, VBR 33,3 V min, VC 48,4 V @12,4 A | 29,4 V'ta iletmez; marj dar |
| U5 AOZ1284 | 3,3 V buck | VIN 3-36 V, abs 40 V | V_PRE ≈ VBUS; uygun |
| U11 TPS55340 | V_PRE ön-boost (5,5-28 V'ta pass-through) | Hesapta 28 V'ta FB ~2,43 V < 3 V | Prototipte doğrulanacak |
| C29 EEHZA1V470P | Çıkış bulk | 35 V | %80 kullanım |
| C3, C12, C13, C27, C28, C14, C24, C26, C32 | VBUS / V_PRE seramikleri | 50 V | Rahat (X5R/X7R DC bias hesaba katılmalı) |
| C31 | LM74801 CAP-VS | 25 V | CAP-VS ~13-14 V; tavandan bağımsız |
| D2 SS2060FL, D4 SX36 | Buck / boost diyotları | 60 V | Rahat |

## Tavan yükseltilirse

36 V veya 48 V EPR için en azından şunlar değişmeli:

1. **U1**: 48 V EPR destekleyen bir PD sink kontrolcüsü.
2. **U3 INA226**: VBUS'ı ≥ 48 V ölçebilen bir monitör (ör. 85 V sınıfı).
3. **D3/D7**: VRWM ≥ 50 V TVS; bu durumda AP33772S'nin 34 V'luk VCC/CC sınırı TVS kırpmasıyla korunamaz, giriş mimarisi baştan ele alınmalı.
4. **U12 OV bölücüsü**, **C29** ve 50 V'luk seramikler (48 V'ta DC bias ile efektif kapasite çok düşer).
5. **U5 AOZ1284** (36 V) ve **U11 TPS55340** pass-through davranışı.

İlgili: maksimum çıkış akımı 3 A kararı `CIKIS_AKIMI_3A_KARARI_20260922.md`; U12 LM74801 geçişi `SEMA_TAMAMLANAN_TODO_REV_C_20260922.md`.
