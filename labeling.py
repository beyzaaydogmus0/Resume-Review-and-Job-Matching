import pandas as pd

# Eğitim seviyesi sıralaması
education_levels = ["ön lisans", "lisans", "yüksek lisans", "doktora"]

# Eğitim seviyesini sıralamada bulmak için yardımcı fonksiyon
def get_education_rank(education):
    if pd.isna(education):
        return -1  # Belirtilmemişse
    education_list = [ed.strip() for ed in str(education).split(",")]
    ranks = [education_levels.index(ed) for ed in education_list if ed in education_levels]
    return max(ranks, default=-1)  # En yüksek seviyesi

# Eğitim seviyesi kontrolü
def check_education(cv_education, job_education):
    cv_rank = get_education_rank(cv_education)
    job_rank = get_education_rank(job_education)

    if cv_rank == -1:
        return 0  # CV'de eğitim seviyesi belirtilmemişse
    if job_rank == -1 or cv_rank >= job_rank:
        return 1  # İş ilanında belirtilmemiş veya CV seviyesi yeterliyse
    return 0  # CV seviyesi iş ilanına uygun değilse

# Çalışma yeri ve süresi eşleşmesi
def check_work_place_and_duration(job_row, cv_row):
    return job_row["Uzaktan/Normal"] == cv_row["Çalışma Şekli2"] and job_row["Çalışma Şekli"] == cv_row["Çalışma Türü"]

# Konum eşleşmesi
def check_location(job_row, cv_row):
    cv_location = cv_row["konum"]
    job_locations = str(job_row["Konum"]).split(",")  # İş ilanındaki iller virgülle ayrılmış olabilir
    return cv_location in job_locations

# Tecrübe eşleşmesi
def check_experience(job_row, cv_row):
    job_experience = job_row["İstenen Tecrübe"]
    cv_experience = cv_row["ÇALIŞMA ZAMANI (YIL)"]

    if pd.isna(cv_experience):
        return False  # CV'de tecrübe belirtilmemişse uygun olmadığını varsayın

    if pd.isna(job_experience) or str(job_experience).strip() == "":
        return True  # İş ilanında tecrübe belirtilmemişse uygun olduğunu varsayın

    try:
        if " ile " in str(job_experience):  # Örnek: "5 ile 10"
            min_exp, max_exp = map(int, str(job_experience).split(" ile "))
            return min_exp <= cv_experience <= max_exp
        else:  # Tek bir sayı belirtilmişse
            min_exp = int(job_experience)
            return cv_experience >= min_exp
    except ValueError:
        return False  # Beklenmeyen bir format varsa uygun olmadığını varsayın

# Yetenekler eşleşme oranı
def check_skills(job_row, cv_row):
    job_skills = set(str(job_row["Yetenekler"]).split(","))
    cv_skills = set(str(cv_row["YETENEKLER"]).split(","))
    if not job_skills or not cv_skills:
        return 0  # Yeteneklerden biri belirtilmemişse eşleşme olmaz
    matching_skills = job_skills.intersection(cv_skills)
    return len(matching_skills) / len(job_skills)  # İş ilanındaki yeteneklerin ne kadarına uyuluyor

# Ek özellik kontrolü (ÖNE ÇIKAN PROJE, SERTİFİKA ADI, GÖNÜLLÜLÜK YAPTIĞI ORGANİZASYON ADI)
def check_additional_features(cv_row):
    score = 0
    if not pd.isna(cv_row["ÖNE ÇIKAN PROJE"]) and str(cv_row["ÖNE ÇIKAN PROJE"]).strip():
        score += 1  # Proje varsa 1 puan
    if not pd.isna(cv_row["SERTİFİKA ADI"]) and str(cv_row["SERTİFİKA ADI"]).strip():
        score += 1  # Sertifika varsa 1 puan
    if not pd.isna(cv_row["GÖNÜLLÜLÜK YAPTIĞI ORGANİZASYON ADI"]) and str(cv_row["GÖNÜLLÜLÜK YAPTIĞI ORGANİZASYON ADI"]).strip():
        score += 1  # Gönüllülük varsa 1 puan
    return score / 3  # Bu özelliklerin toplamı, eşleşme oranına katkıda bulunur (0 ile 1 arasında)

# Eşleşmeyi kontrol et
def calculate_match_percentage(job_row, cv_row):
    total_checks = 6
    matches = 0

    if check_work_place_and_duration(job_row, cv_row):
        matches += 1
    if check_location(job_row, cv_row):
        matches += 1
    if check_experience(job_row, cv_row):
        matches += 1
    if check_education(cv_row["DERECE"], job_row["Eğitim Seviyesi"]):
        matches += 1
    matches += check_skills(job_row, cv_row)  # Yetenekler eşleşme oranı (0 ile 1 arasında)
    matches += check_additional_features(cv_row)  # Ek özellikler eşleşme oranı (0 ile 1 arasında)

    return (matches / total_checks) * 100 if total_checks > 0 else 0

# Excel dosyasını yükle
file_name = "/content/merged_output.xlsx"
data = pd.read_excel(file_name)

# Her CV ve iş ilanı için eşleşme oranını hesapla
match_percentages = []
for _, row in data.iterrows():
    match_percentage = calculate_match_percentage(row, row)
    match_percentages.append(match_percentage)

# Eşleşme oranını yeni bir sütun olarak ekle
data["Eşleşme Oranı (%)"] = match_percentages

# Güncellenmiş Excel dosyasını kaydet
data.to_excel(file_name, index=False)

print(f"Eşleşme oranları '{file_name}' dosyasına kaydedildi.")