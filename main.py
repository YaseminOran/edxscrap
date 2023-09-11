
from scraper import *
# Tarayıcı ayarları
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.edx.org/search?subject=Computer+Science"
driver.get(url)

accept_cookies(driver)
time.sleep(5)
click_show_button(driver)
time.sleep(10)

# 40 sayfa için veriyi topla
all_data = scrape_edx_courses(driver)

# Toplanan veriyi csv dosyasına kaydet
save_to_csv(all_data, "all_courses.csv")

# İşiniz bittiğinde tarayıcıyı kapatmayı unutmayın:
driver.quit()
