
logs = """
[2026-11-14 10:15:03] SENSOR=depth VALUE=2.35 UNIT=m
[2026-11-14 10:15:04] SENSOR=speed VALUE=1.80 UNIT=m/s
[2026-11-14 10:15:05] SENSOR=depth VALUE=2.41 UNIT=m
[2026-11-14 10:15:06] SENSOR=temp VALUE=err UNIT=C
[2026-11-14 10:15:07] SENSOR=speed VALUE=2.10 UNIT=m/s
[2026-11-14 10:15:08] SENSOR=depth VALUE=-1.00 UNIT=m
[2026-11-14 10:15:09] garbage line here

[2026-11-14 10:15:10] SENSOR=temp VALUE=18.5 UNIT=C
"""
#İstenenler: Görev 1
#logs metnini satırlara ayır, boş satırları atla.
#Her satırı regex ile ayrıştır (zaman, sensör adı, değer, birim). Eşleşmeyen satır “bozuk satır” sayılır.
#VALUE sayıya (float) çevrilemiyorsa try/except ile yakala, “geçersiz değer” say.
#depth negatif olamaz, negatifse “geçersiz değer” say.
#Geçerli değerleri bir sözlükte sensör adına göre grupla ({"depth": [...], ...}).
#Aşağıdaki gibi hizalı bir rapor yazdır (f-string kullan, sensör adı 8 karakter sola yaslı, sayılar 2 ondalık):
#7. Raporun altına yazdır: bozuk satır sayısı, geçersiz değer sayısı, 
# ilk ve son geçerli kayıt arasındaki süre (saniye) (datetime ile), ve ortalaması en yüksek olan sensör.
#Beklenen sonuçlar (doğrulama için): 1 bozuk satır, 2 geçersiz değer, 5 geçerli kayıt, süre 7 saniye, en yüksek ortalama temp.

def main():
    pass
def split_logs():
    pass
def find_max_value(sensor):
    pass
def find_min_value(sensor):
    pass
def control_float(sensor_value):
    pass
def control_depth(depth_value):
    pass
def print_formatted_logs():
    pass

