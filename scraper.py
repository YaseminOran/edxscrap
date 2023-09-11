from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import csv


def accept_cookies(driver):
    try:
        cookie_accept_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_accept_button.click()
        print("Çerez kabul butonuna tıklandı.")
    except:
        print("Çerez bildirim butonu bulunamadı ya da tıklanamadı.")


def click_show_button(driver):
    try:
        show_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-all-link.text-primary-500"))
        )
        show_button.click()
        print("Show butonuna tıklandı.")
    except:
        print("Show butonu bulunamadı ya da tıklanamadı.")


def accept_cookies(driver):
    try:
        cookie_accept_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_accept_button.click()
        print("Çerez kabul butonuna tıklandı.")
    except:
        print("Çerez bildirim butonu bulunamadı ya da tıklanamadı.")

def click_show_button(driver):
    try:
        show_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-all-link.text-primary-500"))
        )
        show_button.click()
        print("Show butonuna tıklandı.")
    except:
        print("Show butonu bulunamadı ya da tıklanamadı.")

def get_all_course_data(driver, max_courses=100):  # max_courses varsayılan olarak 100 olarak ayarlandı
    course_data = []
    course_name_base_xpath = '//*[@id="main-content"]/div/div[4]/div/div[2]/div[{}]/a/div/div[2]/div/div[1]/span/span[1]/{}'
    institution_name_xpath = '//*[@id="main-content"]/div/div[4]/div/div[2]/div[{}]/a/div/div[2]/div/div[2]/span/span[1]/span'

    for i in range(1, max_courses + 1):
        course_name_parts = []

        # Kurs isminin parçalarını topla
        for j in range(1, 6):  # En fazla 5 parça için deneme yap
            try:
                part_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, course_name_base_xpath.format(i, f"span[{j}]")))
                )
                course_name_parts.append(part_element.text)
            except:
                break

        # Eğer hiçbir parça bulunamazsa, bir sonraki kursa geç
        if not course_name_parts:
            continue

        # Eğitim veren kurumun adını topla
        try:
            institution_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, institution_name_xpath.format(i)))
            )
            institution_name = institution_element.text
        except:
            institution_name = "Bilinmiyor"  # Eğer kurum adı bulunamazsa

        # Toplanan veriyi listeye ekle
        course_info = {
            "course_name": " ".join(course_name_parts).strip(),
            "institution": institution_name
        }
        course_data.append(course_info)

    return course_data

def scrape_edx_courses(driver, total_pages=40, save_interval=2):
    all_courses_data = []
    try:
        for page_num in range(1, total_pages + 1):
            # Sayfayı yükle
            url = f"https://www.edx.org/search?subject=Computer+Science&tab=course&page={page_num}"
            driver.get(url)

            # Kurs bilgilerini topla
            current_page_courses = get_all_course_data(driver)
            all_courses_data.extend(current_page_courses)

            # Şu anki sayfa numarasını ve bu sayfadaki toplam kurs sayısını ekrana yazdır
            #print(f"Şu anki sayfa: {page_num} bitti, Bu sayfada toplam {len(current_page_courses)} kurs bulunmaktadır.")
            print(all_courses_data)

            # Belirtilen aralıkta veriyi kaydet
            if page_num % save_interval == 0:
                save_to_csv(all_courses_data, f"page{page_num}.csv")
                all_courses_data = []  # Veriyi kaydettikten sonra listeyi temizle

        # Son sayfanın ardından kalan veriyi kaydet
        if all_courses_data:
            save_to_csv(all_courses_data, f"page{page_num}.csv")
    except Exception as e:
        print(f"Sayfa {page_num} işlenirken bir hata oluştu: {e}")

        return all_courses_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['course_name', 'institution_name', 'institution']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            if 'institution' not in row:
                row['institution'] = ''
            writer.writerow(row)


def append_to_csv(data, filename):
    # Check if the file already exists
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['course_name', 'institution']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is newly created
        if not file_exists:
            writer.writeheader()

        for row in data:
            if 'institution' not in row:
                row['institution'] = ''
            writer.writerow(row)


