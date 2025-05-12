from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import os
import logging
from datetime import datetime
import sys

# تنظیمات لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('library_extension.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # برای نمایش در کنسول
    ]
)

def read_config():
    """خواندن تنظیمات از فایل پیکربندی"""
    config = {}
    try:
        with open('config.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        logging.error("فایل config.txt یافت نشد")
        raise
    except Exception as e:
        logging.error(f"خطا در خواندن فایل پیکربندی: {e}")
        raise
    
    required_fields = ['member_code', 'password']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"فیلد {field} در فایل پیکربندی یافت نشد")
    
    return config

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class LibraryExtension:
    def __init__(self):
        # مسیر نسبی به geckodriver
        self.geckodriver_path = get_resource_path('geckodriver.exe')
        
        # خواندن اطلاعات ورود از فایل پیکربندی
        config = read_config()
        self.member_code = config['member_code']
        self.password = config['password']
        
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """راه‌اندازی درایور Firefox"""
        try:
            if not os.path.exists(self.geckodriver_path):
                raise FileNotFoundError(f"geckodriver not found at: {self.geckodriver_path}")
            
            service = Service(self.geckodriver_path)
            options = webdriver.FirefoxOptions()
            options.set_preference('network.security.ssl.enable_ocsp_stapling', False)
            options.set_preference('security.ssl.enable_ocsp_must_staple', False)
            options.set_preference('security.ssl.enable_ocsp_stapling', False)
            
            self.driver = webdriver.Firefox(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            logging.info("Firefox driver initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing Firefox driver: {e}")
            raise

    def login(self):
        """ورود به سیستم کتابخانه"""
        try:
            logging.info("Attempting to connect to the library website...")
            self.driver.get("https://slib.qom.ac.ir/simwebdata/WebAccess/SimWebPortal.dll/CircPage")
            time.sleep(3)  # افزایش زمان انتظار برای لود شدن صفحه

            # بررسی وضعیت اتصال
            current_url = self.driver.current_url
            if "neterror" in current_url:
                raise ConnectionError("Failed to connect to the library website. Please check your internet connection.")

            # پیدا کردن و پر کردن فرم ورود
            logging.info("Looking for login form elements...")
            member_field = self.wait.until(EC.presence_of_element_located((By.ID, "MemBarcodeIL")))
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, "PasswordIL")))
            
            logging.info("Filling login form...")
            member_field.send_keys(self.member_code)
            password_field.send_keys(self.password)

            # کلیک روی دکمه ورود
            logging.info("Clicking login button...")
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "LoginBtn")))
            login_button.click()
            
            time.sleep(5)  # افزایش زمان انتظار برای لود شدن صفحه بعد از ورود
            logging.info("Successfully logged in")
        except TimeoutException as e:
            logging.error(f"Timeout while trying to access login elements: {e}")
            raise
        except ConnectionError as e:
            logging.error(f"Connection error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            raise

    def get_book_rows(self):
        """دریافت لیست کتاب‌های قابل تمدید"""
        try:
            rows = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[@mainindex]"))
            )
            if not rows:
                logging.info("No books found for extension")
                return []
            return rows
        except TimeoutException:
            logging.info("No books found for extension")
            return []
        except Exception as e:
            logging.error(f"Error getting book rows: {e}")
            return []

    def process_book(self, row, index):
        """پردازش یک کتاب برای تمدید"""
        try:
            # استخراج اطلاعات کتاب
            title = row.find_element(By.XPATH, ".//td[1]").text
            reg_no = row.find_element(By.XPATH, ".//td[2]").text
            loan_date = row.find_element(By.XPATH, ".//td[3]").text
            return_date = row.find_element(By.XPATH, ".//td[4]").text

            logging.info(f"Processing book: {title}")
            logging.info(f"Registration number: {reg_no}")
            logging.info(f"Loan date: {loan_date}")
            logging.info(f"Return date: {return_date}")

            # اسکرول به المان
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", row)
            time.sleep(1)

            # انتخاب کتاب
            self.driver.execute_script("arguments[0].click();", row)
            time.sleep(2)

            # کلیک روی دکمه تمدید
            extend_button = self.wait.until(EC.element_to_be_clickable((By.ID, "ExtendLoanBtn")))
            self.driver.execute_script("arguments[0].click();", extend_button)
            time.sleep(2)

            # تأیید تمدید
            yes_button = self.wait.until(EC.element_to_be_clickable((By.ID, "YesBtn")))
            self.driver.execute_script("arguments[0].click();", yes_button)
            time.sleep(2)

            logging.info(f"Successfully extended book: {title}")
            return True
        except StaleElementReferenceException:
            logging.warning(f"Stale element for book at index {index}, retrying...")
            return False
        except Exception as e:
            logging.error(f"Error processing book at index {index}: {e}")
            return False

    def run(self):
        """اجرای اصلی برنامه"""
        try:
            self.setup_driver()
            self.login()

            while True:
                rows = self.get_book_rows()
                if not rows:
                    break

                for index, row in enumerate(rows):
                    try:
                        # دوباره دریافت کردن المان برای جلوگیری از Stale Element
                        rows = self.driver.find_elements(By.XPATH, "//tr[@mainindex]")
                        row = rows[index]
                        
                        if not self.process_book(row, index):
                            continue

                    except Exception as e:
                        logging.error(f"Error in main loop for book {index}: {e}")
                        continue

                break  # اگر همه کتاب‌ها پردازش شدند، حلقه را متوقف کن

        except Exception as e:
            logging.error(f"Critical error in main process: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Browser closed")

if __name__ == "__main__":
    extension = LibraryExtension()
    extension.run()
