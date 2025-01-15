from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

# Tarayıcıyı başlat
driver = webdriver.Firefox()

# Giriş işlemi
try:
    driver.get('https://www.linkedin.com')
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/main/section[1]/div/div/a'))
    )
    login_button.click()

    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
    )
    username.send_keys('snyksl408@gmail.com')

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
    )
    password.send_keys('sena2221')

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[4]/button'))
    )
    sign_in_button.click()
except Exception as e:
    print("Giriş işlemi sırasında hata oluştu:", e)
    driver.quit()
    exit()

# İş ilanı linkleri
links = [
    "https://www.linkedin.com/jobs/search/?currentJobId=4109209007&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4095569605&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4108648315&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4099222682&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4112914227&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4084886084&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4122909537&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4115474528&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4094270670&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4087295698&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=3951416938&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4115472955&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=3974788529&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4084775216&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4103384705&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4066757388&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4111037209&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4036359491&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4064489156&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4113625037&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4120380813&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://linkedin.com/jobs/search/?currentJobId=3966569679&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4109623856&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=3841773852&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4056926976&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=150",
    "https://www.linkedin.com/jobs/search/?currentJobId=4084776663&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=3815201875&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4093606146&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4062478272&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4103121599&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4109631143&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4109630207&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4087693184&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4056914644&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4109202636&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4086220707&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4078445372&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4108649691&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4096852965&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4079319799&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4016780402&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4086403735&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4034550574&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4069877480&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4064274659&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4082047542&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4042556462&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4120393073&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=4108504415&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175",
    "https://www.linkedin.com/jobs/search/?currentJobId=3802252249&geoId=102105699&keywords=Bilgisayar%20M%C3%BChendisi&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&start=175"
]

# Bilgi çekme fonksiyonu
def safe_find(xpath, timeout=10):
    retries = 3
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text
        except Exception as e:
            print(f"Element bulunamadı veya hata oluştu: {e}")
            continue
    return None

# Tüm ilan bilgilerini saklamak için bir liste
all_job_data = []

# Her link için veri çekme işlemi
for link in links:
    driver.get(link)
    time.sleep(5)  # Sayfanın tam yüklenmesi için bekleme

    try:
        # Verileri çek
        job_data = {
            "İlan Adı": safe_find('/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/div/h1/a') or "Veri yok",
            "Uzaktan/Normal": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[4]/ul/li[1]/span/span[1]') or "Veri yok",
            "Çalışma Şekli": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[4]/ul/li[1]/span/span[2]') or "Veri yok",
            "İstenen Tecrübe": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[4]/ul/li[1]/span/span[3]') or "Veri yok",
            "Yetenekler": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[4]/ul/li[2]/button/a') or "Veri yok",
            "Detay": safe_find('//*[@id="job-details"]') or "Veri yok",
            "Şirket": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/div/a') or "Veri yok",
            "Sektör": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/section/section/div[1]/div[2]') or "Veri yok",
            "Konum": safe_find('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[3]/div/span[1]') or "Veri yok",
        }
        all_job_data.append(job_data)
        print(f"İlan verileri çekildi: {job_data}")
    except Exception as e:
        print(f"Veri çekme sırasında hata oluştu: {e}")

    time.sleep(30)  # Her ilan arasında 1 dakika bekleme

# Pandas ile Excel'e yaz
existing_file = "job_details.xlsx"

if os.path.exists(existing_file):
    # Mevcut dosyayı yükle
    existing_data = pd.read_excel(existing_file, engine='openpyxl')
    # Yeni verilerle birleştir
    combined_data = pd.concat([existing_data, pd.DataFrame(all_job_data)], ignore_index=True)
else:
    # Yeni verileri kullan
    combined_data = pd.DataFrame(all_job_data)

# Dosyayı kaydet
combined_data.to_excel(existing_file, index=False, engine='openpyxl')
print("Tüm ilan bilgileri başarıyla Excel dosyasına kaydedildi!")

# Tarayıcıyı kapat
driver.quit()
