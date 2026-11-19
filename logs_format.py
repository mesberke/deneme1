import re

corrupted_data = 0
invalid_data = 0
sensor_values = {}
logs = """
[2026-11-14 10:15:03] SENSOR=depth VALUE=2.35 UNIT=m
[2026-11-14 10:15:04] SENSOR=speed VALUE=1.80 UNIT=m/s
[2026-11-14 10:15:05] SENSOR=depth VALUE=2.41 UNIT=m
[2026-11-14 10:15:06] SENSOR=temp VALUE=err UNIT=C
[2026-11-14 10:15:07] SENSOR=speed VALUE=2.10 UNIT=m/s
[2026-13-14 10:15:08] SENSOR=depth VALUE=-1.00 UNIT=m
[2026-11-14 10:15:09] garbage line here

[2026-11-14 10:15:10] SENSOR=temp VALUE=18.5 UNIT=C
"""
# İstenenler: Görev 1
# logs metnini satırlara ayır, boş satırları atla.
# Her satırı regex ile ayrıştır (zaman, sensör adı, değer, birim). Eşleşmeyen satır “bozuk satır” sayılır.
# VALUE sayıya (float) çevrilemiyorsa try/except ile yakala, “geçersiz değer” say.
# depth negatif olamaz, negatifse “geçersiz değer” say.
# Geçerli değerleri bir sözlükte sensör adına göre grupla ({"depth": [...], ...}).
# Aşağıdaki gibi hizalı bir rapor yazdır (f-string kullan, sensör adı 8 karakter sola yaslı, sayılar 2 ondalık):
# 7. Raporun altına yazdır: bozuk satır sayısı, geçersiz değer sayısı,
# ilk ve son geçerli kayıt arasındaki süre (saniye) (datetime ile), ve ortalaması en yüksek olan sensör.
# Beklenen sonuçlar (doğrulama için): 1 bozuk satır, 2 geçersiz değer, 5 geçerli kayıt, süre 7 saniye, en yüksek ortalama temp.


def main():  # c deki main mantığı ile aynı çalışır ana fonkdur
    load_data()


def load_data():  # veriyi ayrıştırır ve assign value fonk ile dict(sensor values) atar
    split_logs = re.findall(r".+", logs, re.MULTILINE)
    global corrupted_data
    for index, data in enumerate(split_logs):
        sensor = re.search(r"sensor=(\S+)", data, re.IGNORECASE)
        value = re.search(r"value=(\S+)", data, re.IGNORECASE)
        unit = re.search(r"unit=(\S+)", data, re.IGNORECASE)
        date = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", data, re.IGNORECASE)
        time = re.search(r"(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<seconds>\d{2})", data, re.IGNORECASE)

        try:
            dict_value = {
                "sensor": sensor.group(1),
                "value": value.group(1),
                "unit": unit.group(1),
                "date": date.group(),
                "time": time.group(),
            }
        except AttributeError as err:
            print(err)
            corrupted_data +=1
            continue

        if not (value := control_float(sensor_value=value.group(1))):
            continue

        if sensor.group(1).lower() == "depth":  # noqa: SIM102
            if not control_depth(value):
                continue
    
        assign_value(dict_value)
    print(sensor_values)
    print_formatted_logs()

def assign_value(data):  # sensor_values degiskenine deger atar
    global sensor_values  # noqa: PLW0602
    if sensor_values.get(data["time"]) is None:
        sensor_values[data["time"]] = {}
    else :
        print("ayni zamana ait  2 veri geldi supheli tekrar inceleyin (ilk gelen veri alindi)")
        return
    try:
        sensor_values[data["time"]]["value"] = data["value"]
        sensor_values[data["time"]]["unit"] = data["unit"]
        sensor_values[data["time"]]["date"] = data["date"]
        sensor_values[data["time"]]["sensor"] = data["sensor"]
    except KeyError :
        sensor_values[data["time"]] = {
            "value": 0,
            "unit": 0 ,
            "date": 0,
            "sensor": 0,
        }
        sensor_values[data["time"]]["value"] = data["value"]
        sensor_values[data["time"]]["unit"] = data["unit"]
        sensor_values[data["time"]]["date"] = data["date"]
        sensor_values[data["time"]]["sensor"] = data["sensor"]
        return
    return


def find_max_value(sensor):# belirtilen sensore göre max degeri bulur
    set_values = set()
    max_value = 0
    for data in sensor_values.values(): 
        if data["sensor"] == sensor :
            set_values.add(data["value"]) 
    try:
        max_value = max(set_values)
    except Exception as e:  # noqa: BLE001
        print(e)
        return False
    return max_value


def find_min_value(sensor):
    set_values = set()
    min_value = 0
    for data in sensor_values.values(): 
        if data["sensor"] == sensor:
            set_values.add(data["value"])   # belirtilen sensore göre min degeri bulur
    try:
        min_value = min(set_values)
    except Exception as e:  # noqa: BLE001
        print(e)
        return False
    return min_value


def control_float(sensor_value,): 
    global invalid_data # verinin floata çevrilip çevrilmediğini kontrol eder float ise degeri degil ise false dondurur
    try:
        f_value = float(sensor_value)
    except ValueError as error:
        print(error)
        invalid_data +=1
        return False
    return f_value


def control_depth(depth_value):  # verideki depth degerini kontrol eder 0 dan kucukse false dondurur
    global corrupted_data, invalid_data

    if not depth_value:
        corrupted_data += 1
        return False
    if depth_value < 0:
        invalid_data += 1
        return False
    return depth_value


def print_formatted_logs(): # gorevde istenen sekilde logların terminale yazdirilmasını saglar
    print(f"{'Sensor':<10} {'value':<10} {'date':<14} {'time':<8}")
    set_sensors = set()
    for time,data in sensor_values.items():
        print(f"{data["sensor"] :<10} {data["value"]:<8} {data["date"]:<14} {time:<8}")
        set_sensors.add(data["sensor"])
    if set_sensors is None :
        return
    for sensor in set_sensors:
        print(f"{sensor} icin max value = {find_max_value(sensor)} - {sensor} icin min value  = {find_min_value(sensor)}")
    print(f"Corrupted data : {corrupted_data} - Invalid data  : {invalid_data}")
main()
