import re

corrupted_data = 0 
invalid_data = 0

logs = """
[2026-11-14 10:15:03] SENSOR=depth SENSOR_VALUE=2.35 UNIT=m
[2026-11-14 10:15:04] SENSOR=speed SENSOR_VALUE=1.80 UNIT=m/s
[2026-11-14 10:15:05] SENSOR=depth SENSOR_VALUE=2.41 UNIT=m
[2026-11-14 10:15:06] SENSOR=temp SENSOR_VALUE=err UNIT=C
[2026-11-14 10:15:07] SENSOR=speed SENSOR_VALUE=2.10 UNIT=m/s
[2026-13-14 10:15:08] SENSOR=depth SENSOR_VALUE=-1.00 UNIT=m
[2026-11-14 10:15:09] garbage line here

[2026-11-14 10:15:10] SENSOR=temp SENSOR_VALUE=18.5 UNIT=C
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
    format_data()
def format_data():
    split_logs = re.findall(r".+",logs,re.MULTILINE)
    sensor_values = {}
    for index,data in enumerate(split_logs):
        pat = r"(?P<key>unit|value|sensor)\s*[:=]\s*(?P<value>-?\w+(?:\.\w+)?)"
        date = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",data,re.IGNORECASE)
        time = re.search(r"(?P<hour>\d{4})-(?P<minute>\d{2})-(?P<seconds>\d{2})",data,re.IGNORECASE)

        if  (pat is not None ) & (date is not None)  & (time is not None):
            for m in re.finditer(pat, data, re.IGNORECASE):
                if m.group("key").lower() == "depth":  # noqa: SIM102
                    if  f_value := control_depth(m.group("value")) :
                        continue
                try:
                    sensor_values[m.group("key").lower()+"-values"].append(f_value)
                except KeyError as error:
                    print(error)
                    sensor_values[m.group("key").lower()+"-values"] = []
                                   
def find_max_value(sensor):
    pass
def find_min_value(sensor):
    pass
def control_float(sensor_value):
    pass
def control_depth(depth_value):
    global corrupted_data,invalid_data
        
    f_depth = control_float(depth_value)
    if not f_depth:
        corrupted_data += 1
        return False
    if f_depth < 0:
        invalid_data += 1
        return False
    return f_depth
def print_formatted_logs():
    pass

main()