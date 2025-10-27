from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import os
import glob
import time

class SabyDownloadPage(BasePage):
    """Page Object для страницы загрузок Saby.ru"""
    
    # Константы
    FILE_PATTERNS = ["*.exe", "*.msi", "*.zip", "saby-setup*"]  # Паттерны файлов для поиска
    
    # Селекторы
    DOWNLOAD_LINK = (By.CSS_SELECTOR, "a[href='/download']")  # Ссылка на страницу загрузок
    SABY_DESKTOP_TAB = (By.CSS_SELECTOR, ".controls-TabButton[data-id='plugin']")  # Таб "Saby для десктопа"
    SABY_DESKTOP_SELECTED = (By.CSS_SELECTOR, ".controls-TabButton[data-id='plugin'].controls-Checked__checked")  # Выбранный таб Saby Desktop
    WINDOWS_TAB = (By.CSS_SELECTOR, ".sbis_ru-DownloadNew-innerTabs .controls-TabButton[data-id='default']")  # Таб "Windows"
    WINDOWS_SELECTED = (By.CSS_SELECTOR, ".sbis_ru-DownloadNew-innerTabs .controls-TabButton[data-id='default'].controls-Checked__checked")  # Выбранный таб Windows
    DOWNLOAD_BUTTON = (By.CSS_SELECTOR, "a[href*='saby-setup.exe']")  # Кнопка скачивания
    FILE_VERSION_INFO = (By.CSS_SELECTOR, ".sbis_ru-DownloadNew__version")  # Информация о версии файла

    def __init__(self, driver, download_dir):
        super().__init__(driver)
        self.url = "https://saby.ru"
        self.download_dir = download_dir

    def open_page(self):
        """Открывает главную страницу Saby.ru"""
        self.driver.get(self.url)
        self.wait_for_page_loaded()

    def navigate_to_downloads(self):
        """Переход на страницу загрузок"""
        try:
            self._click_download_link()
            self.wait_for_url_contains("/download", timeout=10)
            self.wait_for_page_loaded()
        except Exception as e:
            self.logger.error(f"Не удалось перейти в раздел загрузок: {e}")
            self.wait_for_page_loaded()

    def _click_download_link(self):
        """Клик по ссылке на страницу загрузок"""
        self.click_element(self.DOWNLOAD_LINK, timeout=10)

    def ensure_saby_desktop_selected(self):
        """Проверка и выбор таба 'Saby для десктопа'"""
        return self._ensure_tab_selected(
            self.SABY_DESKTOP_SELECTED, 
            self.SABY_DESKTOP_TAB,
            "Saby Desktop"
        )

    def ensure_windows_selected(self):
        """Проверка и выбор таба 'Windows'"""
        return self._ensure_tab_selected(
            self.WINDOWS_SELECTED, 
            self.WINDOWS_TAB,
            "Windows"
        )

    def _ensure_tab_selected(self, selected_locator, tab_locator, tab_name):
        """Универсальный метод для проверки и выбора таба"""
        try:
            self.find_element(selected_locator, timeout=5)
            return True
        except:
            self.click_element(tab_locator, timeout=10)
            self.wait_visible(selected_locator, timeout=10)
            return True

    def get_download_info(self):
        """Получение информации о файле для скачивания"""
        download_button = self.wait_visible(self.DOWNLOAD_BUTTON, timeout=10)
        file_url = download_button.get_attribute('href')
        version_info = self._get_version_info()
        
        return {
            'element': download_button,
            'url': file_url,
            'version_info': version_info,
        }

    def _get_version_info(self):
        """Получение информации о версии файла"""
        try:
            version_element = self.find_element(self.FILE_VERSION_INFO, timeout=5)
            return version_element.text
        except:
            self.logger.warning("Не удалось найти информацию о версии")
            return "Неизвестно"

    def download_web_installer(self):
        """Скачивание веб-установщика"""
        self.ensure_saby_desktop_selected()
        self.ensure_windows_selected()
        download_info = self.get_download_info()
        self._clean_download_directory()
        download_info['element'].click()

    def _clean_download_directory(self):
        """Очистка директории загрузки"""
        try:
            for pattern in self.FILE_PATTERNS:
                for file in glob.glob(os.path.join(self.download_dir, pattern)):
                    os.remove(file)
                    self.logger.info(f"Удален старый файл: {file}")
        except Exception as e:
            self.logger.warning(f"Не удалось очистить директорию: {e}")

    def _find_downloaded_files(self):
        """Поиск загруженных файлов"""
        downloaded_files = []
        for pattern in self.FILE_PATTERNS:
            downloaded_files.extend(glob.glob(os.path.join(self.download_dir, pattern)))
        return downloaded_files

    def wait_for_download_complete(self, timeout=60):
        """Ожидание завершения загрузки"""
        self.logger.info("Ожидаем завершения загрузки...")
        start_time = time.time()
        last_size = 0
        stable_count = 0
        
        while time.time() - start_time < timeout:
            downloaded_files = self._find_downloaded_files()
            
            if downloaded_files:
                file_path = max(downloaded_files, key=os.path.getctime)
                if os.path.exists(file_path):
                    current_size = os.path.getsize(file_path)
                    
                    if current_size > 0 and current_size == last_size:
                        stable_count += 1
                        if stable_count >= 2:
                            self.logger.info(f"Загрузка завершена: {file_path} ({current_size} байт)")
                            return file_path
                    else:
                        stable_count = 0
                        last_size = current_size
        
        # Проверка после таймаута
        downloaded_files = self._find_downloaded_files()
        if downloaded_files:
            file_path = max(downloaded_files, key=os.path.getctime)
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                self.logger.warning(f"Загрузка завершена с истечением таймаута: {file_path}")
                return file_path
        
        raise TimeoutError(f"Загрузка не завершилась за {timeout} секунд")

    def get_downloaded_file_size(self, file_path):
        """Получение размера скачанного файла в МБ"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        self.logger.info(f"Размер скачанного файла: {size_mb:.2f} МБ")
        return size_mb
