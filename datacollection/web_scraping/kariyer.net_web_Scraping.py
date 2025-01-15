from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Tarayıcıyı başlat
driver = webdriver.Firefox()  # ChromeDriver yüklü olmalı

# URL
url = "https://www.kariyer.net/is-ilani/emse-a-s-yazilim-muhendisi-4017299"
driver.get(url)

# İlk koddaki alanlar
fields_first = {
    "Çalışma Şekli": "//div[h3[contains(text(), 'Çalışma Şekli')]]/p",
    "Pozisyon Seviyesi": "//div[h3[contains(text(), 'Pozisyon Seviyesi')]]/p",
    "Departman": "//div[h3[contains(text(), 'Departman')]]/p",
}

# İkinci koddaki alanlar
fields_second = {
    "İlan Adı": '//*[@id="__layout"]/div/div[2]/main/section/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]/h1/p/span/span',
    "Şirket Adı": '//*[@id="__layout"]/div/div[2]/main/section/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]/h1/a',
    "Konum": '//*[@id="__layout"]/div/div[2]/main/section/div/div/div[1]/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/span',
    "Uzaktan/Normal": '//*[@id="__layout"]/div/div[2]/main/section/div/div/div[1]/div[1]/div/div/div[1]/div[3]/div[1]/div[2]/p',
    "İstenen Tecrübe": '//*[@id="__layout"]/div/div[2]/main/section/div/div/div[1]/div[3]/section/div[1]/label[2]/span',
    "Eğitim Seviyesi": '//*[@id="__layout"]/div/div[2]/main/section/div/div/div[1]/div[3]/section/div[2]/label[2]/span',
}

data = {}

try:
    # Sayfanın tamamen yüklenmesini beklemek için 5 saniye bekle
    time.sleep(20)

    # İlk koddaki alanları çek
    for field_name, xpath in fields_first.items():
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            data[field_name] = element.text.strip() if element else "Bulunamadı"
        except Exception as e:
            data[field_name] = "Bulunamadı"
            print(f"{field_name} alınamadı:", e)

    # "Daha Fazla Gör" butonuna tıkla (varsa)
    try:
        daha_fazla_gor_butonu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Daha Fazla Gör")]'))
        )
        daha_fazla_gor_butonu.click()
        time.sleep(5)  # İçeriğin yüklenmesini bekle
    except Exception as e:
        print("Daha Fazla Gör butonu bulunamadı veya tıklanamadı:", e)

    # Genel Nitelikler ve İş Tanımı kısmını çek
    try:
        genel_nitelikler_element = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job-detail-qualifications"))
        )
        genel_nitelikler_text = genel_nitelikler_element.get_attribute("innerText")
        data["Genel Nitelikler ve İş Tanımı"] = genel_nitelikler_text.strip()
    except Exception as e:
        data["Genel Nitelikler ve İş Tanımı"] = "Bulunamadı"
        print("Genel Nitelikler ve İş Tanımı kısmı alınamadı:", e)

    # İkinci koddaki diğer alanları çek
    for field_name, xpath in fields_second.items():
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            data[field_name] = element.text.strip() if element else "Bulunamadı"
        except Exception as e:
            data[field_name] = "Bulunamadı"
            print(f"{field_name} alınamadı:", e)

finally:
    # Tarayıcıyı kapat
    driver.quit()

# Veriyi pandas DataFrame'e dönüştür
df = pd.DataFrame([data])

# İlan adı kontrolü
if data.get("İlan Adı") and data["İlan Adı"] != "Bulunamadı":
    # Veriyi pandas DataFrame'e dönüştür
    df = pd.DataFrame([data])

    # Eğer daha önce bir Excel dosyası varsa, yeni verileri mevcut sütunlara ekle
    try:
        existing_df = pd.read_excel("kariyer_net_ilanlari.xlsx")
        # Yeni verilerle birleştir
        existing_df = pd.concat([existing_df, df], ignore_index=True)
        existing_df.to_excel("kariyer_net_ilanlari.xlsx", index=False)
        print("Yeni veriler mevcut dosyaya eklendi.")
    except FileNotFoundError:
        # Dosya yoksa yeni bir dosya oluştur
        df.to_excel("kariyer_net_ilanlari.xlsx", index=False)
        print("Yeni dosya oluşturuldu ve veriler kaydedildi.")
else:
    print("İlan adı alınamadığı için veri kaydedilmedi.")