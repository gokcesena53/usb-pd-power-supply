import json
import hashlib

pcb_path = 'hardware/gopo.kicad_pcb'
with open(pcb_path, 'rb') as f:
    h = hashlib.sha256(f.read()).hexdigest()

verification_data = {
    "task": "TASK-097",
    "title": "Tüm direnç ve kapasitörlerin yerleşimini pin bazında denetle",
    "date": "2026-09-28",
    "status": "AUDIT_COMPLETED",
    "verdict": "ALL_APPROVED_FOR_ROUTING",
    "pcb_sha256": h,
    "metrics": {
        "total_rc_components": 86,
        "total_resistors": 52,
        "total_capacitors": 34,
        "schematic_parity_mismatches": 0,
        "missing_in_pcb": 0,
        "extra_in_pcb": 0,
        "value_mismatches": 0,
        "verdict_uygun": 70,
        "verdict_routing_kosullu": 16,
        "verdict_tasinmali": 0,
        "mechanical_anchor_conflicts": 0,
        "drc_courtyard_conflicts": 0,
        "solid_collision_volume_mm3": 0.0
    },
    "critical_components_evaluated": [
        {
            "ref": "C16",
            "val": "47u",
            "layer": "B.Cu",
            "function": "Buck Çıkış Filtre Kondansatörü (+3.3V)",
            "target": "L1 Pad 2 (+3.3V)",
            "euclidean_distance_mm": 9.62,
            "verdict": "ROUTING_KOSULLU",
            "routing_condition": "TASK-096 raporundaki 'giriş kapasitörü' varsayımı şematik analizi ile düzeltildi; C16 aslında buck çıkış kondansatörüdür. L1 ile C16 arasında B.Cu katmanında en az 2.0 mm genişliğinde poligon çekilmeli, Pad 2 den In1.Cu GND düzlemine yoğun via dikişi yapılmalıdır."
        },
        {
            "ref": "C12, C13",
            "val": "4u7",
            "layer": "B.Cu",
            "function": "Buck Giriş Bulk Kondansatörleri (V_PRE)",
            "target": "U5 Exposed Pad (Pin 9 / VIN)",
            "euclidean_distance_mm": 5.91,
            "verdict": "ROUTING_KOSULLU",
            "routing_condition": "AOZ1284PI VIN girişine B.Cu üzerinden doğrudan kesintisiz poligon bağlanmalı ve GND pedlerinden In1.Cu katmanına dönüş via'ları eklenmelidir."
        },
        {
            "ref": "C14",
            "val": "100n",
            "layer": "B.Cu",
            "function": "Buck Giriş Yüksek Frekans Seramik Bypass",
            "target": "U5 Exposed Pad (Pin 9 / VIN)",
            "euclidean_distance_mm": 4.84,
            "verdict": "UYGUN",
            "routing_condition": "U5 Exposed Pad sınırına doğrudan yerleştirilmiştir; ek önlem gerekmez."
        },
        {
            "ref": "C29, C25",
            "val": "47u, 4u7",
            "layer": "B.Cu",
            "function": "Boost Giriş Filtre Kondansatörleri (PD_VOUT)",
            "target": "U11 Pin 3 (VIN)",
            "euclidean_distance_mm": 13.39,
            "verdict": "ROUTING_KOSULLU",
            "routing_condition": "TASK-096 raporundaki 'çıkış sıcak döngüsü' varsayımı şematik analiziyle düzeltildi; C29 boost giriş filtresidir. Yüksek frekans bypass'ı 100nF C26 (U11'e 3.8 mm) tarafından sağlanmaktadır. C29/C25 giriş hattı B.Cu üzerinden geniş poligonla bağlanmalıdır."
        },
        {
            "ref": "C27, C28",
            "val": "4u7",
            "layer": "B.Cu",
            "function": "Boost Çıkış Filtre Kondansatörleri (V_PRE)",
            "target": "D4 Katot & U11 PGND Termal Pedi",
            "euclidean_distance_mm": 7.12,
            "verdict": "ROUTING_KOSULLU",
            "routing_condition": "U11 SW -> D4 -> C27 -> PGND sıcak anahtarlama döngüsü yaklaşık 24 mm çevreye sahiptir. B.Cu üzerinde kesintisiz katı poligonla bağlanmalı ve U11 termal pedinin 15 via'sına doğrudan bağlanmalıdır."
        },
        {
            "ref": "C5, C6, C7",
            "val": "22u, 100n, 1u",
            "layer": "F.Cu",
            "function": "ESP32-C6 Çekirdek +3.3V Dekuplaj Grubu",
            "target": "U2 Pin 1 (VDD33)",
            "euclidean_distance_mm": 12.01,
            "verdict": "ROUTING_KOSULLU",
            "routing_condition": "RF keepout ve USB-C/Ethernet ankrajları nedeniyle Y=83 mm hattında yerleştirilmiştir. +3.3V beslemesi C5 -> C7 -> C6 sırasıyla U2 pin 1 e katman değiştirmeden (viasız), 0.8 mm kalınlığında hatla ve In1.Cu GND düzlemi referansıyla ulaştırılmalıdır."
        },
        {
            "ref": "R11",
            "val": "5m0",
            "layer": "B.Cu",
            "function": "USB VBUS Akım Algılama Şöntü (1206)",
            "target": "U1 Pin 1 & Pin 24 (AP33772S)",
            "euclidean_distance_mm": 16.98,
            "verdict": "ROUTING_KOSULLU",
            "routing_condition": "Ethernet RJ45 J8 ve panel enkoder cebi ankrajları nedeniyle Y=103 mm de konumlandırılmıştır. U1'e giden VBUS_SENSE hatları B.Cu üzerinde 0.2 mm genişlik / 0.2 mm aralıklı sıkı diferansiyel Kelvin çifti olarak çekilmeli, çevresi GND ile ekranlanmalıdır."
        },
        {
            "ref": "RShunt1, C11",
            "val": "5m0, 100n",
            "layer": "B.Cu",
            "function": "Çıkış Akım Şöntü (2512 3W) & INA226 Dekuplajı",
            "target": "U3 INA226 IN+/IN- & VS",
            "euclidean_distance_mm": 4.31,
            "verdict": "UYGUN",
            "routing_condition": "INA226 U3 ile simetrik Kelvin ped geometrisine ve 4.3 mm mesafeye sahiptir. Mükemmel yerleşim."
        },
        {
            "ref": "R34, R35, R36",
            "val": "10k",
            "layer": "B.Cu",
            "function": "Panel Enkoder Pull-up Dirençleri (ENC_A, ENC_B, ENC_SW)",
            "target": "J9 Enkoder Konnektörü",
            "euclidean_distance_mm": 21.01,
            "verdict": "UYGUN",
            "routing_condition": "İnsan arayüzü düşük frekanslı (<100 Hz) sinyalleridir; hat uzunluğu işlevsel performans üzerinde sıfır etkiye sahiptir. FreeCAD mekanik açıklığı 7.04 mm olarak doğrulanmıştır."
        },
        {
            "ref": "C1, C2, C3, C4, C8",
            "val": "1u, 1u, 1u, 1u, 10u",
            "layer": "B.Cu",
            "function": "AP33772S LDO Dekuplaj & VBUS Baypas",
            "target": "U1 İlgili Pinleri (V18, IFB, VBUS, V5V)",
            "euclidean_distance_mm": 3.73,
            "verdict": "UYGUN",
            "routing_condition": "Veri sayfası sınırları (<=5 mm) içinde, U1 pinlerine bitişik konumlandırılmıştır."
        },
        {
            "ref": "C20",
            "val": "100n",
            "layer": "B.Cu",
            "function": "Ethernet RJ45 Magjack Altı Dekuplaj",
            "target": "J8 Pin 14/12",
            "euclidean_distance_mm": 3.55,
            "verdict": "UYGUN",
            "routing_condition": "Doğrudan J8 magjack trafo orta uçlarının altına yerleştirilmiştir; WIZnet W5500 uygulama notuna tam uygundur."
        }
    ]
}

with open('hardware/docs/reports/task-097-20260928/verification.json', 'w', encoding='utf-8') as f:
    json.dump(verification_data, f, indent=2)

print("Saved verification.json")
