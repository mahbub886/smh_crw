import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# تابع برای دانلود فایل
def download_file(url, folder):
    local_filename = os.path.join(folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {local_filename}")

# تابع خزنده وب
def crawl_website(base_url, file_extension, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # پیدا کردن همه لینک‌ها در صفحه
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(file_extension):
            full_url = urljoin(base_url, href)
            print(f"Found file: {full_url}")
            download_file(full_url, download_folder)

# تنظیمات خزنده
website_url = "https://bayanbox.ir"  # آدرس وب‌سایت هدف
file_format = ".apk"                 # فرمت فایلی که دنبال آن هستید
save_folder = "/sdcard/Download"     # محل ذخیره فایل‌ها

# اجرای خزنده
crawl_website(website_url, file_format, save_folder)
